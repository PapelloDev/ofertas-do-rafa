"""
Testes para amazon_auth.py
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
from amazon_auth import (
    AmazonAuth,
    AmazonAuthError,
    InvalidCredentialsError,
    RateLimitError,
    TokenExpiredError
)


class TestAmazonAuth:
    """Testes para classe AmazonAuth"""
    
    def test_init_valid_version(self):
        """Deve inicializar com versão válida"""
        auth = AmazonAuth('client_id', 'secret', '2.1')
        assert auth.version == '2.1'
        assert auth.credential_id == 'client_id'
        assert auth.credential_secret == 'secret'
    
    def test_init_invalid_version(self):
        """Deve rejeitar versão inválida"""
        with pytest.raises(ValueError, match="não suportada"):
            AmazonAuth('client_id', 'secret', '9.9')
    
    def test_get_token_endpoint_v2(self):
        """Deve retornar endpoint correto para v2.x"""
        auth = AmazonAuth('client_id', 'secret', '2.1')
        endpoint = auth._get_token_endpoint()
        assert 'amazoncognito.com' in endpoint
    
    def test_get_token_endpoint_v3(self):
        """Deve retornar endpoint correto para v3.x"""
        auth = AmazonAuth('client_id', 'secret', '3.1')
        endpoint = auth._get_token_endpoint()
        assert 'api.amazon.com' in endpoint
    
    def test_is_v2(self):
        """Deve identificar versão 2.x corretamente"""
        auth_v2 = AmazonAuth('client_id', 'secret', '2.1')
        auth_v3 = AmazonAuth('client_id', 'secret', '3.1')
        
        assert auth_v2._is_v2() is True
        assert auth_v3._is_v2() is False
    
    @patch('amazon_auth.requests.post')
    def test_fetch_new_token_success_v2(self, mock_post):
        """Deve obter token com sucesso (v2.x)"""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'access_token': 'test_token_123',
            'expires_in': 3600
        }
        mock_post.return_value = mock_response
        
        auth = AmazonAuth('client_id', 'secret', '2.1')
        result = auth._fetch_new_token()
        
        assert result['access_token'] == 'test_token_123'
        assert result['expires_in'] == 3600
        
        # Verificar chamada
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        assert call_args[1]['data']['grant_type'] == 'client_credentials'
        assert call_args[1]['data']['scope'] == 'creatorsapi/default'
    
    @patch('amazon_auth.requests.post')
    def test_fetch_new_token_success_v3(self, mock_post):
        """Deve obter token com sucesso (v3.x)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'access_token': 'test_token_456',
            'expires_in': 3600
        }
        mock_post.return_value = mock_response
        
        auth = AmazonAuth('client_id', 'secret', '3.1')
        result = auth._fetch_new_token()
        
        assert result['access_token'] == 'test_token_456'
        
        # Verificar que usou JSON (não form data)
        call_args = mock_post.call_args
        assert 'json' in call_args[1]
        assert call_args[1]['json']['scope'] == 'creatorsapi::default'
    
    @patch('amazon_auth.requests.post')
    def test_fetch_new_token_invalid_credentials(self, mock_post):
        """Deve lançar InvalidCredentialsError para credenciais inválidas"""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = 'Invalid credentials'
        mock_response.json.return_value = {
            'error_description': 'Invalid client credentials'
        }
        mock_post.return_value = mock_response
        
        auth = AmazonAuth('bad_id', 'bad_secret', '2.1')
        
        with pytest.raises(InvalidCredentialsError, match="Credenciais inválidas"):
            auth._fetch_new_token()
    
    @patch('amazon_auth.requests.post')
    def test_fetch_new_token_rate_limit(self, mock_post):
        """Deve lançar RateLimitError quando rate limit excedido"""
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.headers = {'Retry-After': '300'}
        mock_post.return_value = mock_response
        
        auth = AmazonAuth('client_id', 'secret', '2.1')
        
        with pytest.raises(RateLimitError, match="Rate limit"):
            auth._fetch_new_token()
    
    @patch('amazon_auth.requests.post')
    def test_get_valid_token_caches(self, mock_post):
        """Deve cachear token e não buscar novamente"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'access_token': 'cached_token',
            'expires_in': 3600
        }
        mock_post.return_value = mock_response
        
        auth = AmazonAuth('client_id', 'secret', '2.1')
        
        # Primeira chamada - busca token
        token1 = auth.get_valid_token()
        assert token1 == 'cached_token'
        assert mock_post.call_count == 1
        
        # Segunda chamada - usa cache
        token2 = auth.get_valid_token()
        assert token2 == 'cached_token'
        assert mock_post.call_count == 1  # Não chamou novamente
    
    @patch('amazon_auth.requests.post')
    def test_get_valid_token_renews_when_expired(self, mock_post):
        """Deve renovar token quando expirado"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'access_token': 'new_token',
            'expires_in': 3600
        }
        mock_post.return_value = mock_response
        
        auth = AmazonAuth('client_id', 'secret', '2.1')
        
        # Simular token expirado
        auth._token = 'old_token'
        auth._token_expires_at = datetime.now() - timedelta(hours=1)
        
        token = auth.get_valid_token()
        
        assert token == 'new_token'
        assert mock_post.call_count == 1
    
    def test_get_auth_header_v2(self):
        """Deve formatar header corretamente para v2.x"""
        auth = AmazonAuth('client_id', 'secret', '2.1')
        auth._token = 'test_token'
        auth._token_expires_at = datetime.now() + timedelta(hours=1)
        
        header = auth.get_auth_header()
        
        assert header == "Bearer test_token, Version 2.1"
    
    def test_get_auth_header_v3(self):
        """Deve formatar header corretamente para v3.x"""
        auth = AmazonAuth('client_id', 'secret', '3.1')
        auth._token = 'test_token'
        auth._token_expires_at = datetime.now() + timedelta(hours=1)
        
        header = auth.get_auth_header()
        
        assert header == "Bearer test_token"
    
    @patch('amazon_auth.requests.post')
    def test_validate_credentials_success(self, mock_post):
        """Deve validar credenciais com sucesso"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'access_token': 'valid_token',
            'expires_in': 3600
        }
        mock_post.return_value = mock_response
        
        auth = AmazonAuth('client_id', 'secret', '2.1')
        result = auth.validate_credentials()
        
        assert result['valid'] is True
        assert result['version'] == '2.1'
        assert result['expires_in'] == 3600
        assert result['token_type'] == 'Cognito'
    
    @patch('amazon_auth.requests.post')
    def test_validate_credentials_failure(self, mock_post):
        """Deve retornar erro ao validar credenciais inválidas"""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = 'Invalid'
        mock_response.json.return_value = {'error_description': 'Bad credentials'}
        mock_post.return_value = mock_response
        
        auth = AmazonAuth('bad_id', 'bad_secret', '2.1')
        result = auth.validate_credentials()
        
        assert result['valid'] is False
        assert 'error' in result
    
    def test_clear_cache(self):
        """Deve limpar cache de token"""
        auth = AmazonAuth('client_id', 'secret', '2.1')
        auth._token = 'test_token'
        auth._token_expires_at = datetime.now() + timedelta(hours=1)
        
        auth.clear_cache()
        
        assert auth._token is None
        assert auth._token_expires_at is None
