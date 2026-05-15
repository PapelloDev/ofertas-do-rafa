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
        desconto = product_data.get('desconto_percent', 0)
        brand = product_data.get('brand', '')
        imagem_url = product_data.get('imagem_url', '')
        
        # Emoji baseado no desconto
        if desconto >= 50:
            emoji = "🔥"
        elif desconto >= 30:
            emoji = "💥"
        else:
            emoji = "⚡"
        
        # Construir mensagem
        message = f"{emoji} *NOVA OFERTA!* {emoji}\n\n"
        message += f"📦 *{titulo}*\n"
        
        if brand:
            message += f"🏷️ Marca: {brand}\n"
        
        message += f"\n"
        
        if preco_original > preco_atual:
            message += f"💰 De: ~R$ {preco_original:.2f}~\n"
        
        message += f"✅ Por: *R$ {preco_atual:.2f}*\n"
        
        if desconto > 0:
            message += f"📉 Desconto: *{int(desconto)}% OFF*\n"
            economia = preco_original - preco_atual
            message += f"💵 Economia: *R$ {economia:.2f}*\n"
        
        message += f"\n"
        message += f"👉 *Ver oferta completa:*\n{product_url}\n\n"
        message += f"⏰ _Oferta por tempo limitado!_\n"
        message += f"🤖 _Atualizado automaticamente_"
        
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
