import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

EVOLUTION_API_URL = os.getenv('EVOLUTION_API_URL', 'http://localhost:8080')
EVOLUTION_API_KEY = os.getenv('EVOLUTION_API_KEY')
EVOLUTION_INSTANCE_NAME = os.getenv('EVOLUTION_INSTANCE_NAME')

def list_all_chats():
    """Lista todos os chats incluindo grupos"""
    url = f"{EVOLUTION_API_URL}/chat/findChats/{EVOLUTION_INSTANCE_NAME}"
    headers = {
        'apikey': EVOLUTION_API_KEY,
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(url, json={}, headers=headers)
        
        if response.status_code == 200:
            chats = response.json()
            
            print("\n" + "="*80)
            print("📱 GRUPOS DO WHATSAPP ENCONTRADOS")
            print("="*80 + "\n")
            
            groups = [chat for chat in chats if chat.get('remoteJid', '').endswith('@g.us')]
            
            if not groups:
                print("❌ Nenhum grupo encontrado.\n")
                return
            
            for i, group in enumerate(groups, 1):
                group_id = group.get('remoteJid', 'N/A')
                group_name = group.get('pushName', 'Sem nome')
                
                print(f"{i}. Nome: {group_name}")
                print(f"   ID: {group_id}")
                print(f"   Copie este ID para o arquivo .env:")
                print(f"   WHATSAPP_GROUP_ID={group_id}")
                print("-" * 80)
            
            print(f"\n✅ Total de grupos encontrados: {len(groups)}\n")
            
        else:
            print(f"❌ Erro ao listar chats: {response.status_code}")
            print(f"Resposta: {response.text}")
    
    except Exception as e:
        print(f"❌ Erro ao conectar com Evolution API: {e}")
        print("\nVerifique se:")
        print("1. A Evolution API está rodando")
        print("2. A instância está conectada")
        print("3. As credenciais no .env estão corretas")

def check_instance_status():
    """Verifica se a instância está conectada"""
    url = f"{EVOLUTION_API_URL}/instance/connectionState/{EVOLUTION_INSTANCE_NAME}"
    headers = {'apikey': EVOLUTION_API_KEY}
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            state = data.get('instance', {}).get('state', 'unknown')
            
            print("\n" + "="*80)
            print("🔌 STATUS DA INSTÂNCIA")
            print("="*80)
            print(f"Instância: {EVOLUTION_INSTANCE_NAME}")
            print(f"Estado: {state}")
            
            if state == 'open':
                print("✅ Instância conectada e pronta para uso!\n")
                return True
            else:
                print("⚠️  Instância não está conectada.")
                print("   Execute: python connect_instance.py\n")
                return False
        else:
            print(f"❌ Erro ao verificar status: {response.status_code}")
            return False
    
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    print("\n🔍 BUSCANDO GRUPOS DO WHATSAPP\n")
    
    if not EVOLUTION_API_KEY or not EVOLUTION_INSTANCE_NAME:
        print("❌ Erro: Configure o arquivo .env primeiro!")
        print("\nCopie o .env.example para .env e preencha:")
        print("- EVOLUTION_API_KEY")
        print("- EVOLUTION_INSTANCE_NAME")
        exit(1)
    
    if check_instance_status():
        list_all_chats()
    else:
        print("\n⚠️  Não foi possível listar os grupos porque a instância não está conectada.")
