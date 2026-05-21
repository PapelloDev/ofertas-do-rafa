#!/usr/bin/env python3
"""
Script para regenerar todas as páginas de produtos
"""

import requests
import json
import os

# Configurações
API_URL = 'http://localhost:5001/api/generate-product-page'
DATA_FILE = 'site/data/produtos.json'

def regenerate_all_products():
    """Regenera todas as páginas de produtos"""
    
    # Ler produtos
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    produtos = data.get('produtos', [])
    
    print(f"🔄 Regenerando {len(produtos)} páginas de produtos...")
    print()
    
    success_count = 0
    error_count = 0
    
    for produto in produtos:
        asin = produto.get('asin')
        titulo = produto.get('titulo', '')
        
        try:
            response = requests.post(API_URL, json={'asin': asin})
            
            if response.status_code == 200:
                print(f"✅ {titulo[:50]}...")
                success_count += 1
            else:
                print(f"❌ Erro ao regenerar {titulo[:50]}: {response.status_code}")
                error_count += 1
                
        except Exception as e:
            print(f"❌ Erro ao regenerar {titulo[:50]}: {e}")
            error_count += 1
    
    print()
    print("=" * 60)
    print(f"✅ Sucesso: {success_count}")
    print(f"❌ Erros: {error_count}")
    print("=" * 60)

if __name__ == '__main__':
    regenerate_all_products()
