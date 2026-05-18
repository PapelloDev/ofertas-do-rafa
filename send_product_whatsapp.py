#!/usr/bin/env python3
"""
Script para enviar produto para WhatsApp após publicação
"""

import os
import sys
from evolution_client import EvolutionAPIClient
import config

def send_product_to_whatsapp(product_data, product_url):
    """
    Envia notificação do produto para o grupo WhatsApp
    
    Args:
        product_data: Dicionário com dados do produto
        product_url: URL da página do produto no site
    """
    try:
        # Inicializar cliente Evolution
        evolution_client = EvolutionAPIClient()
        
        # Verificar se está conectado
        if not evolution_client.check_connection():
            print("❌ Evolution API não está conectada")
            return False
        
        # Formatar mensagem
        titulo = product_data.get('titulo', 'Produto')
        preco_atual = product_data.get('preco_atual', 0)
        preco_original = product_data.get('preco_original', 0)
        preco_promocional = product_data.get('preco_promocional')
        desconto = product_data.get('desconto_percent', 0)
        brand = product_data.get('brand', '')
        imagem_url = product_data.get('imagem_url', '')
        expiry_date = product_data.get('expiry_date')
        expiry_hours = product_data.get('expiry_hours', 0)
        
        # Verificar se é promoção especial (preço editado manualmente)
        is_special_promo = preco_promocional is not None and preco_promocional > 0
        
        # Emoji baseado no desconto ou promoção especial
        if is_special_promo:
            emoji = "🎉"
            header = "🎉 *PROMOÇÃO ESPECIAL!* 🎉"
        elif desconto >= 50:
            emoji = "🔥"
            header = f"{emoji} *NOVA OFERTA!* {emoji}"
        elif desconto >= 30:
            emoji = "💥"
            header = f"{emoji} *NOVA OFERTA!* {emoji}"
        else:
            emoji = "⚡"
            header = f"{emoji} *NOVA OFERTA!* {emoji}"
        
        # Construir mensagem
        message = f"{header}\n\n"
        
        if is_special_promo:
            message += "⭐ *PREÇO EXCLUSIVO DO RAFA!* ⭐\n\n"
        
        message += f"📦 *{titulo}*\n"
        
        if brand:
            message += f"🏷️ Marca: {brand}\n"
        
        message += f"\n"
        
        if preco_original > preco_atual:
            message += f"💰 De: ~R$ {preco_original:.2f}~\n"
        
        if is_special_promo:
            message += f"✅ Por apenas: *R$ {preco_atual:.2f}* 🎯\n"
        else:
            message += f"✅ Por: *R$ {preco_atual:.2f}*\n"
        
        if desconto > 0:
            message += f"📉 Desconto: *{int(desconto)}% OFF*\n"
            economia = preco_original - preco_atual
            message += f"💵 Economia: *R$ {economia:.2f}*\n"
        
        # Adicionar prazo de validade se existir
        if expiry_date and expiry_hours > 0:
            from datetime import datetime
            expiry_dt = datetime.fromisoformat(expiry_date.replace('Z', '+00:00'))
            
            if expiry_hours < 24:
                prazo_texto = f"{expiry_hours}h"
            elif expiry_hours == 24:
                prazo_texto = "24 horas"
            elif expiry_hours == 48:
                prazo_texto = "2 dias"
            elif expiry_hours == 72:
                prazo_texto = "3 dias"
            elif expiry_hours == 168:
                prazo_texto = "1 semana"
            else:
                dias = expiry_hours // 24
                prazo_texto = f"{dias} dias"
            
            message += f"⏰ Válido por: *{prazo_texto}*\n"
        
        message += f"\n"
        message += f"🔗 *Ver oferta:*\n{product_url}\n\n"
        message += f"_💡 Aproveite enquanto dura!_"
        
        # Enviar mensagem com imagem
        print(f"📤 Enviando para WhatsApp...")
        print(f"   Grupo: {config.WHATSAPP_GROUP_ID}")
        
        success = evolution_client.send_message_with_image(
            config.WHATSAPP_GROUP_ID,
            message,
            imagem_url
        )
        
        if success:
            print(f"✅ Mensagem enviada com sucesso!")
            return True
        else:
            print(f"❌ Falha ao enviar mensagem")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao enviar para WhatsApp: {e}")
        return False

if __name__ == '__main__':
    # Teste
    if len(sys.argv) < 2:
        print("Uso: python send_product_whatsapp.py <ASIN>")
        sys.exit(1)
    
    asin = sys.argv[1]
    
    # Carregar produto do JSON
    import json
    with open('site/data/produtos.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    product = next((p for p in data['produtos'] if p['asin'] == asin), None)
    
    if not product:
        print(f"❌ Produto {asin} não encontrado")
        sys.exit(1)
    
    product_url = f"{data['config']['site_url']}/produto/{asin}.html"
    
    send_product_to_whatsapp(product, product_url)
