import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

function serveStaticFile(context, filename, statusCode = 404) {
  const filePath = path.join(__dirname, "..", "public", filename);
  try {
    const html = fs.readFileSync(filePath, "utf8");
    context.res = {
      status: statusCode,
      headers: { "Content-Type": "text/html" },
      body: html
    };
  } catch (err) {
    context.log.error("Could not load fallback 404 page:", err.message);
    context.res = {
      status: 500,
      body: "Internal error loading 404 page"
    };
  }
}

export default async function (context, req) {
  serveStaticFile(context, "404.html", 404);
}
