#!/usr/bin/env python3
"""
Script para testar acesso à Amazon Product Advertising API
"""

import os
import sys
from dotenv import load_dotenv
from amazon_client import AmazonClient

# Carregar variáveis de ambiente
load_dotenv()

def test_amazon_api():
    """Testa conexão e acesso à API da Amazon"""
    
    print("=" * 60)
    print("🧪 TESTE DE ACESSO À AMAZON API")
    print("=" * 60)
    print()
    
    # Verificar credenciais
    print("📋 Verificando credenciais...")
    credential_id = os.getenv('AMAZON_CREDENTIAL_ID')
    credential_secret = os.getenv('AMAZON_CREDENTIAL_SECRET')
    partner_tag = os.getenv('AMAZON_PARTNER_TAG')
    marketplace = os.getenv('AMAZON_MARKETPLACE', 'www.amazon.com.br')
    
    if not credential_id:
        print("❌ AMAZON_CREDENTIAL_ID não encontrado no .env")
        return False
    
    if not credential_secret:
        print("❌ AMAZON_CREDENTIAL_SECRET não encontrado no .env")
        return False
    
    if not partner_tag:
        print("❌ AMAZON_PARTNER_TAG não encontrado no .env")
        return False
    
    print(f"✅ Credential ID: {credential_id[:20]}...")
    print(f"✅ Partner Tag: {partner_tag}")
    print(f"✅ Marketplace: {marketplace}")
    print()
    
    # Inicializar cliente
    print("🔌 Inicializando cliente Amazon...")
    try:
        client = AmazonClient()
        print("✅ Cliente inicializado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao inicializar cliente: {e}")
        return False
    
    print()
    
    # Testar busca de produto
    print("🔍 Testando busca de produto...")
    test_asin = "B0CSTJ7C6R"  # ASIN de teste (produto comum)
    
    try:
        print(f"   Buscando ASIN: {test_asin}")
        
        # Testar request direta para ver o erro real
        payload = {
            "partnerTag": partner_tag,
            "itemIds": [test_asin],
            "itemIdType": "ASIN",
            "resources": [
                "images.primary.large",
                "itemInfo.title",
                "offersV2.listings.price"
            ]
        }
        
        print("   Fazendo request direta à API...")
        response = client._make_request("GetItems", payload)
        
        print(f"   Status da resposta: OK")
        print(f"   Dados retornados: {list(response.keys())}")
        
        # Verificar se há items
        items = response.get('itemsResult', {}).get('items', [])
        print(f"   Items encontrados: {len(items)}")
        
        if items:
            print("✅ Produto encontrado!")
            item = items[0]
            title = item.get('itemInfo', {}).get('title', {}).get('displayValue', 'N/A')
            print(f"   Título: {title[:60]}...")
            print()
            print("=" * 60)
            print("✅ SUCESSO! API da Amazon está funcionando!")
            print("=" * 60)
            return True
        else:
            print("⚠️ Nenhum item retornado")
            print(f"   Resposta completa: {response}")
            print()
            
            # Verificar tipo de erro
            output_type = response.get('Output', {}).get('__type', '')
            
            if 'InternalFailure' in output_type:
                print("=" * 60)
                print("❌ ERRO: InternalFailure")
                print("=" * 60)
                print()
                print("Isso geralmente significa que:")
                print()
                print("1. ❌ Sua conta ainda NÃO foi aprovada pela Amazon")
                print("   para usar a Product Advertising API")
                print()
                print("2. ⏳ Você ainda não completou os requisitos:")
                print("   - 3 vendas qualificadas nos últimos 180 dias")
                print("   - Vendas devem ser de produtos diferentes")
                print("   - Vendas devem ser concluídas (não canceladas)")
                print()
                print("3. 📋 Próximos passos:")
                print("   a) Verifique seu painel de afiliados da Amazon")
                print("   b) Confirme quantas vendas qualificadas você tem")
                print("   c) Aguarde aprovação (pode levar alguns dias)")
                print()
                print("💡 Dica: Você mencionou ter feito 10 vendas de teste.")
                print("   Verifique se essas vendas foram:")
                print("   - De produtos diferentes (não o mesmo produto 10x)")
                print("   - Concluídas e não canceladas")
                print("   - Feitas através do seu link de afiliado")
                print()
            else:
                print("=" * 60)
                print("⚠️ API respondeu mas não retornou dados do produto")
                print("=" * 60)
            
            return False
            
    except Exception as e:
        print(f"❌ Erro ao buscar produto: {e}")
        print()
        
        # Verificar tipo de erro
        error_str = str(e).lower()
        
        if 'unauthorized' in error_str or '401' in error_str:
            print("=" * 60)
            print("❌ ERRO DE AUTENTICAÇÃO")
            print("=" * 60)
            print()
            print("Possíveis causas:")
            print("1. Credenciais inválidas ou expiradas")
            print("2. Ainda não completou as 3 vendas qualificadas")
            print("3. Conta ainda não foi aprovada pela Amazon")
            print()
            print("💡 Dica: Verifique seu painel de afiliados da Amazon")
            print("   para confirmar o status da sua conta.")
            
        elif 'forbidden' in error_str or '403' in error_str:
            print("=" * 60)
            print("❌ ACESSO NEGADO")
            print("=" * 60)
            print()
            print("Possíveis causas:")
            print("1. Sua conta ainda não tem acesso à Product Advertising API")
            print("2. Você precisa completar mais vendas qualificadas")
            print("3. Sua aplicação não foi aprovada")
            
        elif 'not found' in error_str or '404' in error_str:
            print("=" * 60)
            print("⚠️ ENDPOINT NÃO ENCONTRADO")
            print("=" * 60)
            print()
            print("Possíveis causas:")
            print("1. URL da API está incorreta")
            print("2. Versão da API está desatualizada")
            
        else:
            print("=" * 60)
            print("❌ ERRO DESCONHECIDO")
            print("=" * 60)
            print()
            print(f"Detalhes: {e}")
        
        print()
        return False

if __name__ == '__main__':
    success = test_amazon_api()
    sys.exit(0 if success else 1)
