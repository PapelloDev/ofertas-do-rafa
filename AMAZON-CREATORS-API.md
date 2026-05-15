# 📚 Amazon Creators API - Documentação Completa

Documentação resumida da Amazon Creators API para referência do sistema.

---

## 🔑 Credenciais

### Formato das Credenciais

As credenciais da Creators API têm o seguinte formato:

| Campo | Descrição |
|-------|-----------|
| **Application** | Nome da aplicação |
| **Application Id** | ID da aplicação (não usado diretamente) |
| **Credential Id** | Client ID (usado para autenticação) |
| **Secret** | Client Secret (usado para autenticação) |
| **Version** | Versão da credencial (ex: 2.1, 2.2, 2.3, 3.1, 3.2, 3.3) |

### Mapeamento para o Sistema

```
Credential Id = CLIENT_ID
Secret = CLIENT_SECRET
Version = CREDENTIAL_VERSION
```

---

## 🌍 Endpoints Regionais

### Endpoints de Autenticação (Token)

A API usa diferentes endpoints baseados na **versão da credencial**:

#### **Versão 2.x (Cognito)**

| Região | Versão | Token Endpoint | Marketplaces |
|--------|--------|----------------|--------------|
| NA (North America) | 2.1 | `creatorsapi.auth.us-east-1.amazoncognito.com/oauth2/token` | US, CA, MX, BR |
| EU (Europe) | 2.2 | `creatorsapi.auth.eu-south-2.amazoncognito.com/oauth2/token` | UK, DE, FR, IT, ES, NL, BE, EG, IN, IE, PL, SA, SE, TR, AE |
| FE (Far East) | 2.3 | `creatorsapi.auth.us-west-2.amazoncognito.com/oauth2/token` | JP, SG, AU |

#### **Versão 3.x (LwA - Login with Amazon)**

| Região | Versão | Token Endpoint | Marketplaces |
|--------|--------|----------------|--------------|
| NA (North America) | 3.1 | `api.amazon.com/auth/o2/token` | US, CA, MX, BR |
| EU (Europe) | 3.2 | `api.amazon.co.uk/auth/o2/token` | UK, DE, FR, IT, ES, NL, BE, EG, IN, IE, PL, SA, SE, TR, AE |
| FE (Far East) | 3.3 | `api.amazon.co.jp/auth/o2/token` | JP, SG, AU |

### Endpoint da API

**Base URL para todas as regiões:** `https://creatorsapi.amazon`

---

## 🔐 Autenticação

### Passo 1: Obter Access Token

#### **Para Credenciais v2.x (Cognito)**

**Método 1: Credenciais no Body**

```bash
curl -X POST https://creatorsapi.auth.us-east-1.amazoncognito.com/oauth2/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials&client_id=YOUR_CLIENT_ID&client_secret=YOUR_CLIENT_SECRET&scope=creatorsapi/default"
```

**Método 2: Credenciais no Header (Base64)**

```bash
curl -X POST https://creatorsapi.auth.us-east-1.amazoncognito.com/oauth2/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "Authorization: Basic $(echo -n 'YOUR_CLIENT_ID:YOUR_CLIENT_SECRET' | base64)" \
  -d "grant_type=client_credentials&scope=creatorsapi/default"
```

**Resposta:**
```json
{
  "access_token": "eyJraWQiOiJ...",
  "expires_in": 3600,
  "token_type": "Bearer"
}
```

#### **Para Credenciais v3.x (LwA)**

```bash
curl -X POST https://api.amazon.com/auth/o2/token \
  -H "Content-Type: application/json" \
  -d '{
    "grant_type": "client_credentials",
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET",
    "scope": "creatorsapi::default"
  }'
```

**Resposta:**
```json
{
  "access_token": "Atc|MQICIJvSKVTZ...",
  "scope": "creatorsapi::default",
  "token_type": "bearer",
  "expires_in": 3600
}
```

### ⚠️ Importante sobre Tokens

