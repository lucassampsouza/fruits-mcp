import os
import base64
import httpx
from mcp.server.fastmcp import FastMCP

BASE_URL = "https://api.productfruits.com/v1/knowledgebase"

mcp = FastMCP("fruits-mcp")


def get_client() -> httpx.AsyncClient:
    token = os.environ.get("PRODUCT_FRUITS_API_TOKEN")
    if not token:
        raise ValueError("PRODUCT_FRUITS_API_TOKEN environment variable is not set.")
    return httpx.AsyncClient(
        base_url=BASE_URL,
        headers={"Authorization": f"Bearer {token}"},
        timeout=30,
    )


async def api_request(method: str, path: str, **kwargs) -> dict:
    async with get_client() as client:
        response = await client.request(method, path, **kwargs)
        response.raise_for_status()
        if response.content:
            return response.json()
        return {}


# ─── ARTICLES ────────────────────────────────────────────────────────────────

@mcp.tool()
async def list_articles(category_correlation_id: str = "") -> dict:
    """List all knowledge base articles. Optionally filter by category correlation ID."""
    params = {}
    if category_correlation_id:
        params["categoryCorrelationId"] = category_correlation_id
    return await api_request("GET", "/articles", params=params)


@mcp.tool()
async def import_articles(articles: list[dict]) -> dict:
    """
    Import or update knowledge base articles (max 50 per request, up to 20 languages each).
    Each article requires 'correlationId' and 'contents'. Each content entry requires
    'lang', 'title', and 'content'. Optional fields: 'format' (markdown|html),
    'publishStatus' (published|draft), 'categoryCorrelationId', 'isPrivate',
    'ignoreImportErrors'.
    """
    return await api_request("POST", "/import", json={"articles": articles})


@mcp.tool()
async def delete_article(correlation_id: str) -> dict:
    """Delete an entire article (all languages) by its correlation ID."""
    return await api_request("DELETE", f"/articles/{correlation_id}")


@mcp.tool()
async def delete_article_language(correlation_id: str, lang: str) -> dict:
    """Delete all content versions for a specific language from an article."""
    return await api_request("DELETE", f"/articles/{correlation_id}/content/{lang}")


@mcp.tool()
async def delete_article_content_version(
    correlation_id: str, lang: str, content_id: str
) -> dict:
    """Delete a specific content version from an article language."""
    return await api_request(
        "DELETE", f"/articles/{correlation_id}/content/{lang}/{content_id}"
    )


# ─── CATEGORIES ──────────────────────────────────────────────────────────────

@mcp.tool()
async def list_categories() -> dict:
    """Get all categories from the knowledge base."""
    return await api_request("GET", "/categories")


@mcp.tool()
async def get_category(correlation_id: str) -> dict:
    """Retrieve a specific category by its correlation ID."""
    return await api_request("GET", f"/categories/{correlation_id}")


@mcp.tool()
async def import_categories(categories: list[dict]) -> dict:
    """
    Import or update knowledge base categories. Creates if not found, updates if existing.
    Each category requires 'correlationId' and 'name'. Optional: 'parentCorrelationId',
    'isPrivate', 'order'.
    """
    return await api_request("POST", "/categories/import", json={"categories": categories})


@mcp.tool()
async def update_category(
    correlation_id: str,
    name: str = "",
    parent_correlation_id: str = "",
    is_private: bool | None = None,
    order: int | None = None,
) -> dict:
    """Update an existing category by its correlation ID."""
    body: dict = {}
    if name:
        body["name"] = name
    if parent_correlation_id:
        body["parentCorrelationId"] = parent_correlation_id
    if is_private is not None:
        body["isPrivate"] = is_private
    if order is not None:
        body["order"] = order
    return await api_request("PUT", f"/categories/{correlation_id}", json=body)


@mcp.tool()
async def delete_category(correlation_id: str) -> dict:
    """Delete a category by its correlation ID."""
    return await api_request("DELETE", f"/categories/{correlation_id}")


# ─── IMAGES ──────────────────────────────────────────────────────────────────

@mcp.tool()
async def upload_image(image_base64: str, mime_type: str, filename: str) -> dict:
    """
    Upload an image to use in knowledge base articles.
    Provide the image as a Base64-encoded string along with its MIME type
    (e.g. 'image/png') and filename (e.g. 'cover.png').
    """
    token = os.environ.get("PRODUCT_FRUITS_API_TOKEN")
    if not token:
        raise ValueError("PRODUCT_FRUITS_API_TOKEN environment variable is not set.")

    image_bytes = base64.b64decode(image_base64)
    files = {"file": (filename, image_bytes, mime_type)}

    async with httpx.AsyncClient(
        base_url=BASE_URL,
        headers={"Authorization": f"Bearer {token}"},
        timeout=60,
    ) as client:
        response = await client.post("/upload-image", files=files)
        response.raise_for_status()
        return response.json()


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
