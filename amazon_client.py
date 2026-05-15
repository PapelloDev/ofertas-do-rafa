"""
Amazon Creators API - Cliente de Produtos

Cliente para buscar produtos usando a Amazon Creators API.
Implementa SearchItems, GetItems, retry logic e rate limiting.
"""

import requests
import time
import random
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import logging

from amazon_auth import AmazonAuth, AmazonAuthError
import config

logger = logging.getLogger(__name__)


class AmazonAPIError(Exception):
    """Exceção base para erros da API"""
    pass


class ThrottleError(AmazonAPIError):
    """Rate limit excedido"""
    pass


class RateLimiter:
    """
    Rate limiter simples para respeitar TPS da API.
    
    Limites padrão:
    - 1 TPS (Transaction Per Second)
    - 8640 TPD (Transactions Per Day)
    """
    
    def __init__(self, tps: float = 1.0):
        self.tps = tps
        self.min_interval = 1.0 / tps
        self.last_request = 0.0
    
    def wait_if_needed(self):
        """Aguarda se necessário para respeitar rate limit"""
        now = time.time()
        time_since_last = now - self.last_request
        
        if time_since_last < self.min_interval:
            wait_time = self.min_interval - time_since_last
            logger.debug(f"Rate limiting: aguardando {wait_time:.2f}s")
            time.sleep(wait_time)
        
        self.last_request = time.time()


