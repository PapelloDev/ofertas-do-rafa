# 🔍 Amazon Creators API - Exemplos de Requests

Exemplos práticos de como usar a API para diferentes casos de uso.

---

## 🎯 Casos de Uso para o Sistema de Ofertas

### 1. Buscar Produtos Tecnológicos com Desconto

**Objetivo:** Encontrar produtos tech com preços e descontos

**Request:**
```bash
curl -X POST https://creatorsapi.amazon/catalog/v1/searchItems \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN, Version 2.1" \
  -H "Content-Type: application/json" \
  -H "x-marketplace: www.amazon.com.br" \
  -d '{
    "keywords": "fone bluetooth",
    "marketplace": "www.amazon.com.br",
    "partnerTag": "seu-tag-20",
    "itemCount": 10,
    "sortBy": "Relevance",
    "resources": [
      "images.primary.large",
      "itemInfo.title",
      "offersV2.listings.price",
      "offersV2.listings.savingBasis",
      "offersV2.listings.availability"
    ]
  }'
```

**Response Esperada:**
```json
{
  "searchResult": {
    "items": [
      {
        "asin": "B08XYZ123",
        "detailPageURL": "https://www.amazon.com.br/dp/B08XYZ123?tag=seu-tag-20",
        "images": {
          "primary": {
            "large": {
              "url": "https://m.media-amazon.com/images/I/41abc.jpg",
              "height": 500,
              "width": 500
            }
          }
        },
        "itemInfo": {
          "title": {
            "displayValue": "Fone Bluetooth JBL Tune 510BT"
          }
        },
        "offersV2": {
          "listings": [
            {
              "price": {
                "amount": 179.90,
                "currency": "BRL"
              },
              "savingBasis": {
                "amount": 299.00,
                "currency": "BRL"
              },
              "availability": {
                "message": "Em estoque",
                "type": "Now"
              }
            }
          ]
        }
      }
    ],
    "totalResultCount": 1000
  }
}
```

---

### 2. Obter Detalhes de Produtos Específicos (por ASIN)

**Objetivo:** Buscar informações completas de produtos conhecidos

**Request:**
```bash
curl -X POST https://creatorsapi.amazon/catalog/v1/getItems \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN, Version 2.1" \
  -H "Content-Type: application/json" \
  -H "x-marketplace: www.amazon.com.br" \
  -d '{
    "itemIds": ["B08XYZ123", "B09ABC456"],
    "itemIdType": "ASIN",
    "marketplace": "www.amazon.com.br",
    "partnerTag": "seu-tag-20",
    "resources": [
      "images.primary.large",
      "itemInfo.title",
      "itemInfo.features",
      "itemInfo.byLineInfo",
      "offersV2.listings.price",
      "offersV2.listings.savingBasis",
      "browseNodeInfo.browseNodes",
      "customerReviews.starRating"
    ]
  }'
```

---

### 3. Buscar Best Sellers em Categoria

**Objetivo:** Encontrar produtos mais vendidos em eletrônicos

**Request:**
```bash
curl -X POST https://creatorsapi.amazon/catalog/v1/searchItems \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN, Version 2.1" \
  -H "Content-Type: application/json" \
  -H "x-marketplace: www.amazon.com.br" \
  -d '{
    "browseNodeId": "16243663011",
    "marketplace": "www.amazon.com.br",
    "partnerTag": "seu-tag-20",
    "itemCount": 10,
    "sortBy": "AvgCustomerReviews",
    "resources": [
      "images.primary.large",
      "itemInfo.title",
      "offersV2.listings.price",
      "offersV2.listings.savingBasis",
      "customerReviews.starRating"
    ]
  }'
```

---

### 4. Buscar Produtos por Menor Preço

**Objetivo:** Encontrar ofertas ordenadas por preço