- **Duração:** Tokens expiram após 3600 segundos (1 hora)
- **Cache:** Reutilize tokens até expirarem (não gere novo token a cada request)
- **Rate Limit:** v2.x limita a 300 requests por 5 minutos
- **Erro 429:** Indica que você está gerando tokens demais

---

## 📡 Operações da API

### Headers Comuns

#### **Para v2.x:**
```
Authorization: Bearer <access_token>, Version <credential_version>
Content-Type: application/json
x-marketplace: <marketplace_domain>
```

#### **Para v3.x:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
x-marketplace: <marketplace_domain>
```

### Marketplaces Disponíveis

| País | Marketplace Domain | Partner Tag Exemplo |
|------|-------------------|---------------------|
| Brasil | `www.amazon.com.br` | `seu-tag-20` |
| EUA | `www.amazon.com` | `seu-tag-20` |
| Reino Unido | `www.amazon.co.uk` | `seu-tag-21` |
| Alemanha | `www.amazon.de` | `seu-tag-21` |
| Japão | `www.amazon.co.jp` | `seu-tag-22` |

---

## 🛍️ Operações de Produtos

### 1. GetItems - Obter Produtos por ASIN

**Endpoint:** `POST https://creatorsapi.amazon/catalog/v1/getItems`

**Request Body:**
```json
{
  "itemIds": ["B09B2SBHQK", "B09B8V1LZ3"],
  "itemIdType": "ASIN",
  "marketplace": "www.amazon.com.br",
  "partnerTag": "seu-tag-20",
  "resources": [
    "images.primary.large",
    "images.primary.medium",
    "images.primary.small",
    "itemInfo.title",
    "itemInfo.features",
    "itemInfo.byLineInfo",
    "offersV2.listings.price",
    "offersV2.listings.savingBasis",
    "offersV2.listings.availability",
    "parentASIN",
    "browseNodeInfo.browseNodes",
    "customerReviews.starRating"
  ]
}
```

**Recursos Disponíveis:**
- `images.primary.small` - Imagem pequena
- `images.primary.medium` - Imagem média
- `images.primary.large` - Imagem grande
- `images.primary.hiRes` - Imagem alta resolução
- `itemInfo.title` - Título do produto
- `itemInfo.features` - Características
- `itemInfo.byLineInfo` - Informações do vendedor/marca
- `offersV2.listings.price` - Preço atual
- `offersV2.listings.savingBasis` - Preço original (para calcular desconto)
- `offersV2.listings.availability` - Disponibilidade
- `parentASIN` - ASIN pai (para variações)
- `browseNodeInfo.browseNodes` - Categorias
- `customerReviews.starRating` - Avaliações

**Resposta:**
```json
{
  "itemsResult": {
    "items": [
      {
        "asin": "B09B2SBHQK",
        "detailPageURL": "https://www.amazon.com.br/dp/B09B2SBHQK?tag=seu-tag-20",
        "images": {
          "primary": {
            "large": {
              "height": 500,
              "url": "https://m.media-amazon.com/images/I/41cNJGm9ZFL._SL500_.jpg",
              "width": 500
            }
          }
        },
        "itemInfo": {
          "title": {
            "displayValue": "Amazon Echo Show 5",
            "locale": "pt_BR"
          },
          "features": {
            "displayValues": [
              "Alexa can show you more",
              "Small size, bigger sound"
            ]
          }
        },
        "offersV2": {
          "listings": [
            {
              "price": {
                "amount": 299.90,
                "currency": "BRL"
              },
              "savingBasis": {
                "amount": 399.90,
                "currency": "BRL"
              }
            }
          ]
        }
      }
    ]
  }
}
```

---

### 2. SearchItems - Buscar Produtos por Palavra-chave

**Endpoint:** `POST https://creatorsapi.amazon/catalog/v1/searchItems`

**Request Body:**
```json
{
  "keywords": "fone bluetooth",
  "marketplace": "www.amazon.com.br",
  "partnerTag": "seu-tag-20",
  "itemCount": 10,
  "resources": [
    "images.primary.large",
    "itemInfo.title",
    "itemInfo.features",
    "offersV2.listings.price",
    "offersV2.listings.savingBasis",
    "browseNodeInfo.browseNodes"
  ],
  "sortBy": "Relevance"
}
```

