import logging
from typing import List, Dict
from database import Database
from amazon_client import AmazonClient
from evolution_client import EvolutionAPIClient
import config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DealMonitor:
    def __init__(self):
        self.db = Database()
        self.amazon_client = AmazonClient()
        self.evolution_client = EvolutionAPIClient()
    
    def scan_and_update_products(self):
        """
        Busca produtos tecnológicos mais vendidos com maior desconto.
        Usa múltiplas keywords para encontrar as melhores ofertas.
        """
        logger.info("Iniciando varredura de produtos tecnológicos...")
        
        all_products = []
        
        for keyword in config.SEARCH_KEYWORDS:
            logger.info(f"Buscando: {keyword}")
            try:
                products = self.amazon_client.search_deals(
                    keywords=keyword,
                    min_discount=config.PRICE_DROP_THRESHOLD,
                    search_index="Electronics",
                    max_results=10
                )
                
                all_products.extend(products)
                logger.info(f"  ✅ Encontrados {len(products)} produtos com desconto")
                
            except Exception as e:
                logger.error(f"  ❌ Erro ao buscar '{keyword}': {e}")
                continue
        
        logger.info(f"Total de produtos encontrados: {len(all_products)}")
        
        for product in all_products:
            try:
                self.db.add_or_update_product(product)
            except Exception as e:
                logger.error(f"Erro ao salvar produto {product.get('asin')}: {e}")
        
        logger.info("Varredura concluída")
        return len(all_products)
    
    def check_and_send_deals(self):
        """
        Verifica ofertas no banco de dados e envia para WhatsApp.
        Prioriza produtos com maior desconto que ainda não foram enviados.
        """
        logger.info("Verificando ofertas com quedas de preço...")
        
        deals = self.db.get_products_with_price_drops(config.PRICE_DROP_THRESHOLD)
        
        if not deals:
            logger.info("Nenhuma oferta encontrada no momento")
            return
        
        logger.info(f"Encontradas {len(deals)} ofertas com desconto >= {config.PRICE_DROP_THRESHOLD}%")
        
        top_deals = deals[:config.MAX_PRODUCTS_PER_MESSAGE]
        
        if self.evolution_client.check_connection():
            success = self.evolution_client.send_deals_to_group(top_deals)
            
            if success:
                for deal in top_deals:
                    self.db.mark_deal_as_sent(
                        deal['asin'],
                        deal['current_price'],
                        deal['discount_percentage']
                    )
                logger.info(f"✅ Enviadas {len(top_deals)} ofertas para o grupo")
            else:
                logger.error("❌ Falha ao enviar ofertas")
        else:
            logger.error("❌ Evolution API não está conectada")
    
    def run_full_cycle(self):
        logger.info("=== Iniciando ciclo completo de monitoramento ===")
        
        try:
            self.scan_and_update_products()
            
            self.check_and_send_deals()
            
            logger.info("=== Ciclo completo finalizado ===")
        except Exception as e:
            logger.error(f"Erro durante o ciclo de monitoramento: {e}")
    
    def get_statistics(self) -> Dict:
        all_products = self.db.get_all_products()
        deals = self.db.get_products_with_price_drops(config.PRICE_DROP_THRESHOLD)
        
        return {
            'total_products': len(all_products),
            'current_deals': len(deals),
            'threshold': config.PRICE_DROP_THRESHOLD,
            'top_deals': deals[:5] if deals else []
        }
