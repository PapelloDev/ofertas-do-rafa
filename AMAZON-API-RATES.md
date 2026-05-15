# 📊 Amazon Creators API - Rate Limits e Best Practices

Documentação sobre limites de uso, rate limiting e melhores práticas.

---

## 🚦 Limites de API (Rate Limits)

### Definições

| Termo | Descrição |
|-------|-----------|
| **TPS** | Transactions Per Second - Máximo de chamadas por segundo |
| **TPD** | Transactions Per Day - Máximo de chamadas por dia |
| **Primary Account** | Email usado para criar conta Associates e gerar credenciais |
| **Shipped Revenue** | Volume de vendas de itens enviados via seus links |

### Limites Iniciais

Ao criar suas credenciais, você recebe:

- ✅ **1 TPS** - 1 request por segundo
- ✅ **8,640 TPD** - 8,640 requests por dia
- ⏰ **Período:** Primeiros 30 dias

**Importante:** Cada chamada à API conta como 1 transação, independente de quantos ASINs você enviar.

**Exemplo:**
```json
// Esta chamada conta como 1 transação (não 10)
{
  "itemIds": ["ASIN1", "ASIN2", "ASIN3", "ASIN4", "ASIN5", 
              "ASIN6", "ASIN7", "ASIN8", "ASIN9", "ASIN10"]
}
```

---

## 📈 Aumento de Limites

Seus limites aumentam automaticamente baseado em **receita de vendas**:

### Fórmula de Cálculo

| Receita | Limite Ganho |
|---------|--------------|
| **$0.05** (5 centavos) | +1 TPD |
| **$4,320** | +1 TPS (máximo 10 TPS) |

### Exemplo Prático

```
Receita nos últimos 30 dias: $10,000

TPD = 10,000 / 0.05 = 200,000 TPD
TPS = 10,000 / 4,320 = 2.31 → 2 TPS (arredonda para baixo)
```

### ⚠️ Perda de Acesso

Você **perde acesso** à API se:
- ❌ Não gerar vendas qualificadas por **30 dias consecutivos**
- ✅ Recupera acesso em **2 dias** após nova venda ser enviada

---

## 🔥 Erro 429 - TooManyRequests

Você receberá erro **429** quando:

1. ❌ Exceder seu TPS (requests por segundo)
2. ❌ Exceder seu TPD (requests por dia)
3. ❌ Acesso foi revogado (sem vendas por 30 dias)

**Exemplo de Erro:**
```json
{
  "error": "TooManyRequests",
  "message": "Rate exceeded"
}
```

---

## ✅ Best Practices - Práticas Recomendadas

### 1. Cache de Access Tokens ⚡

**❌ ERRADO:**
```python
# Gera token a cada request (vai bater rate limit!)
def make_request():
    token = fetch_new_token()  # ❌ NÃO FAÇA ISSO
    return call_api(token)
```

**✅ CORRETO:**
```python
# Cache token por 1 hora
class TokenCache:
    def __init__(self):
        self.token = None
        self.expires_at = None
    
    def get_token(self):
        if self.token is None or datetime.now() >= self.expires_at:
            self.token = fetch_new_token()
            self.expires_at = datetime.now() + timedelta(hours=1)
        return self.token
```

**Importante:**
- ✅ Tokens duram **1 hora** (3600 segundos)
- ✅ Reutilize o mesmo token em todos os requests
- ✅ v2.x limita a **300 tokens por 5 minutos**
- ✅ SDKs fazem isso automaticamente

---

### 2. Use Partner Tag Corretamente 🏷️

**Regras:**
- ✅ Use o Partner Tag correto para cada marketplace
- ✅ Não altere os links retornados pela API
- ✅ Use a mesma conta (email) para Associates e Creators API

**Exemplo:**
```python
# Para Brasil
partner_tag = "seu-tag-20"
marketplace = "www.amazon.com.br"

# Para EUA
partner_tag = "seu-tag-20"  # Pode ser diferente
marketplace = "www.amazon.com"
```