**Request:**
```bash
curl -X POST https://creatorsapi.amazon/catalog/v1/searchItems \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN, Version 2.1" \
  -H "Content-Type: application/json" \
  -H "x-marketplace: www.amazon.com.br" \
  -d '{
    "keywords": "smartwatch",
    "marketplace": "www.amazon.com.br",
    "partnerTag": "seu-tag-20",
    "itemCount": 10,
    "sortBy": "Price:LowToHigh",
    "resources": [
      "images.primary.large",
      "itemInfo.title",
      "offersV2.listings.price",
      "offersV2.listings.savingBasis"
    ]
  }'
```

---

## 🔄 Fluxo Completo para o Sistema

### Passo 1: Autenticação

```python
import requests
import base64
from datetime import datetime, timedelta

class AmazonAuth:
    def __init__(self, client_id, client_secret, version):
        self.client_id = client_id
        self.client_secret = client_secret
        self.version = version
        self.token = None
        self.token_expires_at = None
    
    def get_token_endpoint(self):
        """Retorna endpoint baseado na versão"""
        version_map = {
            '2.1': 'https://creatorsapi.auth.us-east-1.amazoncognito.com/oauth2/token',
            '2.2': 'https://creatorsapi.auth.eu-south-2.amazoncognito.com/oauth2/token',
            '2.3': 'https://creatorsapi.auth.us-west-2.amazoncognito.com/oauth2/token',
            '3.1': 'https://api.amazon.com/auth/o2/token',
            '3.2': 'https://api.amazon.co.uk/auth/o2/token',
            '3.3': 'https://api.amazon.co.jp/auth/o2/token'
        }
        return version_map.get(self.version)
    
    def fetch_token(self):
        """Obtém novo access token"""
        endpoint = self.get_token_endpoint()
        
        if self.version.startswith('2.'):
            # v2.x - Cognito
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            data = {
                'grant_type': 'client_credentials',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'scope': 'creatorsapi/default'
            }
            response = requests.post(endpoint, headers=headers, data=data)
        else:
            # v3.x - LwA
            headers = {
                'Content-Type': 'application/json'
            }
            data = {
                'grant_type': 'client_credentials',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'scope': 'creatorsapi::default'
            }
            response = requests.post(endpoint, headers=headers, json=data)
        
        if response.status_code == 200:
            result = response.json()
            self.token = result['access_token']
            expires_in = result['expires_in']
            self.token_expires_at = datetime.now() + timedelta(seconds=expires_in - 60)
            return self.token
        else:
            raise Exception(f"Erro ao obter token: {response.status_code} - {response.text}")
    
    def get_valid_token(self):
        """Retorna token válido (cached ou novo)"""
        if self.token is None or datetime.now() >= self.token_expires_at:
            return self.fetch_token()
        return self.token
```

### Passo 2: Buscar Produtos

```python
class AmazonProductSearch:
    def __init__(self, auth, partner_tag, marketplace='www.amazon.com.br'):
        self.auth = auth
        self.partner_tag = partner_tag
        self.marketplace = marketplace
        self.base_url = 'https://creatorsapi.amazon'
    
    def get_headers(self):
        """Gera headers para requests"""
        token = self.auth.get_valid_token()
        
        if self.auth.version.startswith('2.'):
            auth_header = f"Bearer {token}, Version {self.auth.version}"
        else:
            auth_header = f"Bearer {token}"
        
        return {
            'Authorization': auth_header,
            'Content-Type': 'application/json',
            'x-marketplace': self.marketplace
        }
    
    def search_items(self, keywords, item_count=10, sort_by='Relevance'):
        """Busca produtos por palavra-chave"""
        url = f"{self.base_url}/catalog/v1/searchItems"
        
        payload = {
            'keywords': keywords,
            'marketplace': self.marketplace,
            'partnerTag': self.partner_tag,
            'itemCount': item_count,
            'sortBy': sort_by,
            'resources': [
                'images.primary.large',
                'itemInfo.title',
                'offersV2.listings.price',
                'offersV2.listings.savingBasis',
                'offersV2.listings.availability'
            ]
        }
        
        response = requests.post(url, headers=self.get_headers(), json=payload)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Erro na busca: {response.status_code} - {response.text}")
    
    def get_items(self, asins):
        """Obtém detalhes de produtos específicos"""
        url = f"{self.base_url}/catalog/v1/getItems"
        
        payload = {
            'itemIds': asins,
            'itemIdType': 'ASIN',
            'marketplace': self.marketplace,
            'partnerTag': self.partner_tag,
            'resources': [
                'images.primary.large',
                'itemInfo.title',
                'itemInfo.features',
                'offersV2.listings.price',
                'offersV2.listings.savingBasis',
                'browseNodeInfo.browseNodes'
            ]
        }
        
        response = requests.post(url, headers=self.get_headers(), json=payload)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Erro ao obter items: {response.status_code} - {response.text}")
```

