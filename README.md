# fruits-mcp

MCP server for the [Product Fruits](https://productfruits.com) Knowledge Base API.

## Requirements

- [uv](https://docs.astral.sh/uv/) installed

**Windows:**
```powershell
winget install astral-sh.uv
```

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Claude Desktop setup (Windows)

Edit `%APPDATA%\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "fruits-mcp": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/lucassampsouza/fruits-mcp", "fruits-mcp"],
      "env": {
        "PRODUCT_FRUITS_API_TOKEN": "your_token_here"
      }
    }
  }
}
```

Restart Claude Desktop after saving.

## Claude Code setup

```bash
claude mcp add fruits-mcp uvx -- --from git+https://github.com/lucassampsouza/fruits-mcp fruits-mcp
```

Then set the token:
```bash
# Add to your shell profile or set in Claude Code settings
export PRODUCT_FRUITS_API_TOKEN=your_token_here
```

## Available tools

| Tool | Description |
|---|---|
| `list_articles` | List articles, optionally filtered by category |
| `import_articles` | Create/update articles (up to 50, up to 20 languages each) |
| `delete_article` | Delete an entire article |
| `delete_article_language` | Delete a specific language from an article |
| `delete_article_content_version` | Delete a specific content version |
| `list_categories` | List all categories |
| `get_category` | Get a category by correlationId |
| `import_categories` | Create/update categories |
| `update_category` | Update a category |
| `delete_category` | Delete a category |
| `upload_image` | Upload an image (Base64) |
