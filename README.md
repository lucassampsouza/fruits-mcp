# fruits-mcp

MCP server for the [Product Fruits](https://productfruits.com) Knowledge Base API.

## Setup

Set your API token via environment variable:

```bash
export PRODUCT_FRUITS_API_TOKEN=your_token_here
```

## Usage with uvx (after publishing to PyPI)

```bash
uvx fruits-mcp
```

## Usage with uvx (local)

```bash
uvx --from /path/to/fruits-mcp fruits-mcp
```

## Claude Code / Claude Desktop config

```json
{
  "mcpServers": {
    "fruits-mcp": {
      "command": "uvx",
      "args": ["fruits-mcp"],
      "env": {
        "PRODUCT_FRUITS_API_TOKEN": "your_token_here"
      }
    }
  }
}
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
