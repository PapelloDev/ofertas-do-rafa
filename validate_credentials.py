#!/usr/bin/env python3
"""
Script de validação de credenciais Amazon Creators API

Valida se as credenciais no .env estão corretas e funcionando.
"""

import os
import sys
from dotenv import load_dotenv
from amazon_auth import AmazonAuth, InvalidCredentialsError, RateLimitError

# Cores para output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'


def print_header():
    """Imprime cabeçalho"""
    print(f"\n{BLUE}{'='*60}")
    print("  Amazon Creators API - Validação de Credenciais")
    print(f"{'='*60}{RESET}\n")


def print_success(message):
    """Imprime mensagem de sucesso"""
    print(f"{GREEN}✓ {message}{RESET}")


def print_error(message):
    """Imprime mensagem de erro"""
    print(f"{RED}✗ {message}{RESET}")


def print_warning(message):
    """Imprime mensagem de aviso"""
    print(f"{YELLOW}⚠ {message}{RESET}")


def print_info(message):
    """Imprime mensagem informativa"""
    print(f"{BLUE}ℹ {message}{RESET}")


def load_credentials():
    """
    Carrega credenciais do .env
    
    Returns:
        Tuple (credential_id, credential_secret, version, partner_tag, marketplace)
    """
    load_dotenv()
    
    credential_id = os.getenv('AMAZON_CREDENTIAL_ID')
    credential_secret = os.getenv('AMAZON_CREDENTIAL_SECRET')
    version = os.getenv('AMAZON_CREDENTIAL_VERSION', '2.1')
    partner_tag = os.getenv('AMAZON_PARTNER_TAG')
    marketplace = os.getenv('AMAZON_MARKETPLACE', 'www.amazon.com.br')
    
    return credential_id, credential_secret, version, partner_tag, marketplace


def validate_env_vars(credential_id, credential_secret, partner_tag):
    """
    Valida se variáveis de ambiente estão configuradas
    
    Returns:
        bool: True se todas configuradas
    """
    print_info("Verificando variáveis de ambiente...")
    
    all_valid = True
    
    if not credential_id or credential_id == 'your_credential_id':
        print_error("AMAZON_CREDENTIAL_ID não configurado")
        all_valid = False
    else:
        print_success(f"AMAZON_CREDENTIAL_ID: {credential_id[:20]}...")
    
    if not credential_secret or credential_secret == 'your_credential_secret':
        print_error("AMAZON_CREDENTIAL_SECRET não configurado")
        all_valid = False
    else:
        print_success(f"AMAZON_CREDENTIAL_SECRET: {'*' * 20}")
    
    if not partner_tag or partner_tag == 'your_partner_tag':
        print_error("AMAZON_PARTNER_TAG não configurado")
        all_valid = False
    else:
        print_success(f"AMAZON_PARTNER_TAG: {partner_tag}")
    
    return all_valid


def validate_credentials_api(credential_id, credential_secret, version):
    """
    Valida credenciais fazendo request à API
    
    Returns:
        bool: True se válidas
    """
    print_info(f"\nValidando credenciais com Amazon (versão {version})...")
    
    try:
        auth = AmazonAuth(credential_id, credential_secret, version)
        result = auth.validate_credentials()
        
        if result['valid']:
            print_success("Credenciais válidas!")
            print_info(f"  Tipo de token: {result['token_type']}")
            print_info(f"  Validade: {result['expires_in']} segundos (1 hora)")
            return True
        else:
            print_error(f"Credenciais inválidas: {result.get('error', 'Erro desconhecido')}")
            return False
            
    except ValueError as e:
        print_error(f"Erro de configuração: {e}")
        return False
    except Exception as e:
        print_error(f"Erro inesperado: {e}")
        return False


def print_next_steps(all_valid):
    """Imprime próximos passos"""
    print(f"\n{BLUE}{'='*60}")
    print("  Próximos Passos")
    print(f"{'='*60}{RESET}\n")
    
    if all_valid:
        print_success("Todas as validações passaram!")
        print_info("\nVocê pode agora:")
        print("  1. Executar os testes: ./test.sh")
        print("  2. Iniciar o sistema: ./start.sh")
        print("  3. Testar busca de produtos manualmente")
    else:
        print_error("Algumas validações falharam.")
        print_info("\nPara corrigir:")
        print("  1. Edite o arquivo .env com suas credenciais")
        print("  2. Obtenha credenciais em: https://associados.amazon.com.br/creatorsapi")
        print("  3. Execute novamente: python validate_credentials.py")


def main():
    """Função principal"""
    print_header()
    
    # Carregar credenciais
    credential_id, credential_secret, version, partner_tag, marketplace = load_credentials()
    
    # Validar variáveis de ambiente
    env_valid = validate_env_vars(credential_id, credential_secret, partner_tag)
    
    if not env_valid:
        print_warning("\nConfigure as variáveis de ambiente antes de continuar.")
        print_next_steps(False)
        return 1
    
    # Validar credenciais com API
    api_valid = validate_credentials_api(credential_id, credential_secret, version)
    
    # Resumo
    all_valid = env_valid and api_valid
    print_next_steps(all_valid)
    
    return 0 if all_valid else 1


if __name__ == '__main__':
    sys.exit(main())
