"""
Amazon Creators API - Autenticação e Gerenciamento de Token

Este módulo gerencia a autenticação com a Amazon Creators API,
incluindo cache de token e tratamento de erros.
"""

import requests
from datetime import datetime, timedelta
from typing import Optional, Dict
import logging

logger = logging.getLogger(__name__)


class AmazonAuthError(Exception):
    """Exceção base para erros de autenticação"""
    pass


class TokenExpiredError(AmazonAuthError):
    """Token expirado"""
    pass


class InvalidCredentialsError(AmazonAuthError):
    """Credenciais inválidas"""
    pass


class RateLimitError(AmazonAuthError):
    """Rate limit do endpoint de token excedido"""
    pass


class AmazonAuth:
    """
    Gerencia autenticação com Amazon Creators API.
    
    Implementa cache de token para evitar rate limiting do endpoint de token.
    Tokens são válidos por 1 hora e devem ser reutilizados.
    """
    
    # Endpoints de token por versão
    TOKEN_ENDPOINTS = {
        '2.1': 'https://creatorsapi.auth.us-east-1.amazoncognito.com/oauth2/token',
        '2.2': 'https://creatorsapi.auth.eu-south-2.amazoncognito.com/oauth2/token',
        '2.3': 'https://creatorsapi.auth.us-west-2.amazoncognito.com/oauth2/token',
        '3.1': 'https://api.amazon.com/auth/o2/token',
        '3.2': 'https://api.amazon.co.uk/auth/o2/token',
        '3.3': 'https://api.amazon.co.jp/auth/o2/token'
    }
    
    def __init__(self, credential_id: str, credential_secret: str, version: str = '2.1'):
        """
        Inicializa autenticação.
        
        Args:
            credential_id: Client ID da credencial
            credential_secret: Client Secret da credencial
            version: Versão da credencial (2.1, 2.2, 2.3, 3.1, 3.2, 3.3)
        
        Raises:
            ValueError: Se versão não for suportada
        """
        if version not in self.TOKEN_ENDPOINTS:
            raise ValueError(
                f"Versão {version} não suportada. "
                f"Versões válidas: {', '.join(self.TOKEN_ENDPOINTS.keys())}"
            )
        
        self.credential_id = credential_id
        self.credential_secret = credential_secret
        self.version = version
        
        # Cache de token
        self._token: Optional[str] = None
        self._token_expires_at: Optional[datetime] = None
        
        logger.info(f"AmazonAuth inicializado com versão {version}")
    
    def _get_token_endpoint(self) -> str:
        """Retorna endpoint de token baseado na versão."""
        return self.TOKEN_ENDPOINTS[self.version]
    
    def _is_v2(self) -> bool:
        """Verifica se é versão 2.x (Cognito)."""
        return self.version.startswith('2.')
    
    def _fetch_new_token(self) -> Dict:
        """
        Busca novo access token do endpoint.
        
        Returns:
            Dict com 'access_token' e 'expires_in'
        
        Raises:
            InvalidCredentialsError: Credenciais inválidas
            RateLimitError: Rate limit excedido
            AmazonAuthError: Outros erros
        """
        endpoint = self._get_token_endpoint()
        
        try:
            if self._is_v2():
                # v2.x - Cognito (application/x-www-form-urlencoded)
                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
                data = {
                    'grant_type': 'client_credentials',
                    'client_id': self.credential_id,
                    'client_secret': self.credential_secret,
                    'scope': 'creatorsapi/default'
                }
                response = requests.post(endpoint, headers=headers, data=data, timeout=10)
            else:
                # v3.x - LwA (application/json)
                headers = {
                    'Content-Type': 'application/json'
                }
                data = {
                    'grant_type': 'client_credentials',
                    'client_id': self.credential_id,
                    'client_secret': self.credential_secret,
                    'scope': 'creatorsapi::default'
                }
                response = requests.post(endpoint, headers=headers, json=data, timeout=10)
            
            # Rate limit do endpoint de token
            if response.status_code == 429:
                retry_after = response.headers.get('Retry-After', '300')
                logger.error(f"Token endpoint rate limit. Retry after {retry_after}s")
                raise RateLimitError(
                    f"Rate limit do endpoint de token excedido. "
                    f"Aguarde {retry_after} segundos. "
                    f"IMPORTANTE: Tokens devem ser cacheados por 1 hora!"
                )
            
            # Credenciais inválidas
            if response.status_code in (400, 401, 403):
                error_data = response.json() if response.text else {}
                error_msg = error_data.get('error_description', response.text)
                logger.error(f"Credenciais inválidas: {error_msg}")
                raise InvalidCredentialsError(f"Credenciais inválidas: {error_msg}")
            
            # Outros erros
            if response.status_code != 200:
                logger.error(f"Erro ao obter token: {response.status_code} - {response.text}")
                raise AmazonAuthError(
                    f"Erro ao obter token: {response.status_code} - {response.text}"
                )
            
            result = response.json()
            logger.info("Token obtido com sucesso")
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro de rede ao obter token: {e}")
            raise AmazonAuthError(f"Erro de rede: {e}")
    
    def get_valid_token(self) -> str:
        """
        Retorna token válido (cached ou novo).
        
        Implementa cache automático de token por 1 hora.
        Renova automaticamente se expirado.
        
        Returns:
            Access token válido
        
        Raises:
            InvalidCredentialsError: Credenciais inválidas
            RateLimitError: Rate limit excedido
            AmazonAuthError: Outros erros
        """
        # Verificar se token em cache ainda é válido
        if self._token and self._token_expires_at:
            # Renovar 1 minuto antes de expirar (margem de segurança)
            if datetime.now() < self._token_expires_at - timedelta(minutes=1):
                logger.debug("Usando token em cache")
                return self._token
        
        # Buscar novo token
        logger.info("Token expirado ou ausente. Buscando novo token...")
        token_data = self._fetch_new_token()
        
        self._token = token_data['access_token']
        expires_in = token_data['expires_in']  # Segundos (geralmente 3600 = 1 hora)
        self._token_expires_at = datetime.now() + timedelta(seconds=expires_in)
        
        logger.info(f"Novo token válido até {self._token_expires_at.strftime('%H:%M:%S')}")
        return self._token
    
    def get_auth_header(self) -> str:
        """
        Retorna valor do Authorization header.
        
        Returns:
            String formatada para o header Authorization
        
        Example:
            v2.x: "Bearer eyJraWQiOiJ..., Version 2.1"
            v3.x: "Bearer Atc|MQICIJvS..."
        """
        token = self.get_valid_token()
        
        if self._is_v2():
            return f"Bearer {token}, Version {self.version}"
        else:
            return f"Bearer {token}"
    
    def validate_credentials(self) -> Dict:
        """
        Valida credenciais tentando obter um token.
        
        Returns:
            Dict com informações de validação:
            {
                'valid': bool,
                'version': str,
                'expires_in': int,
                'error': str (se invalid)
            }
        """
        try:
            token_data = self._fetch_new_token()
            return {
                'valid': True,
                'version': self.version,
                'expires_in': token_data['expires_in'],
                'token_type': 'Cognito' if self._is_v2() else 'LwA'
            }
        except InvalidCredentialsError as e:
            return {
                'valid': False,
                'version': self.version,
                'error': str(e)
            }
        except RateLimitError as e:
            return {
                'valid': False,
                'version': self.version,
                'error': str(e)
            }
        except AmazonAuthError as e:
            return {
                'valid': False,
                'version': self.version,
                'error': str(e)
            }
    
    def clear_cache(self):
        """Limpa cache de token (útil para testes)."""
        self._token = None
        self._token_expires_at = None
        logger.info("Cache de token limpo")
