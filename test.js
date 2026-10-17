const fs = require("fs");
const path = require("path");

console.log("=== Running CI Automated Tests ===");

const indexPath = path.join(__dirname, "index.html");
if (!fs.existsSync(indexPath)) {
  console.error("Test failed: index.html does not exist!");
  process.exit(1);
}
console.log("PASS: index.html exists.");

const content = fs.readFileSync(indexPath, "utf8");
if (!content.includes("Hello World")) {
  console.error("Test failed: index.html must contain 'Hello World'!");
  process.exit(1);
}
console.log("PASS: index.html contains 'Hello World'.");

console.log("=== All tests passed successfully! ===");
process.exit(0);