---

### 3. Envie Múltiplos ASINs por Request 📦

**❌ ERRADO - 10 requests:**
```python
for asin in asins:
    get_items([asin])  # 10 chamadas = 10 transações
```

**✅ CORRETO - 1 request:**
```python
get_items(asins)  # 1 chamada = 1 transação (até 10 ASINs)
```

**Limites:**
- GetItems: até **10 ASINs** por request
- GetBrowseNodes: até **10 BrowseNodeIds** por request

---

### 4. Controle Fino de Rate (TPS) ⏱️

Distribua suas chamadas ao longo do dia:

**❌ ERRADO:**
```python
# Envia todas as 8640 chamadas em 2 horas
for i in range(8640):
    make_request()  # Vai bater TPS!
```

**✅ CORRETO:**
```python
import time

# Distribui ao longo de 24 horas
# 8640 requests / 86400 segundos = 1 request a cada 10 segundos
for i in range(8640):
    make_request()
    time.sleep(10)  # Espera 10 segundos
```

**Cálculo:**
```
Se você tem 1 TPS:
- Máximo: 1 request por segundo
- Por dia: 86,400 segundos → máximo 86,400 requests
- Mas TPD limita a 8,640

Solução: 8,640 requests / 86,400 segundos = 1 request a cada 10 segundos
```

---

### 5. Cache de Respostas da API 💾

**Tempos de Cache Recomendados:**

| Recurso | TTL (Time To Live) |
|---------|-------------------|
| **Offers** (preços) | 1 hora |
| **BrowseNodeInfo** | 1 hora |
| **Images** | 1 dia |
| **ItemInfo.Title** | 1 dia |
| **DetailPageURL** | 1 dia |
| **Outros recursos** | 1 dia |

**Implementação:**
```python
import time

class ResponseCache:
    def __init__(self):
        self.cache = {}
    
    def get(self, key, ttl_hours=1):
        if key in self.cache:
            data, timestamp = self.cache[key]
            if time.time() - timestamp < ttl_hours * 3600:
                return data
        return None
    
    def set(self, key, data, ttl_hours=1):
        self.cache[key] = (data, time.time())

# Uso
cache = ResponseCache()

# Cache de preços (1 hora)
price_data = cache.get(f"price_{asin}", ttl_hours=1)
if price_data is None:
    price_data = fetch_from_api(asin)
    cache.set(f"price_{asin}", price_data, ttl_hours=1)

# Cache de imagens (1 dia)
image_data = cache.get(f"image_{asin}", ttl_hours=24)
if image_data is None:
    image_data = fetch_from_api(asin)
    cache.set(f"image_{asin}", image_data, ttl_hours=24)
```

---

### 6. Peça Apenas os Resources Necessários 🎯

**❌ ERRADO - Pede tudo:**
```json
{
  "resources": [
    "images.primary.small",
    "images.primary.medium",
    "images.primary.large",
    "images.primary.hiRes",
    "images.variants",
    "itemInfo.title",
    "itemInfo.features",
    "itemInfo.byLineInfo",
    // ... 20+ recursos desnecessários
  ]
}
```

**✅ CORRETO - Pede só o necessário:**
```json
{
  "resources": [
    "images.primary.large",
    "itemInfo.title",
    "offersV2.listings.price",
    "offersV2.listings.savingBasis"
  ]
}
```

**Benefícios:**
- ⚡ Resposta mais rápida
- 📉 Menor payload
- 🚀 Menos processamento

---

### 7. Lide com Web Crawlers 🤖

Crawlers podem consumir seus limites:

**Solução: robots.txt**
```txt
User-agent: *
Disallow: /api/
Disallow: /search/
Crawl-delay: 10
```

---

## 📋 Headers e Parâmetros Comuns

### Headers Obrigatórios

#### **Para v2.x (Cognito):**
```http
Content-Type: application/json
Authorization: Bearer eyJraWQiOiJ..., Version 2.1
x-marketplace: www.amazon.com.br
```

