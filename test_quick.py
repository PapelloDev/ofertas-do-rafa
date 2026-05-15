#!/usr/bin/env python3
"""
Script de teste rápido para validar configuração do sistema.
Executa um ciclo completo de busca e mostra resultados sem enviar para WhatsApp.
"""

import logging
from amazon_client import AmazonClient
from evolution_client import EvolutionAPIClient
import config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_amazon_connection():
    """Testa conexão com Amazon API"""
    logger.info("=" * 60)
    logger.info("1. TESTANDO CONEXÃO AMAZON API")
    logger.info("=" * 60)
    
    try:
        client = AmazonClient()
        logger.info("✅ Cliente Amazon inicializado")
        
        logger.info("\nBuscando produtos com desconto...")
        products = client.search_deals(
            keywords="fone bluetooth",
            min_discount=15,
            search_index="Electronics",
            max_results=5
        )
        
        if products:
            logger.info(f"✅ Encontrados {len(products)} produtos com desconto!")
            logger.info("\n📦 PRODUTOS ENCONTRADOS:\n")
            
            for i, product in enumerate(products, 1):
                logger.info(f"{i}. {product['title'][:60]}...")
                logger.info(f"   💰 Preço: R$ {product['current_price']:.2f}")
                logger.info(f"   📉 Desconto: {product['discount_percent']:.0f}%")
                logger.info(f"   🏷️  Marca: {product.get('brand', 'N/A')}")
                logger.info("")
            
            return True, products
        else:
            logger.warning("⚠️  Nenhum produto encontrado com os critérios especificados")
            logger.info("💡 Dica: Tente reduzir PRICE_DROP_THRESHOLD no .env")
            return False, []
            
    except Exception as e:
        logger.error(f"❌ Erro ao conectar com Amazon API: {e}")
        logger.info("\n🔧 Verifique:")
        logger.info("   - Credenciais no arquivo .env")
        logger.info("   - Versão da credencial (2.1, 2.2, 2.3, etc)")
        logger.info("   - Execute: python validate_credentials.py")
        return False, []

def test_evolution_connection():
    """Testa conexão com Evolution API"""
    logger.info("=" * 60)
    logger.info("2. TESTANDO CONEXÃO EVOLUTION API")
    logger.info("=" * 60)
    
    try:
        client = EvolutionAPIClient()
        logger.info("✅ Cliente Evolution inicializado")
        
        logger.info(f"\nURL: {config.EVOLUTION_API_URL}")
        logger.info(f"Instância: {config.EVOLUTION_INSTANCE_NAME}")
        
        is_connected = client.check_connection()
        
        if is_connected:
            logger.info("✅ Evolution API conectada e funcionando!")
            return True
        else:
            logger.warning("⚠️  Evolution API não está conectada")
            logger.info("\n🔧 Verifique:")
            logger.info("   - Evolution API está rodando")
            logger.info("   - URL e API Key no .env estão corretos")
            logger.info("   - Instância existe e está ativa")
            return False
            
    except Exception as e:
        logger.error(f"❌ Erro ao conectar com Evolution API: {e}")
        logger.info("\n🔧 Verifique:")
        logger.info("   - Evolution API está rodando: curl http://localhost:8080")
        logger.info("   - Configurações no arquivo .env")
        return False

def test_whatsapp_group():
    """Valida configuração do grupo WhatsApp"""
    logger.info("=" * 60)
    logger.info("3. VALIDANDO GRUPO WHATSAPP")
    logger.info("=" * 60)
    
    group_id = config.WHATSAPP_GROUP_ID
    
    if not group_id:
        logger.error("❌ ID do grupo WhatsApp não configurado!")
        logger.info("\n🔧 Para obter o ID do grupo:")
        logger.info("   1. Execute: python get_group_id.py")
        logger.info("   2. Copie o ID do grupo desejado")
        logger.info("   3. Cole no arquivo .env em WHATSAPP_GROUP_ID")
        return False
    
    logger.info(f"✅ Grupo configurado: {group_id}")
    
    if not group_id.endswith('@g.us'):
        logger.warning("⚠️  Formato do ID pode estar incorreto")
        logger.info("   Formato esperado: 120363123456789012@g.us")
        return False
    
    return True

