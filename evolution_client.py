import requests
import logging
from typing import List, Dict
import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EvolutionAPIClient:
    def __init__(self):
        self.base_url = config.EVOLUTION_API_URL
        self.api_key = config.EVOLUTION_API_KEY
        self.instance_name = config.EVOLUTION_INSTANCE_NAME
        self.headers = {
            'Content-Type': 'application/json',
            'apikey': self.api_key
        }
    
    def send_text_message(self, group_id: str, message: str) -> bool:
        try:
            url = f"{self.base_url}/message/sendText/{self.instance_name}"
            
            payload = {
                'number': group_id,
                'text': message
            }
            
            response = requests.post(url, json=payload, headers=self.headers)
            
            if response.status_code == 200 or response.status_code == 201:
                logger.info(f"Mensagem enviada com sucesso para {group_id}")
                return True
            else:
                logger.error(f"Erro ao enviar mensagem: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            logger.error(f"Exceção ao enviar mensagem: {e}")
            return False
    
    def send_image_message(self, group_id: str, image_url: str, caption: str = '') -> bool:
        try:
            url = f"{self.base_url}/message/sendMedia/{self.instance_name}"
            
            payload = {
                'number': group_id,
                'mediatype': 'image',
                'media': image_url,
                'caption': caption
            }
            
            response = requests.post(url, json=payload, headers=self.headers)
            
            if response.status_code == 200 or response.status_code == 201:
                logger.info(f"Imagem enviada com sucesso para {group_id}")
                return True
            else:
                logger.error(f"Erro ao enviar imagem: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            logger.error(f"Exceção ao enviar imagem: {e}")
            return False
    
    def send_message_with_image(self, group_id: str, message: str, image_url: str) -> bool:
        """Envia mensagem com imagem (imagem com caption)"""
        return self.send_image_message(group_id, image_url, message)
    
    def check_connection(self) -> bool:
        """Verifica se a instância está conectada"""
        try:
            url = f"{self.base_url}/instance/connectionState/{self.instance_name}"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                data = response.json()
                state = data.get('instance', {}).get('state')
                return state == 'open'
            return False
        except Exception as e:
            logger.error(f"Erro ao verificar conexão: {e}")
            return False
    
    def format_single_deal_message(self, product: Dict) -> str:
        discount = product['discount_percentage']
        current_price = product['current_price']
        original_price = product['original_price']
        title = product['title']
        brand = product.get('brand', '')
        
        discount_emoji = "🔥" if discount >= 50 else "💥" if discount >= 30 else "⚡"
        
        message = f"{discount_emoji} *OFERTA IMPERDÍVEL* {discount_emoji}\n\n"
        message += f"📦 *{title}*\n"
        
        if brand:
            message += f"🏷️ Marca: {brand}\n"
        
        message += f"\n💰 De: ~R$ {original_price:.2f}~\n"
        message += f"✅ Por: *R$ {current_price:.2f}*\n"
        message += f"📉 Desconto: *{discount:.0f}% OFF*\n"
        
        economy = original_price - current_price
        message += f"💵 Economia: *R$ {economy:.2f}*\n\n"
        
        message += f"� *Compre agora:*\n{product['affiliate_url']}\n\n"
        message += "⏰ _Oferta por tempo limitado!_\n"
        message += "🤖 _Atualizado automaticamente pelo bot_"
        
        return message
    
    def send_deals_to_group(self, products: List[Dict]) -> bool:
        if not products:
            logger.info("Nenhum produto para enviar")
            return False
        
        group_id = config.WHATSAPP_GROUP_ID
        
        if not group_id:
            logger.error("ID do grupo não configurado")
            return False
        
        import time
        
        products_to_send = products[:config.MAX_PRODUCTS_PER_MESSAGE]
        success_count = 0
        
        logger.info(f"Enviando {len(products_to_send)} produtos individualmente...")
        
        for i, product in enumerate(products_to_send, 1):
            message = self.format_single_deal_message(product)
            
            try:
                if product.get('image_url'):
                    logger.info(f"Enviando produto {i}/{len(products_to_send)} com imagem")
                    success = self.send_image_message(
                        group_id, 
                        product['image_url'],
                        message
                    )
                else:
                    logger.info(f"Enviando produto {i}/{len(products_to_send)} sem imagem")
                    success = self.send_text_message(group_id, message)
                
                if success:
                    success_count += 1
                
                if i < len(products_to_send):
                    time.sleep(2)
                    
            except Exception as e:
                logger.error(f"Erro ao enviar produto {i}: {e}")
                continue
        
        logger.info(f"Enviados {success_count}/{len(products_to_send)} produtos com sucesso")
        return success_count > 0
    
    def check_connection(self) -> bool:
        try:
            url = f"{self.base_url}/instance/connectionState/{self.instance_name}"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                data = response.json()
                state = data.get('instance', {}).get('state', '')
                logger.info(f"Estado da conexão: {state}")
                return state == 'open'
            else:
                logger.error(f"Erro ao verificar conexão: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Exceção ao verificar conexão: {e}")
            return False