#### **Para v3.x (LwA):**
```http
Content-Type: application/json
Authorization: Bearer Atc|MQICIJvS...
x-marketplace: www.amazon.com.br
```

### Parâmetros Obrigatórios

```json
{
  "marketplace": "www.amazon.com.br",
  "partnerTag": "seu-tag-20"
}
```

---

## 🌍 Marketplaces Disponíveis

| País | Marketplace | Região | Versão Credencial |
|------|-------------|--------|-------------------|
| Brasil | `www.amazon.com.br` | NA | 2.1 / 3.1 |
| EUA | `www.amazon.com` | NA | 2.1 / 3.1 |
| Canadá | `www.amazon.ca` | NA | 2.1 / 3.1 |
| México | `www.amazon.com.mx` | NA | 2.1 / 3.1 |
| Reino Unido | `www.amazon.co.uk` | EU | 2.2 / 3.2 |
| Alemanha | `www.amazon.de` | EU | 2.2 / 3.2 |
| França | `www.amazon.fr` | EU | 2.2 / 3.2 |
| Itália | `www.amazon.it` | EU | 2.2 / 3.2 |
| Espanha | `www.amazon.es` | EU | 2.2 / 3.2 |
| Japão | `www.amazon.co.jp` | FE | 2.3 / 3.3 |
| Austrália | `www.amazon.com.au` | FE | 2.3 / 3.3 |
| Índia | `www.amazon.in` | EU | 2.2 / 3.2 |

**Importante:**
- ✅ Suas credenciais funcionam **globalmente**
- ✅ Você precisa de **Partner Tag válido** para cada marketplace
- ✅ Você precisa de **acesso aprovado** para cada região

---

## 🔢 Entendendo Versões

### Tipos de Versão

| Tipo | Exemplo | Onde Usar | Propósito |
|------|---------|-----------|-----------|
| **Credential Version** | 2.1, 3.1 | Authorization header | Formato de autenticação |
| **SDK Version** | 1.1.2 | Package SDK | Versão da biblioteca |
| **API Version** | v1 | URL endpoint | Versão dos endpoints |
| **Resource Version** | OffersV2 | Response data | Formato dos dados |

### Credential Version

```http
# v2.x - Cognito
Authorization: Bearer YOUR_TOKEN, Version 2.1

# v3.x - LwA
Authorization: Bearer YOUR_TOKEN
```

### API Version (nos endpoints)

```
https://creatorsapi.amazon/catalog/v1/getItems
https://creatorsapi.amazon/catalog/v1/searchItems
https://creatorsapi.amazon/catalog/v1/getBrowseNodes
https://creatorsapi.amazon/catalog/v1/getVariations
```

### Resource Version (nos requests)

```json
{
  "resources": [
    "offersV2.listings.price",      // v2 - Novo formato
    "offersV2.listings.availability"
  ]
}
```

---

## 📊 Monitoramento de Vendas

Verifique vendas atribuídas à API:

1. Acesse **Associates Central**
2. Vá em **Link Type Performance Report**
3. Filtre por **Creators API**

---

## ⚠️ Checklist para Atribuição Correta

- ✅ Use links exatamente como retornados pela API
- ✅ Não edite parâmetros da URL
- ✅ Use mesma conta (email) para Associates e Creators API
- ✅ Use credenciais da conta primária
- ✅ Passe Partner Tag em todos os requests

---

## 🎯 Resumo para Nosso Sistema

Para o sistema de ofertas, devemos:

1. ✅ **Cache de token** - Reutilizar por 1 hora
2. ✅ **Cache de preços** - 1 hora (são voláteis)
3. ✅ **Cache de imagens/títulos** - 1 dia (são estáveis)
4. ✅ **Múltiplos ASINs** - Até 10 por request
5. ✅ **Rate control** - Distribuir requests ao longo do dia
6. ✅ **Resources mínimos** - Pedir só o necessário
7. ✅ **Retry com backoff** - Em caso de erro 429

---

**Última atualização:** 14 de Maio de 2026
