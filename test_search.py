#!/usr/bin/env python3
"""
Script de teste para busca de produtos
"""

import logging
from amazon_client import AmazonClient

# Configurar logging para ver detalhes
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    print("=" * 60)
    print("Teste de Busca de Produtos - Amazon Creators API")
    print("=" * 60)
    print()
    
    # Inicializar cliente
    print("Inicializando cliente...")
    client = AmazonClient()
    print(f"Marketplace: {client.marketplace}")
    print(f"Partner Tag: {client.partner_tag}")
    print(f"Version: {client.version}")
    print()
    
    # Teste 1: Busca simples
    print("Teste 1: Busca simples por 'fone bluetooth'")
    print("-" * 60)
    products = client.search_items(
        keywords="fone bluetooth",
        search_index="Electronics",
        item_count=5
    )
    print(f"Produtos encontrados: {len(products)}")
    
    if products:
        for i, p in enumerate(products[:3], 1):
            print(f"\n{i}. {p['title'][:60]}...")
            print(f"   Preço: R$ {p['current_price']:.2f}")
            if p['discount_percent'] > 0:
                print(f"   Desconto: {p['discount_percent']}%")
    else:
        print("Nenhum produto encontrado")
    
    print()
    print("=" * 60)
    
    # Teste 2: Busca com desconto
    print("\nTeste 2: Busca com desconto mínimo de 20%")
    print("-" * 60)
    deals = client.search_deals(
        keywords="fone bluetooth",
        min_discount=20,
        search_index="Electronics",
        max_results=5
    )
    print(f"Ofertas encontradas: {len(deals)}")
    
    if deals:
        for i, p in enumerate(deals[:3], 1):
            print(f"\n{i}. {p['title'][:60]}...")
            print(f"   De: R$ {p['original_price']:.2f}")
            print(f"   Por: R$ {p['current_price']:.2f}")
            print(f"   Desconto: {p['discount_percent']}%")
            print(f"   Em estoque: {'Sim' if p['in_stock'] else 'Não'}")
    else:
        print("Nenhuma oferta encontrada")
    
    print()
    print("=" * 60)

if __name__ == '__main__':
    main()
