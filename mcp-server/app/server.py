from typing import List
from mcp.server.fastmcp import FastMCP
import httpx

mcp = FastMCP("MercadoLivre")

API_URL = "https://api.mercadolibre.com/sites/MLB/search"

@mcp.tool()
async def get_meli_prices(produto: str) -> List[str]:
    """
    Busca preços reais de um produto no Mercado Livre.
    """
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(API_URL, params={"q": produto})
            response.raise_for_status()
            results = response.json().get("results", [])[:5]

            if not results:
                return ["Nenhum resultado encontrado."]

            return [
                f"{item['title']} - R${item['price']:.2f}"
                for item in results
            ]

    except Exception as e:
        return [f"Erro ao consultar Mercado Livre: {str(e)}"]

if __name__ == "__main__":
    mcp.run(transport="sse")