def show_configuration():
    """Mostra configuração atual"""
    logger.info("=" * 60)
    logger.info("4. CONFIGURAÇÃO ATUAL")
    logger.info("=" * 60)
    
    logger.info(f"\n📊 Parâmetros de Monitoramento:")
    logger.info(f"   • Desconto mínimo: {config.PRICE_DROP_THRESHOLD}%")
    logger.info(f"   • Intervalo de verificação: {config.CHECK_INTERVAL_MINUTES} minutos")
    logger.info(f"   • Produtos por mensagem: {config.MAX_PRODUCTS_PER_MESSAGE}")
    
    logger.info(f"\n🔍 Keywords monitoradas ({len(config.SEARCH_KEYWORDS)}):")
    for keyword in config.SEARCH_KEYWORDS[:5]:
        logger.info(f"   • {keyword}")
    if len(config.SEARCH_KEYWORDS) > 5:
        logger.info(f"   ... e mais {len(config.SEARCH_KEYWORDS) - 5}")

def preview_message(products):
    """Mostra preview de como ficaria a mensagem"""
    if not products:
        return
    
    logger.info("=" * 60)
    logger.info("5. PREVIEW DA MENSAGEM")
    logger.info("=" * 60)
    
    client = EvolutionAPIClient()
    product = products[0]
    
    message = client.format_single_deal_message(product)
    
    logger.info("\n📱 Assim ficaria a mensagem no WhatsApp:\n")
    logger.info("-" * 60)
    logger.info(message)
    logger.info("-" * 60)

def main():
    """Executa todos os testes"""
    logger.info("\n")
    logger.info("🚀 TESTE RÁPIDO DO SISTEMA DE OFERTAS AMAZON")
    logger.info("=" * 60)
    logger.info("")
    
    results = {
        'amazon': False,
        'evolution': False,
        'whatsapp': False
    }
    
    products = []
    
    results['amazon'], products = test_amazon_connection()
    logger.info("")
    
    results['evolution'] = test_evolution_connection()
    logger.info("")
    
    results['whatsapp'] = test_whatsapp_group()
    logger.info("")
    
    show_configuration()
    logger.info("")
    
    if products:
        preview_message(products)
        logger.info("")
    
    logger.info("=" * 60)
    logger.info("📋 RESUMO DOS TESTES")
    logger.info("=" * 60)
    
    status_emoji = lambda x: "✅" if x else "❌"
    
    logger.info(f"\n{status_emoji(results['amazon'])} Amazon API: {'OK' if results['amazon'] else 'FALHOU'}")
    logger.info(f"{status_emoji(results['evolution'])} Evolution API: {'OK' if results['evolution'] else 'FALHOU'}")
    logger.info(f"{status_emoji(results['whatsapp'])} Grupo WhatsApp: {'OK' if results['whatsapp'] else 'FALHOU'}")
    
    all_ok = all(results.values())
    
    logger.info("")
    if all_ok:
        logger.info("🎉 TUDO PRONTO! Sistema configurado corretamente.")
        logger.info("\n📌 Próximos passos:")
        logger.info("   1. Execute: python main.py")
        logger.info("   2. Aguarde as ofertas serem enviadas")
        logger.info("   3. Monitore os logs: tail -f deal_monitor.log")
    else:
        logger.warning("⚠️  ATENÇÃO: Alguns testes falharam.")
        logger.info("\n📌 Corrija os problemas acima antes de executar o sistema.")
        logger.info("   Consulte: GUIA-USO.md para mais detalhes")
    
    logger.info("")
    logger.info("=" * 60)
    
    return all_ok

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