### Passo 3: Processar Resultados

```python
def extract_product_data(item):
    """Extrai dados relevantes do produto"""
    
    # Preço atual
    current_price = None
    original_price = None
    
    if 'offersV2' in item and item['offersV2']:
        listings = item['offersV2'].get('listings', [])
        if listings:
            listing = listings[0]
            
            if 'price' in listing:
                current_price = listing['price']['amount']
            
            if 'savingBasis' in listing:
                original_price = listing['savingBasis']['amount']
    
    # Se não tem preço original, usa o atual
    if original_price is None and current_price:
        original_price = current_price
    
    # Calcular desconto
    discount_percentage = 0
    if original_price and current_price and original_price > current_price:
        discount_percentage = ((original_price - current_price) / original_price) * 100
    
    # Imagem
    image_url = ''
    if 'images' in item and item['images']:
        primary = item['images'].get('primary', {})
        large = primary.get('large', {})
        image_url = large.get('url', '')
    
    # Título
    title = ''
    if 'itemInfo' in item and item['itemInfo']:
        title_obj = item['itemInfo'].get('title', {})
        title = title_obj.get('displayValue', '')
    
    return {
        'asin': item.get('asin'),
        'title': title,
        'current_price': current_price,
        'original_price': original_price,
        'discount_percentage': discount_percentage,
        'image_url': image_url,
        'affiliate_url': item.get('detailPageURL', '')
    }
```

---

## 📊 Exemplo Completo de Uso

```python
# Inicializar autenticação
auth = AmazonAuth(
    client_id='amzn1.application-oa2-client.xxxxx',
    client_secret='your_secret_here',
    version='2.1'
)

# Inicializar busca
search = AmazonProductSearch(
    auth=auth,
    partner_tag='seu-tag-20',
    marketplace='www.amazon.com.br'
)

# Buscar produtos
keywords = ['fone bluetooth', 'smartwatch', 'mouse gamer']

all_products = []

for keyword in keywords:
    print(f"Buscando: {keyword}")
    result = search.search_items(keyword, item_count=10)
    
    if 'searchResult' in result:
        items = result['searchResult'].get('items', [])
        
        for item in items:
            product = extract_product_data(item)
            
            # Filtrar apenas produtos com desconto >= 10%
            if product['discount_percentage'] >= 10:
                all_products.append(product)
                print(f"  ✅ {product['title'][:50]} - {product['discount_percentage']:.1f}% OFF")

print(f"\nTotal de produtos com desconto: {len(all_products)}")
```

---

## 🎯 Keywords Recomendadas para Gadgets Tech

```python
TECH_KEYWORDS = [
    # Áudio
    'fone bluetooth',
    'fone de ouvido',
    'airpods',
    'jbl',
    'soundbar',
    
    # Smartphones e Acessórios
    'smartphone',
    'carregador rápido',
    'power bank',
    'cabo usb-c',
    'película de vidro',
    
    # Wearables
    'smartwatch',
    'smart band',
    'relógio inteligente',
    
    # Computação
    'mouse gamer',
    'teclado mecânico',
    'webcam',
    'headset gamer',
    'ssd',
    'hd externo',
    
    # Casa Inteligente
    'alexa',
    'echo dot',
    'lâmpada inteligente',
    'tomada inteligente',
    'câmera segurança',
    
    # Streaming
    'chromecast',
    'fire tv stick',
    'roku',
    
    # Outros
    'tablet',
    'kindle',
    'ring light',
    'tripé celular'
]
```

---

**Última atualização:** 14 de Maio de 2026
