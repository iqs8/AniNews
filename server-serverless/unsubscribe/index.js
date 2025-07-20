import { container } from "../cosmosClient.js";
import fs from "fs";
import path from "path";
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

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
  const id = context.bindingData.id;
  context.log("Unsubscribe request received for ID:", id);

  if (!id) {
    serveStaticFile(context, "500.html", 500);
    return;
  }

  try {
    const { resource } = await container.item(id, id).read();

    if (!resource) {
      context.log.warn("User not found:", id);
      serveStaticFile(context, "500.html", 500);
      return;
    }

    await container.item(id, id).delete();
    context.log("Unsubscribed user:", id);
    serveStaticFile(context, "unsub-success.html");
  } catch (err) {
    context.log.error("Error during unsubscribe:", err.message);
    serveStaticFile(context, "500.html", 500);
  }
}
