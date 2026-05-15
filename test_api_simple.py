#!/usr/bin/env python3
"""
Teste simples da API para verificar elegibilidade
"""

import requests
import json
from amazon_auth import AmazonAuth
import config

def test_api():
    print("=" * 60)
    print("Teste de Elegibilidade - Amazon Creators API")
    print("=" * 60)
    print()
    
    # Autenticar
    print("1. Autenticando...")
    auth = AmazonAuth(
        config.AMAZON_CREDENTIAL_ID,
        config.AMAZON_CREDENTIAL_SECRET,
        config.AMAZON_CREDENTIAL_VERSION
    )
    
    token = auth.get_valid_token()
    print(f"   ✓ Token obtido: {token[:20]}...")
    print()
    
    # Testar SearchItems
    print("2. Testando SearchItems...")
    url = "https://creatorsapi.amazon/SearchItems"
    
    headers = {
        'Authorization': auth.get_auth_header(),
        'Content-Type': 'application/json',
        'x-marketplace': config.AMAZON_MARKETPLACE
    }
    
    payload = {
        "partnerTag": config.AMAZON_PARTNER_TAG,
        "keywords": "fone",
        "searchIndex": "All",
        "itemCount": 1,
        "resources": ["itemInfo.title"]
    }
    
    print(f"   URL: {url}")
    print(f"   Marketplace: {config.AMAZON_MARKETPLACE}")
    print(f"   Partner Tag: {config.AMAZON_PARTNER_TAG}")
    print()
    
    response = requests.post(url, json=payload, headers=headers)
    
    print(f"   Status: {response.status_code}")
    print(f"   Response:")
    print(json.dumps(response.json(), indent=2))
    print()
    
    # Verificar elegibilidade
    if response.status_code == 200:
        data = response.json()
        
        if 'Output' in data and '__type' in data['Output']:
            error_type = data['Output']['__type']
            
            if 'InternalFailure' in error_type:
                print("❌ ERRO: InternalFailure")
                print()
                print("Possíveis causas:")
                print("1. Conta não elegível (precisa 10 vendas nos últimos 30 dias)")
                print("2. Partner Tag incorreto ou não vinculado")
                print("3. Marketplace incorreto")
                print()
                print("Verificações:")
                print(f"   - Partner Tag: {config.AMAZON_PARTNER_TAG}")
                print(f"   - Marketplace: {config.AMAZON_MARKETPLACE}")
                print(f"   - Credential Version: {config.AMAZON_CREDENTIAL_VERSION}")
                print()
                print("Ações:")
                print("1. Verifique se a conta tem 10 vendas qualificadas")
                print("2. Verifique se o Partner Tag está correto")
                print("3. Acesse: https://associados.amazon.com.br/")
        
        elif 'searchResult' in data:
            items = data.get('searchResult', {}).get('items', [])
            print(f"✓ Sucesso! {len(items)} produtos encontrados")
    
    elif response.status_code == 403:
        print("❌ ERRO 403: Acesso negado")
        print("   Conta não elegível para Creators API")
        print("   Precisa de 10 vendas qualificadas nos últimos 30 dias")
    
    else:
        print(f"❌ ERRO {response.status_code}")

if __name__ == '__main__':
    test_api()
