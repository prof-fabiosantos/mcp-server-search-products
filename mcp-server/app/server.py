from typing import List
from mcp.server.fastmcp import FastMCP
import random
import asyncio

mcp = FastMCP("BestPriceSimulator")

LOJAS = ["Americanas", "Carrefour", "Magalu", "Havan"]

def gerar_preco_fake() -> str:
    return f"R${random.uniform(50.0, 500.0):.2f}".replace('.', ',')

async def simular_busca(nome_loja: str, produto: str) -> str:
    await asyncio.sleep(random.uniform(0.5, 1.5))  # Simula tempo de resposta
    return f"{nome_loja}: {produto} por {gerar_preco_fake()}"

@mcp.tool()
async def get_fake_best_prices(produto: str) -> List[str]:
    """
    Retorna preços simulados para um produto nas lojas: Americanas, Carrefour, Magalu, Havan.
    """
    resultados = await asyncio.gather(
        *[simular_busca(loja, produto) for loja in LOJAS]
    )
    return resultados

if __name__ == "__main__":
    mcp.run(transport="sse")


