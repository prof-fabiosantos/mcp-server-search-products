
from typing import List
from mcp.server.fastmcp import FastMCP
import httpx
from bs4 import BeautifulSoup
import asyncio

mcp = FastMCP("BestPriceFinder")

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

async def search_product(url: str, query: str, product_selector: str) -> str:
    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            response = await client.get(f"{url}{query}", headers=HEADERS)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            results = soup.select(product_selector)
            return results[0].get_text(strip=True) if results else "Produto não encontrado"
        except Exception as e:
            return f"Erro ao buscar em {url}: {str(e)}"

@mcp.tool()
async def get_best_prices(product: str) -> List[str]:
    """
    Busca os melhores preços de um produto nos sites: Americanas, Carrefour, Magalu, Havan.
    """
    results = await asyncio.gather(
        search_product("https://www.americanas.com.br/busca/", product, ".product-name"),
        search_product("https://www.carrefour.com.br/busca/", product, ".product-card__title"),
        search_product("https://www.magazineluiza.com.br/busca/", product, ".product-title"),
        search_product("https://www.havan.com.br/busca/", product, ".product-item__name")
    )
    lojas = ["Americanas", "Carrefour", "Magalu", "Havan"]
    return [f"{loja}: {res}" for loja, res in zip(lojas, results)]

if __name__ == "__main__":
    mcp.run(transport="sse")