**Parâmetros:**
- `keywords` - Palavra-chave de busca
- `itemCount` - Número de resultados (máximo: 10)
- `sortBy` - Ordenação:
  - `Relevance` - Relevância
  - `Price:LowToHigh` - Menor preço
  - `Price:HighToLow` - Maior preço
  - `AvgCustomerReviews` - Melhor avaliado
  - `NewestArrivals` - Mais recentes

**Resposta:** Similar ao GetItems

---

### 3. GetBrowseNodes - Obter Categorias

**Endpoint:** `POST https://creatorsapi.amazon/catalog/v1/getBrowseNodes`

**Request Body:**
```json
{
  "browseNodeIds": ["16243663011"],
  "marketplace": "www.amazon.com.br",
  "partnerTag": "seu-tag-20",
  "resources": [
    "browseNodes.ancestor",
    "browseNodes.children"
  ]
}
```

---

### 4. GetVariations - Obter Variações de Produto

**Endpoint:** `POST https://creatorsapi.amazon/catalog/v1/getVariations`

**Request Body:**
```json
{
  "asin": "B09B2SBHQK",
  "marketplace": "www.amazon.com.br",
  "partnerTag": "seu-tag-20",
  "resources": [
    "variationSummary.variationDimension",
    "variationSummary.price.highestPrice",
    "variationSummary.price.lowestPrice"
  ]
}
```

---

## 📊 Categorias Populares (Browse Nodes) - Brasil

| Categoria | Browse Node ID |
|-----------|----------------|
| Eletrônicos | `16243663011` |
| Computadores | `16364346011` |
| Celulares e Acessórios | `16283175011` |
| Câmeras e Foto | `16285268011` |
| Fones de Ouvido | `16285269011` |
| Video Games | `16242916011` |
| Casa Inteligente | `TBD` |
| Wearables | `TBD` |

---

## ⚡ Best Practices

### 1. Gerenciamento de Tokens
- ✅ Cache tokens até expirarem (1 hora)
- ✅ Não gere novo token a cada request
- ✅ Implemente renovação automática antes da expiração

### 2. Rate Limiting
- ✅ Respeite os limites da API
- ✅ Implemente retry com exponential backoff
- ✅ v2.x: máximo 300 tokens por 5 minutos

### 3. Segurança
- ✅ Nunca exponha credenciais em código client-side
- ✅ Não commite credenciais no Git
- ✅ Use variáveis de ambiente

### 4. Error Handling
- ✅ Implemente tratamento de erros
- ✅ Retry em falhas transitórias
- ✅ Log de erros para debugging

---

## 🔄 Changelog do SDK

| Versão | Data | Mudanças |
|--------|------|----------|
| 1.2.0 | 22/02/2026 | Suporte para credenciais v3 |
| 1.1.3 | 03/02/2026 | Fix em GetVariations |
| 1.1.2 | 12/01/2026 | Fix em SortBy do SearchItems |
| 1.1.0 | 09/01/2026 | Suporte para Reporting API |
| 1.0.0 | 15/12/2025 | Release inicial |

---

## 📝 Notas Importantes

1. **Credenciais Globais:** Suas credenciais funcionam em todos os marketplaces
2. **Partner Tag:** Você precisa de um Partner Tag válido para cada marketplace
3. **Marketplace Header:** Use `x-marketplace` para especificar o marketplace
4. **Versão no Header:** v2.x requer `Version` no Authorization header
5. **Token Caching:** Essencial para evitar rate limiting

---

## 🔗 Links Úteis

- **Documentação Oficial:** https://associados.amazon.com.br/creatorsapi/docs/
- **SDK Python:** Download via Amazon Associates Central
- **Registro:** https://associados.amazon.com.br/

---

**Última atualização:** 14 de Maio de 2026
