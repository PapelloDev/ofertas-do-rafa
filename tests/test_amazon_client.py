"""
Testes para amazon_client.py
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from amazon_client import (
    AmazonClient,
    AmazonAPIError,
    ThrottleError,
    RateLimiter
)


class TestRateLimiter:
    """Testes para RateLimiter"""
    
    def test_init(self):
        """Deve inicializar com TPS correto"""
        limiter = RateLimiter(tps=2.0)
        assert limiter.tps == 2.0
        assert limiter.min_interval == 0.5
    
    @patch('amazon_client.time.sleep')
    @patch('amazon_client.time.time')
    def test_wait_if_needed_waits(self, mock_time, mock_sleep):
        """Deve aguardar se necessário"""
        limiter = RateLimiter(tps=1.0)
        
        # Simular requests muito rápidos
        mock_time.side_effect = [0.0, 0.3, 0.3]
        limiter.last_request = 0.0
        
        limiter.wait_if_needed()
        
        # Deve ter aguardado ~0.7s (1.0 - 0.3)
        assert mock_sleep.called
    
    @patch('amazon_client.time.sleep')
    @patch('amazon_client.time.time')
    def test_wait_if_needed_no_wait(self, mock_time, mock_sleep):
        """Não deve aguardar se intervalo OK"""
        limiter = RateLimiter(tps=1.0)
        
        # Simular intervalo suficiente (>1s desde última request)
        limiter.last_request = 0.0
        mock_time.return_value = 2.0  # 2s depois
        
        limiter.wait_if_needed()
        
        # Não deve ter aguardado
        assert not mock_sleep.called


class TestAmazonClient:
    """Testes para AmazonClient"""
    
    @patch('amazon_client.AmazonAuth')
    def test_init(self, mock_auth_class):
        """Deve inicializar corretamente"""
        client = AmazonClient(
            credential_id='test_id',
            credential_secret='test_secret',
            version='3.1',
            partner_tag='test-tag',
            marketplace='www.amazon.com.br',
            tps=2.0
        )
        
        assert client.credential_id == 'test_id'
        assert client.partner_tag == 'test-tag'
        assert client.marketplace == 'www.amazon.com.br'
        assert client.rate_limiter.tps == 2.0
    
    @patch('amazon_client.AmazonAuth')
    @patch('amazon_client.requests.post')
    def test_make_request_success(self, mock_post, mock_auth_class):
        """Deve fazer request com sucesso"""
        # Mock auth
        mock_auth = Mock()
        mock_auth.get_auth_header.return_value = "Bearer test_token"
        mock_auth_class.return_value = mock_auth
        
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'searchResult': {'items': []}}
        mock_post.return_value = mock_response
        
        client = AmazonClient('id', 'secret', '3.1', 'tag', 'www.amazon.com.br')
        result = client._make_request('SearchItems', {'keywords': 'test'})
        
        assert result == {'searchResult': {'items': []}}
        mock_post.assert_called_once()
    
    @patch('amazon_client.AmazonAuth')
    @patch('amazon_client.requests.post')
    def test_make_request_partial_errors(self, mock_post, mock_auth_class):
        """Deve logar erros parciais"""
        mock_auth = Mock()
        mock_auth.get_auth_header.return_value = "Bearer test_token"
        mock_auth_class.return_value = mock_auth
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'searchResult': {'items': []},
            'errors': [{'code': 'InvalidASIN', 'message': 'Invalid ASIN'}]
        }
        mock_post.return_value = mock_response
        
        client = AmazonClient('id', 'secret', '3.1', 'tag', 'www.amazon.com.br')
        result = client._make_request('GetItems', {'itemIds': ['INVALID']})
        
        assert 'errors' in result
    
    @patch('amazon_client.AmazonAuth')
    @patch('amazon_client.requests.post')
    @patch('amazon_client.time.sleep')
    def test_make_request_rate_limit_retry(self, mock_sleep, mock_post, mock_auth_class):
        """Deve fazer retry em rate limit"""
        mock_auth = Mock()
        mock_auth.get_auth_header.return_value = "Bearer test_token"
        mock_auth_class.return_value = mock_auth
        
        # Primeira chamada: 429, segunda: 200
        mock_response_429 = Mock()
        mock_response_429.status_code = 429
        mock_response_429.json.return_value = {'retryAfterSeconds': 1}
        
        mock_response_200 = Mock()
        mock_response_200.status_code = 200
        mock_response_200.json.return_value = {'searchResult': {'items': []}}
        
        mock_post.side_effect = [mock_response_429, mock_response_200]
        
        client = AmazonClient('id', 'secret', '3.1', 'tag', 'www.amazon.com.br')
        
        # Mockar rate_limiter para não interferir
        client.rate_limiter.wait_if_needed = Mock()
        
        result = client._make_request('SearchItems', {'keywords': 'test'})
        
        assert result == {'searchResult': {'items': []}}
        assert mock_post.call_count == 2
        # Verificar que sleep foi chamado com 1 (retryAfterSeconds)
        assert any(call[0][0] == 1 for call in mock_sleep.call_args_list)
    
    @patch('amazon_client.AmazonAuth')
    @patch('amazon_client.requests.post')
    def test_make_request_rate_limit_max_retries(self, mock_post, mock_auth_class):
        """Deve lançar ThrottleError após max retries"""
        mock_auth = Mock()
        mock_auth.get_auth_header.return_value = "Bearer test_token"
        mock_auth_class.return_value = mock_auth
        
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.json.return_value = {'retryAfterSeconds': 1}
        mock_post.return_value = mock_response
        
        client = AmazonClient('id', 'secret', '3.1', 'tag', 'www.amazon.com.br')
        
        with pytest.raises(ThrottleError):
            client._make_request('SearchItems', {'keywords': 'test'}, max_retries=2)
    
    @patch('amazon_client.AmazonAuth')
    @patch('amazon_client.requests.post')
    @patch('amazon_client.time.sleep')
    def test_make_request_token_expired_retry(self, mock_sleep, mock_post, mock_auth_class):
        """Deve renovar token e fazer retry"""
        mock_auth = Mock()
        mock_auth.get_auth_header.return_value = "Bearer test_token"
        mock_auth_class.return_value = mock_auth
        
        # Primeira: 401 TokenExpired, segunda: 200
        mock_response_401 = Mock()
        mock_response_401.status_code = 401
        mock_response_401.json.return_value = {'reason': 'TokenExpired'}
        
        mock_response_200 = Mock()
        mock_response_200.status_code = 200
        mock_response_200.json.return_value = {'searchResult': {'items': []}}
        
        mock_post.side_effect = [mock_response_401, mock_response_200]
        
        client = AmazonClient('id', 'secret', '3.1', 'tag', 'www.amazon.com.br')
        result = client._make_request('SearchItems', {'keywords': 'test'})
        
        assert result == {'searchResult': {'items': []}}
        mock_auth.clear_cache.assert_called_once()
    
    @patch('amazon_client.AmazonAuth')
    def test_search_items(self, mock_auth_class):
        """Deve buscar produtos"""
        mock_auth = Mock()
        mock_auth.get_auth_header.return_value = "Bearer test_token"
        mock_auth_class.return_value = mock_auth
        
        client = AmazonClient('id', 'secret', '3.1', 'tag', 'www.amazon.com.br')
        
        # Mock _make_request
        client._make_request = Mock(return_value={
            'searchResult': {
                'items': [
                    {
                        'asin': 'B001',
                        'itemInfo': {'title': {'displayValue': 'Produto 1'}},
                        'offersV2': {
                            'listings': [{
                                'price': {'money': {'amount': 100, 'currency': 'BRL'}}
                            }]
                        }
                    }
                ]
            }
        })
        
        products = client.search_items('fone bluetooth', min_saving_percent=20)
        
        assert len(products) == 1
        assert products[0]['asin'] == 'B001'
        assert products[0]['title'] == 'Produto 1'
    
    @patch('amazon_client.AmazonAuth')
    def test_get_items(self, mock_auth_class):
        """Deve obter produtos por ASIN"""
        mock_auth = Mock()
        mock_auth.get_auth_header.return_value = "Bearer test_token"
        mock_auth_class.return_value = mock_auth
        
        client = AmazonClient('id', 'secret', '3.1', 'tag', 'www.amazon.com.br')
        
        client._make_request = Mock(return_value={
            'itemsResult': {
                'items': [
                    {
                        'asin': 'B001',
                        'itemInfo': {'title': {'displayValue': 'Produto 1'}},
                        'offersV2': {
                            'listings': [{
                                'price': {'money': {'amount': 100, 'currency': 'BRL'}}
                            }]
                        }
                    }
                ]
            }
        })
        
        products = client.get_items(['B001', 'B002'])
        
        assert len(products) == 1
        assert products[0]['asin'] == 'B001'
    
    def test_parse_item_complete(self):
        """Deve parsear item completo"""
        client = AmazonClient('id', 'secret', '3.1', 'tag', 'www.amazon.com.br')
        
        item = {
            'asin': 'B001',
            'itemInfo': {
                'title': {'displayValue': 'Fone JBL'},
                'byLineInfo': {'brand': {'displayValue': 'JBL'}},
                'features': {'displayValues': ['Bluetooth', '40h bateria']}
            },
            'images': {
                'primary': {'large': {'url': 'https://example.com/image.jpg'}}
            },
            'detailPageURL': 'https://amazon.com.br/dp/B001',
            'offersV2': {
                'listings': [{
                    'price': {
                        'money': {'amount': 180, 'currency': 'BRL'},
                        'savingBasis': {'money': {'amount': 300}},
                        'savings': {
                            'money': {'amount': 120},
                            'percentage': 40
                        }
                    },
                    'availability': {
                        'type': 'IN_STOCK',
                        'message': 'Em estoque'
                    },
                    'dealDetails': {
                        'badge': 'Oferta relâmpago'
                    }
                }]
            }
        }
        
        product = client._parse_item(item)
        
        assert product['asin'] == 'B001'
        assert product['title'] == 'Fone JBL'
        assert product['brand'] == 'JBL'
        assert product['current_price'] == 180
        assert product['original_price'] == 300
        assert product['discount_percent'] == 40
        assert product['in_stock'] is True
        assert product['has_deal'] is True
    
    def test_parse_item_no_offers(self):
        """Deve retornar None se sem ofertas"""
        client = AmazonClient('id', 'secret', '3.1', 'tag', 'www.amazon.com.br')
        
        item = {
            'asin': 'B001',
            'itemInfo': {'title': {'displayValue': 'Produto'}},
            'offersV2': {'listings': []}
        }
        
        product = client._parse_item(item)
        assert product is None
    
    @patch('amazon_client.AmazonAuth')
    def test_search_deals(self, mock_auth_class):
        """Deve buscar produtos com desconto"""
        mock_auth = Mock()
        mock_auth_class.return_value = mock_auth
        
        client = AmazonClient('id', 'secret', '3.1', 'tag', 'www.amazon.com.br')
        
        # Mock search_items
        client.search_items = Mock(return_value=[
            {'asin': 'B001', 'discount_percent': 30, 'in_stock': True},
            {'asin': 'B002', 'discount_percent': 50, 'in_stock': True},
            {'asin': 'B003', 'discount_percent': 20, 'in_stock': False}
        ])
        
        deals = client.search_deals('fone', min_discount=20)
        
        # Deve filtrar out_of_stock e ordenar por desconto
        assert len(deals) == 2
        assert deals[0]['discount_percent'] == 50
        assert deals[1]['discount_percent'] == 30
