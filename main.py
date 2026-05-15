import schedule
import time
import logging
from deal_monitor import DealMonitor
import config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('deal_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    logger.info("Iniciando sistema de monitoramento de ofertas Amazon")
    logger.info(f"Intervalo de verificação: {config.CHECK_INTERVAL_MINUTES} minutos")
    logger.info(f"Threshold de desconto: {config.PRICE_DROP_THRESHOLD}%")
    
    monitor = DealMonitor()
    
    logger.info("Executando primeira varredura...")
    monitor.run_full_cycle()
    
    schedule.every(config.CHECK_INTERVAL_MINUTES).minutes.do(monitor.run_full_cycle)
    
    logger.info("Sistema em execução. Aguardando próximas verificações...")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        logger.info("Sistema encerrado pelo usuário")
    except Exception as e:
        logger.error(f"Erro fatal: {e}")

if __name__ == "__main__":
    main()
