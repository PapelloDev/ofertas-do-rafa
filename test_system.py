import logging
from deal_monitor import DealMonitor
from evolution_client import EvolutionAPIClient
from database import Database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_evolution_connection():
    logger.info("=== Testando conexão com Evolution API ===")
    client = EvolutionAPIClient()
    
    if client.check_connection():
        logger.info("✅ Conexão com Evolution API estabelecida")
        return True
    else:
        logger.error("❌ Falha na conexão com Evolution API")
        return False

def test_database():
    logger.info("=== Testando banco de dados ===")
    try:
        db = Database()
        logger.info("✅ Banco de dados inicializado")
        
        test_product = {
            'asin': 'TEST123',
            'title': 'Produto de Teste',
            'current_price': 100.0,
            'original_price': 150.0,
            'category': 'Electronics',
            'image_url': 'https://example.com/image.jpg',
            'affiliate_url': 'https://amazon.com.br/test'
        }
        
        db.add_or_update_product(test_product)
        logger.info("✅ Produto de teste adicionado")
        
        deals = db.get_products_with_price_drops(10)
        logger.info(f"✅ Encontradas {len(deals)} ofertas no banco")
        
        return True
    except Exception as e:
        logger.error(f"❌ Erro no banco de dados: {e}")
        return False

def test_full_system():
    logger.info("=== Testando sistema completo ===")
    
    monitor = DealMonitor()
    
    logger.info("Executando varredura de teste...")
    monitor.scan_and_update_products()
    
    stats = monitor.get_statistics()
    logger.info(f"📊 Estatísticas:")
    logger.info(f"  - Total de produtos: {stats['total_products']}")
    logger.info(f"  - Ofertas atuais: {stats['current_deals']}")
    logger.info(f"  - Threshold: {stats['threshold']}%")
    
    if stats['top_deals']:
        logger.info(f"  - Top 3 ofertas:")
        for i, deal in enumerate(stats['top_deals'][:3], 1):
            logger.info(f"    {i}. {deal['title'][:50]} - {deal['discount_percentage']:.1f}% OFF")

def send_test_message():
    logger.info("=== Enviando mensagem de teste ===")
    client = EvolutionAPIClient()
    
    test_products = [{
        'title': 'Produto de Teste - Fone Bluetooth',
        'current_price': 89.90,
        'original_price': 149.90,
        'discount_percentage': 40.0,
        'affiliate_url': 'https://amazon.com.br/test',
        'image_url': 'https://m.media-amazon.com/images/I/test.jpg'
    }]
    
    success = client.send_deals_to_group(test_products)
    
    if success:
        logger.info("✅ Mensagem de teste enviada com sucesso")
    else:
        logger.error("❌ Falha ao enviar mensagem de teste")

if __name__ == "__main__":
    print("\n🔍 TESTE DO SISTEMA DE OFERTAS AMAZON\n")
    
    test_database()
    print()
    
    test_evolution_connection()
    print()
    
    print("\n⚠️  Deseja executar uma varredura completa? (pode demorar)")
    response = input("Digite 'sim' para continuar: ")
    
    if response.lower() == 'sim':
        test_full_system()
    
    print("\n⚠️  Deseja enviar uma mensagem de teste para o grupo?")
    response = input("Digite 'sim' para continuar: ")
    
    if response.lower() == 'sim':
        send_test_message()
    
    print("\n✅ Testes concluídos!")