class AmazonClient:
    """
    Cliente para Amazon Creators API.
    
    Implementa:
    - SearchItems (busca de produtos)
    - GetItems (detalhes por ASIN)
    - Retry automático com exponential backoff
    - Rate limiting
    - Cache de resultados
    """
    
    API_BASE_URL = "https://creatorsapi.amazon"
    
    def __init__(
        self,
        credential_id: str = None,
        credential_secret: str = None,
        version: str = None,
        partner_tag: str = None,
        marketplace: str = None,
        tps: float = 1.0
    ):
        """
        Inicializa cliente.
        
        Args:
            credential_id: Client ID (default: config.AMAZON_CREDENTIAL_ID)
            credential_secret: Client Secret (default: config.AMAZON_CREDENTIAL_SECRET)
            version: Versão da credencial (default: config.AMAZON_CREDENTIAL_VERSION)
            partner_tag: Partner Tag (default: config.AMAZON_PARTNER_TAG)
            marketplace: Marketplace (default: config.AMAZON_MARKETPLACE)
            tps: Transactions per second (default: 1.0)
        """
        self.credential_id = credential_id or config.AMAZON_CREDENTIAL_ID
        self.credential_secret = credential_secret or config.AMAZON_CREDENTIAL_SECRET
        self.version = version or config.AMAZON_CREDENTIAL_VERSION
        self.partner_tag = partner_tag or config.AMAZON_PARTNER_TAG
        self.marketplace = marketplace or config.AMAZON_MARKETPLACE
        
        # Autenticação
        self.auth = AmazonAuth(self.credential_id, self.credential_secret, self.version)
        
        # Rate limiting
        self.rate_limiter = RateLimiter(tps)
        
        # Cache simples (em memória)
        self._cache: Dict[str, Dict] = {}
        self._cache_ttl = timedelta(minutes=30)
        
        logger.info(f"AmazonClient inicializado para {self.marketplace}")
    
    def _make_request(
        self,
        operation: str,
        payload: Dict,
        max_retries: int = 3
    ) -> Dict:
        """
        Faz request à API com retry automático.
        
        Args:
            operation: Nome da operação (SearchItems, GetItems, etc)
            payload: Payload da request
            max_retries: Número máximo de tentativas
        
        Returns:
            Response JSON
        
        Raises:
            AmazonAPIError: Erro na API
            ThrottleError: Rate limit excedido
        """
        url = f"{self.API_BASE_URL}/{operation}"
        
        for attempt in range(max_retries):
            try:
                # Rate limiting
                self.rate_limiter.wait_if_needed()
                
                # Headers
                headers = {
                    'Authorization': self.auth.get_auth_header(),
                    'Content-Type': 'application/json',
                    'x-marketplace': self.marketplace
                }
                
                # Request
                logger.debug(f"Request {operation}: {payload}")
                response = requests.post(url, json=payload, headers=headers, timeout=30)
                
                # Success
                if response.status_code == 200:
                    data = response.json()
                    
                    # Verificar erros parciais
                    if 'errors' in data:
                        logger.warning(f"Erros parciais: {data['errors']}")
                    
                    return data
                
                # Rate limit (429)
                if response.status_code == 429:
                    error_data = response.json()
                    retry_after = error_data.get('retryAfterSeconds', 60)
                    
                    if attempt < max_retries - 1:
                        logger.warning(f"Rate limit. Retry após {retry_after}s")
                        time.sleep(retry_after)
                        continue
                    else:
                        raise ThrottleError(f"Rate limit excedido após {max_retries} tentativas")
                
                # Token expirado (401)
                if response.status_code == 401:
                    error_data = response.json()
                    reason = error_data.get('reason')
                    
                    if reason == 'TokenExpired' and attempt < max_retries - 1:
                        logger.info("Token expirado. Renovando...")
                        self.auth.clear_cache()
                        continue
                    else:
                        raise AmazonAPIError(f"Erro de autenticação: {error_data}")
                
                # Server error (500)
                if response.status_code >= 500:
                    if attempt < max_retries - 1:
                        wait_time = (2 ** attempt) + random.uniform(0, 1)
                        logger.warning(f"Erro no servidor. Retry em {wait_time:.1f}s")
                        time.sleep(wait_time)
                        continue
                    else:
                        raise AmazonAPIError(f"Erro no servidor: {response.status_code}")
                
                # Outros erros
                error_data = response.json() if response.text else {}
                raise AmazonAPIError(
                    f"Erro {response.status_code}: {error_data.get('message', response.text)}"
                )
                
            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt) + random.uniform(0, 1)
                    logger.warning(f"Erro de rede. Retry em {wait_time:.1f}s")
                    time.sleep(wait_time)
                    continue
                else:
                    raise AmazonAPIError(f"Erro de rede: {e}")
        
        raise AmazonAPIError(f"Falha após {max_retries} tentativas")
    
    def search_items(
        self,
        keywords: str,
        search_index: str = "All",
        item_count: int = 10,
        min_saving_percent: int = 0,
        min_price: float = None,
        max_price: float = None,
        sort_by: str = None,
        brand: str = None
    ) -> List[Dict]:
        """
        Busca produtos por keywords.
        
        Args:
            keywords: Palavras-chave de busca
            search_index: Categoria (All, Electronics, etc)
            item_count: Número de itens (máx 10)
            min_saving_percent: Desconto mínimo (%)
            min_price: Preço mínimo
            max_price: Preço máximo
            sort_by: Ordenação (Price:LowToHigh, etc)
            brand: Filtro de marca
        
        Returns:
            Lista de produtos
        """
        # Payload
        payload = {
            "partnerTag": self.partner_tag,
            "keywords": keywords,
            "searchIndex": search_index,
            "itemCount": min(item_count, 10),
            "resources": [
                "images.primary.large",
                "itemInfo.title",
                "itemInfo.features",
                "itemInfo.byLineInfo",
                "offersV2.listings.price",
                "offersV2.listings.savingBasis",
                "offersV2.listings.availability",
                "offersV2.listings.dealDetails"
            ]
        }
        
        # Filtros opcionais
        if min_saving_percent:
            payload["minSavingPercent"] = min_saving_percent
        
        if min_price:
            payload["minPrice"] = int(min_price * 100)
        
        if max_price:
            payload["maxPrice"] = int(max_price * 100)
        
        if sort_by:
            payload["sortBy"] = sort_by
        
        if brand:
            payload["brand"] = brand
        
        # Request
        try:
            response = self._make_request("SearchItems", payload)
            
            # Debug: logar resposta completa
            logger.debug(f"Response completa: {response}")
            
            # Extrair produtos
            items = response.get('searchResult', {}).get('items', [])
            
            # Debug: verificar se há erro
            if not items:
                logger.warning(f"Nenhum item retornado. Response keys: {response.keys()}")
                if 'errors' in response:
                    logger.warning(f"Erros: {response['errors']}")
            
            products = [self._parse_item(item) for item in items]
            
            # Filtrar None
            products = [p for p in products if p is not None]
            
            logger.info(f"Encontrados {len(products)} produtos para '{keywords}'")
            return products
            
        except AmazonAPIError as e:
            logger.error(f"Erro ao buscar produtos: {e}")
            return []
    
    def get_items(self, asins: List[str]) -> List[Dict]:
        """
        Busca detalhes de produtos por ASIN.
        
        Args:
            asins: Lista de ASINs (máx 10)
        
        Returns:
            Lista de produtos
        """
        if not asins:
            return []
        
        # Limitar a 10 ASINs
        asins = asins[:10]
        
        # Payload
        payload = {
            "partnerTag": self.partner_tag,
            "itemIds": asins,
            "itemIdType": "ASIN",
            "resources": [
                "images.primary.large",
                "itemInfo.title",
                "itemInfo.features",
                "itemInfo.byLineInfo",
                "offersV2.listings.price",
                "offersV2.listings.savingBasis",
                "offersV2.listings.availability"
            ]
        }
        
        # Request
        try:
            response = self._make_request("GetItems", payload)
            
            # Extrair produtos
            items = response.get('itemsResult', {}).get('items', [])
            products = [self._parse_item(item) for item in items]
            
            # Filtrar None
            products = [p for p in products if p is not None]
            
            logger.info(f"Obtidos {len(products)} produtos de {len(asins)} ASINs")
            return products
            
        except AmazonAPIError as e:
            logger.error(f"Erro ao obter produtos: {e}")
            return []
    
    def _parse_item(self, item: Dict) -> Optional[Dict]:
        """
        Extrai dados relevantes de um item da API.
        
        Args:
            item: Item da resposta da API
        
        Returns:
            Dict com dados do produto ou None
        """
        try:
            asin = item.get('asin')
            if not asin:
                return None
            
            # Título
            title = item.get('itemInfo', {}).get('title', {}).get('displayValue', 'Sem título')
            
            # Marca
            brand = item.get('itemInfo', {}).get('byLineInfo', {}).get('brand', {}).get('displayValue', '')
            
            # Features
            features_obj = item.get('itemInfo', {}).get('features', {})
            features = features_obj.get('displayValues', []) if features_obj else []
            
            # Imagem
            image_url = item.get('images', {}).get('primary', {}).get('large', {}).get('url', '')
            
            # URL de afiliado
            affiliate_url = item.get('detailPageURL', '')
            
            # Ofertas
            listings = item.get('offersV2', {}).get('listings', [])
            if not listings:
                return None
            
            listing = listings[0]
            
            # Preço atual
            price_obj = listing.get('price', {}).get('money', {})
            current_price = price_obj.get('amount')
            currency = price_obj.get('currency', 'BRL')
            
            if not current_price:
                return None
            
            # Preço original (savingBasis)
            saving_basis = listing.get('price', {}).get('savingBasis', {}).get('money', {})
            original_price = saving_basis.get('amount', current_price)
            
            # Desconto
            savings = listing.get('price', {}).get('savings', {})
            discount_amount = savings.get('money', {}).get('amount', 0)
            discount_percent = savings.get('percentage', 0)
            
            # Disponibilidade
            availability = listing.get('availability', {})
            availability_type = availability.get('type', 'UNKNOWN')
            availability_message = availability.get('message', '')
            
            # Deal details
            deal_details = listing.get('dealDetails', {})
            has_deal = bool(deal_details)
            deal_badge = deal_details.get('badge', '') if has_deal else ''
            
            return {
                'asin': asin,
                'title': title,
                'brand': brand,
                'features': features,
                'current_price': current_price,
                'original_price': original_price,
                'discount_amount': discount_amount,
                'discount_percent': discount_percent,
                'currency': currency,
                'image_url': image_url,
                'affiliate_url': affiliate_url,
                'availability_type': availability_type,
                'availability_message': availability_message,
                'in_stock': availability_type == 'IN_STOCK',
                'has_deal': has_deal,
                'deal_badge': deal_badge
            }
            
        except Exception as e:
            logger.error(f"Erro ao parsear item {item.get('asin', 'unknown')}: {e}")
            return None
    
    def search_deals(
        self,
        keywords: str,
        min_discount: int = 20,
        search_index: str = "Electronics",
        max_results: int = 10
    ) -> List[Dict]:
        """
        Busca produtos com desconto.
        
        Args:
            keywords: Palavras-chave
            min_discount: Desconto mínimo (%)
            search_index: Categoria
            max_results: Número máximo de resultados
        
        Returns:
            Lista de produtos com desconto
        """
        products = self.search_items(
            keywords=keywords,
            search_index=search_index,
            item_count=max_results,
            min_saving_percent=min_discount,
            sort_by="Price:LowToHigh"
        )
        
        # Filtrar apenas produtos em estoque
        products = [p for p in products if p.get('in_stock', False)]
        
        # Ordenar por desconto (maior primeiro)
        products.sort(key=lambda x: x.get('discount_percent', 0), reverse=True)
        
        return products
