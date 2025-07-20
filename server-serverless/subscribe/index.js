import { v4 as uuidv4 } from "uuid";
import { container } from "../cosmosClient.js";
import fs from "fs";
import path from "path";
import { fileURLToPath } from 'url';
import nodemailer from 'nodemailer';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Function to create email transporter
function createTransporter() {
  const gmailUsername = process.env["GMAIL_USERNAME"];
  const gmailPassword = process.env["GMAIL_PASSWORD"];

  if (!gmailUsername || !gmailPassword) {
    return null;
  }

  return nodemailer.createTransport({
    service: 'gmail',
    auth: {
      user: gmailUsername,
      pass: gmailPassword
    }
  });
}

// Function to send welcome email
async function sendWelcomeEmail(email, userId, context) {
  const transporter = createTransporter();
  if (!transporter) {
    context.log.warn("Email configuration missing - skipping welcome email");
    return;
  }

  // Read the email template
  const templatePath = path.join(__dirname, "..", "public", "welcome-email.html");
  let emailHtml;
  try {
    emailHtml = fs.readFileSync(templatePath, "utf8");
  } catch (error) {
    context.log.error("Failed to load welcome email template:", error.message);
    return;
  }

  // Replace the unsubscribe link with the actual user ID
  const baseUrl = process.env["BASE_URL"];
  if (!baseUrl) {
    context.log.error("BASE_URL environment variable is not set!");
    // Fallback to a default value for testing
    context.log.warn("Using default BASE_URL for testing");
    const unsubscribeLink = `https://newsletter--server.azurewebsites.net/api/unsubscribe/${userId}`;
    emailHtml = emailHtml.replace("{{UNSUB_LINK}}", unsubscribeLink);
  } else {
    context.log.info("BASE_URL from environment:", baseUrl);
    const unsubscribeLink = `${baseUrl}/api/unsubscribe/${userId}`;
    emailHtml = emailHtml.replace("{{UNSUB_LINK}}", unsubscribeLink);
  }
  
  context.log.info("Full email HTML:", emailHtml);

  const mailOptions = {
    from: process.env["GMAIL_USERNAME"],
    to: email,
    subject: 'Thank you for subscribing to AniNews!',
    html: emailHtml
  };

  try {
    await transporter.sendMail(mailOptions);
    context.log.info("Welcome email sent successfully to:", email);
  } catch (emailError) {
    context.log.error("Error sending welcome email:", emailError.message);
    // Don't throw - we want to continue even if email fails
  }
}

function serveStaticFile(context, filename, statusCode = 200) {
  const filePath = path.join(__dirname, "..", "public", filename);
  try {
    const html = fs.readFileSync(filePath, "utf8");
    context.res = {
      status: statusCode,
      headers: { "Content-Type": "text/html" },
      body: html,
    };
  } catch (error) {
    context.log.error("Failed to load static file:", filename, error.message);
    context.res = {
      status: 500,
      body: "Internal server error while loading HTML.",
    };
  }
}

export default async function (context, req) {
  if (req.method !== "POST" || !req.body?.email) {
    serveStaticFile(context, "404.html", 404);
    return;
  }

  const email = req.body?.email;

  try {
    const querySpec = {
      query: "SELECT * FROM c WHERE c.email = @email",
      parameters: [{ name: "@email", value: email }],
    };

    const { resources: existingUsers } = await container.items
      .query(querySpec, { enableCrossPartitionQuery: true })
      .fetchAll();

    if (existingUsers.length > 0) {
      context.res = { status: 409, body: { error: "Email already subscribed" } };
      return;
    }

    const userId = uuidv4();
    const user = {
      id: userId,
      email,
      subscribed_at: new Date().toISOString(),
    };

    const { resource } = await container.items.create(user);

    // Try to send welcome email, but don't let it affect the subscription
    await sendWelcomeEmail(email, userId, context);

    context.res = { status: 201, body: resource };
  } catch (err) {
    context.log.error("Error subscribing user:", err.message);
    context.res = { status: 509, body: { error: "Error subscribing user" } };
  }
}
