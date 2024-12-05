import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";
import path from 'path';
import { fileURLToPath } from 'url';
import fs from 'fs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Function to find the server file
function findServerFile(startDir) {
  let currentDir = startDir;
  while (currentDir !== path.parse(currentDir).root) {
    const serverPath = path.join(currentDir, 'server', 'index.js');
    if (fs.existsSync(serverPath)) {
      return serverPath;
    }
    currentDir = path.dirname(currentDir);
  }
  throw new Error('Server file not found');
}

// Find the server file
const serverPath = findServerFile(__dirname);
console.log('Server path:', serverPath);

// Define the transport to communicate with the server
const transport = new StdioClientTransport({
  command: `"${process.execPath}" "${serverPath}"`,
});

// Initialize the MCP client
const client = new Client({
  name: "example-client",
  version: "1.0.0",
}, {
  capabilities: {}
});

async function main() {
  try {
    // Connect the client to the server
    await client.connect(transport);
    console.log("Connected to server successfully");

    // List available resources
    const resources = await client.request(
      { method: "resources/list" },
      {
        type: "object",
        properties: {
          resources: {
            type: "array",
            items: {
              type: "object",
              properties: {
                uri: { type: "string" },
                name: { type: "string" },
              },
            },
          },
        },
      }
    );
    console.log("Resources List:", resources);

    // Read example.txt
    const resourceContent = await client.request(
      {
        method: "resources/read",
        params: {
          uri: "file:///example.txt",
        },
      },
      {
        type: "object",
        properties: {
          contents: {
            type: "array",
            items: {
              type: "object",
              properties: {
                uri: { type: "string" },
                mimeType: { type: "string" },
                text: { type: "string" },
              },
            },
          },
        },
      }
    );
    console.log("Resource Content:", resourceContent.contents[0].text);

  } catch (error) {
    console.error("Error:", error);
    process.exit(1);
  }
}

main();

