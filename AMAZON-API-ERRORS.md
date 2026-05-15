# ⚠️ Amazon Creators API - Erros e Troubleshooting

Documentação completa sobre códigos de erro, tratamento e resolução de problemas.

---

## 📋 Estrutura de Erro

Todos os erros seguem uma estrutura JSON consistente:

```json
{
  "type": "ValidationException",
  "message": "Partner tag in the request is invalid",
  "reason": "InvalidPartnerTag",
  "fieldList": ["partnerTag"],
  "retryAfterSeconds": 60
}
```

### Campos

| Campo | Descrição |
|-------|-----------|
| `type` | Tipo de exceção (para identificação programática) |
| `message` | Descrição legível do erro |
| `reason` | Código da razão específica do erro |
| `fieldList` | Lista de campos com problema (ValidationException) |
| `retryAfterSeconds` | Segundos para aguardar antes de retry (ThrottleException) |

---

## 🔴 Tipos de Exceção

### HTTP Status Codes

| Status | Exceção | Descrição |
|--------|---------|-----------|
| **400** | ValidationException | Entrada inválida |
| **401** | UnauthorizedException | Autenticação ausente/inválida |
| **403** | AccessDeniedException | Permissões insuficientes |
| **404** | ResourceNotFoundException | Recurso não encontrado |
| **429** | ThrottleException | Rate limit excedido |
| **500** | InternalServerException | Erro no servidor |

---

## ❌ ValidationException (400)

### Reason Codes

| Reason | Descrição | Solução |
|--------|-----------|---------|
| `UnknownOperation` | Operação não reconhecida | Verificar nome da operação |
| `CannotParse` | JSON inválido | Validar formato JSON |
| `FieldValidationFailed` | Campo(s) inválido(s) | Verificar `fieldList` |
| `InvalidAssociate` | Credencial não vinculada ao Partner Tag | Verificar vinculação no Associates Central |
| `InvalidPartnerTag` | Partner Tag inválido | Usar Partner Tag correto do marketplace |
| `Other` | Outro erro de validação | Ver mensagem específica |

### Exemplos

**Partner Tag Inválido:**
```json
{
  "type": "ValidationException",
  "message": "Partner tag in the request is invalid or is not mapped to the store associated with your credential.",
  "reason": "InvalidPartnerTag"
}
```

**Campo Faltando:**
```json
{
  "type": "ValidationException",
  "message": "Request validation failed.",
  "reason": "FieldValidationFailed",
  "fieldList": ["partnerTag", "marketplace"]
}
```

**Credencial Não Vinculada:**
```json
{
  "type": "ValidationException",
  "message": "Your credential is not linked to the partner tag in the request for the given Marketplace.",
  "reason": "InvalidAssociate"
}
```

---

## 🔐 UnauthorizedException (401)

### Reason Codes

| Reason | Descrição | Solução |
|--------|-----------|---------|
| `TokenExpired` | Token expirado | Gerar novo token |
| `InvalidToken` | Token inválido/malformado | Verificar formato e regenerar |
| `InvalidIssuer` | Issuer não corresponde | Verificar versão da credencial |
| `MissingClaim` | Claims obrigatórios ausentes | Regenerar token com scopes corretos |
| `MissingKeyId` | Key ID ausente no JWT header | Incluir `kid` no token |
| `UnsupportedClient` | Client ID não suportado | Verificar registro da credencial |
| `InvalidClient` | Client ID não corresponde | Usar Client ID correto |
| `MissingCredential` | Credenciais ausentes | Incluir Authorization header |
| `Other` | Outro erro de autenticação | Ver mensagem específica |

### Exemplos

**Token Expirado:**
```json
{
  "type": "UnauthorizedException",
  "message": "Authentication token has expired.",
  "reason": "TokenExpired"
}
```

**Token Inválido:**
```json
{
  "type": "UnauthorizedException",
  "message": "The authentication token is invalid or malformed.",
  "reason": "InvalidToken"
}
```

---

## 🚫 AccessDeniedException (403)

### Reason Codes

| Reason | Descrição | Solução |
|--------|-----------|---------|
| `AssociateNotEligible` | Conta não elegível (precisa 10 vendas em 30 dias) | Gerar vendas qualificadas |
| `AuthorizationFailed` | Falha na autorização | Verificar permissões |
| `Other` | Outro erro de acesso | Ver mensagem específica |

### Exemplo

**Conta Não Elegível:**
```json
{
  "type": "AccessDeniedException",
  "message": "Your account does not currently meet the eligibility requirements.",
  "reason": "AssociateNotEligible"
}
```

---

## 🔍 ResourceNotFoundException (404)

Recurso solicitado não existe.

### Exemplo

```json
{
  "type": "ResourceNotFoundException",
  "message": "No items found for the requested item IDs.",
  "resourceType": "Item",
  "resourceId": "B08N5WRWNW"
}
```

**Casos comuns:**
- ASIN não existe
- ASIN não acessível via Creators API
- Busca sem resultados
- Browse Node inválido

---

## 🚦 ThrottleException (429)

Rate limit excedido.

### Exemplo

```json
{
  "type": "ThrottleException",
  "message": "The request was denied due to request throttling. Please verify the number of requests made per second.",
  "retryAfterSeconds": 60
}
```

### Solução

```python
import time

def retry_with_backoff(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except ThrottleException as e:
            if attempt == max_retries - 1:
                raise
            
            wait_time = e.retry_after_seconds or (2 ** attempt)
            print(f"Rate limited. Waiting {wait_time}s...")
            time.sleep(wait_time)
```

---

## 💥 InternalServerException (500)

Erro inesperado no servidor.

### Exemplo

```json
{
  "type": "InternalServerException",
  "message": "An unexpected error occurred while processing your request."
}
```

### Solução

Implementar retry com exponential backoff:

```python
import time
import random

def exponential_backoff_retry(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except InternalServerException:
            if attempt == max_retries - 1:
                raise
            
            # Exponential backoff com jitter
            wait_time = (2 ** attempt) + random.uniform(0, 1)
            print(f"Server error. Retry {attempt + 1}/{max_retries} in {wait_time:.1f}s")
            time.sleep(wait_time)
```

---

## 🔥 Token Endpoint Rate Limiting

**Erro específico do endpoint de token (v2.x Cognito):**

### Limite
- **300 requests por 5 minutos** por Client ID

### Erro

```json
HTTP/1.1 429 Too Many Requests
Retry-After: 300

{
  "error": "too_many_requests",
  "error_description": "Your client has exceeded the token-endpoint rate limit. This usually indicates a missing token cache — access tokens are valid for 1 hour and should be reused."
}
```

### Causa

❌ **Gerando novo token a cada request**

```python
# ERRADO - Gera token toda hora
def make_request():
    token = fetch_new_token()  # ❌
    return call_api(token)
```

### Solução

✅ **Cache de token por 1 hora**

```python
# CORRETO - Cache de token
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

---

## 📊 Respostas Parciais

A API pode retornar **sucesso parcial** (HTTP 200) com array `errors`:

### Exemplo - GetItems com ASINs Inválidos

**Request:**
```json
{
  "itemIds": ["B08N5WRWNW", "B0BL8WSCH3"],
  "partnerTag": "xyz-20",
  "marketplace": "www.amazon.com.br"
}
```

**Response:**
```json
{
  "errors": [
    {
      "code": "InvalidParameterValue",
      "message": "The ItemIds B08N5WRWNW provided in the request is invalid."
    }
  ],
  "itemsResult": {
    "items": [
      {
        "asin": "B0BL8WSCH3",
        "detailPageURL": "https://www.amazon.com.br/dp/B0BL8WSCH3?tag=xyz-20",
        "itemInfo": {
          "title": {
            "displayValue": "Amazon Fire 7 Kids tablet"
          }
        }
      }
    ]
  }
}
```

### Comportamento

| Cenário | HTTP Status | Response |
|---------|-------------|----------|
| **Todos válidos** | 200 | `itemsResult` apenas |
| **Alguns válidos** | 200 | `itemsResult` + `errors` array |
| **Todos inválidos** | 404 | `ResourceNotFoundException` |

### Tratamento

```python
def process_response(response):
    # Processar itens válidos
    if 'itemsResult' in response:
        for item in response['itemsResult']['items']:
            process_item(item)
    
    # Logar erros parciais
    if 'errors' in response:
        for error in response['errors']:
            logger.warning(f"Partial error: {error['code']} - {error['message']}")
```

---

## 🔧 Troubleshooting

### 1. Resource Não Retornado

**Problema:** Solicitou resource mas não veio na resposta.

**Causa:** Resource não disponível para aquele produto.

**Exemplo:**
```json
{
  "resources": ["itemInfo.contentRating", "itemInfo.title"]
}
```

Se o produto não tem `contentRating`, só `title` será retornado.

**Solução:** Sempre verificar se o resource existe antes de usar:

```python
def get_content_rating(item):
    item_info = item.get('itemInfo', {})
    content_rating = item_info.get('contentRating')
    
    if content_rating:
        return content_rating.get('audienceRating', {}).get('displayValue')
    return None
```

---

### 2. Busca Sem Resultados

**Problema:** Request válido mas sem resultados.

**Response:**
```json
{
  "type": "ResourceNotFoundException",
  "message": "No results found for your search request",
  "resourceType": "SearchResult",
  "resourceId": "Mystery Novels Non Existing"
}
```

**Causas:**
- Keywords muito específicas
- SearchIndex errado
- Filtros muito restritivos
- Produto não existe

**Solução:**
- Tentar keywords mais genéricas
- Remover alguns filtros
- Usar SearchIndex "All"
- Verificar se produto existe na Amazon

---

### 3. Rate Limiting

**Sintomas:**
- Erro 429 frequente
- Requests lentos
- Timeouts

**Diagnóstico:**
```python
import time

class RateLimiter:
    def __init__(self, tps=1):
        self.tps = tps
        self.last_request = 0
    
    def wait_if_needed(self):
        now = time.time()
        time_since_last = now - self.last_request
        
        if time_since_last < (1.0 / self.tps):
            wait_time = (1.0 / self.tps) - time_since_last
            time.sleep(wait_time)
        
        self.last_request = time.time()
```

---

## 📝 Best Practices

### 1. Tratamento de Erros

```python
class CreatorsAPIError(Exception):
    def __init__(self, error_type, message, reason=None):
        self.error_type = error_type
        self.message = message
        self.reason = reason
        super().__init__(f"{error_type}: {message}")

def handle_api_error(response):
    if response.status_code == 200:
        data = response.json()
        
        # Verificar erros parciais
        if 'errors' in data:
            for error in data['errors']:
                logger.warning(f"Partial error: {error}")
        
        return data
    
    # Erros HTTP
    error_data = response.json()
    error_type = error_data.get('type')
    message = error_data.get('message')
    reason = error_data.get('reason')
    
    if response.status_code == 401:
        if reason == 'TokenExpired':
            # Renovar token
            return refresh_token_and_retry()
    
    elif response.status_code == 429:
        retry_after = error_data.get('retryAfterSeconds', 60)
        time.sleep(retry_after)
        return retry_request()
    
    elif response.status_code >= 500:
        return exponential_backoff_retry()
    
    raise CreatorsAPIError(error_type, message, reason)
```

### 2. Logging

```python
import logging

logger = logging.getLogger(__name__)

def log_api_call(operation, params, response):
    logger.info(f"API Call: {operation}")
    logger.debug(f"Params: {params}")
    
    if response.status_code != 200:
        logger.error(f"Error {response.status_code}: {response.text}")
    else:
        data = response.json()
        if 'errors' in data:
            logger.warning(f"Partial errors: {data['errors']}")
```

### 3. Retry Strategy

```python
from functools import wraps
import time

def retry_on_error(max_retries=3, backoff_factor=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except (ThrottleException, InternalServerException) as e:
                    if attempt == max_retries - 1:
                        raise
                    
                    wait_time = backoff_factor ** attempt
                    logger.warning(f"Retry {attempt + 1}/{max_retries} in {wait_time}s")
                    time.sleep(wait_time)
        return wrapper
    return decorator
```

---

## 🌍 Marketplace Brasil (BR)

### Configurações

| Parâmetro | Valor |
|-----------|-------|
| **Marketplace** | `www.amazon.com.br` |
| **Language** | `pt_BR` (padrão) |
| **Currency** | `BRL` (padrão) |

### Search Indexes

| SearchIndex | Display Name |
|-------------|--------------|
| `All` | Todos os departamentos |
| `Books` | Livros |
| `Computers` | Computadores e Informática |
| `Electronics` | Eletrônicos |
| `HomeAndKitchen` | Casa e Cozinha |
| `KindleStore` | Loja Kindle |
| `MobileApps` | Apps e Jogos |
| `OfficeProducts` | Material para Escritório |
| `ToolsAndHomeImprovement` | Ferramentas e Construção |
| `VideoGames` | Games |

### Exemplo de Request BR

```json
{
  "partnerTag": "seu-tag-20",
  "marketplace": "www.amazon.com.br",
  "languagesOfPreference": ["pt_BR"],
  "currencyOfPreference": "BRL",
  "keywords": "fone bluetooth",
  "searchIndex": "Electronics"
}
```

---

## ✅ Checklist de Troubleshooting

- [ ] Verificar se credenciais estão corretas
- [ ] Confirmar que Partner Tag está vinculado à credencial
- [ ] Usar marketplace correto (`www.amazon.com.br`)
- [ ] Cache de token implementado (1 hora)
- [ ] Rate limiting respeitado (TPS/TPD)
- [ ] Retry com exponential backoff para 429/500
- [ ] Tratamento de erros parciais (array `errors`)
- [ ] Logging adequado de erros
- [ ] Verificar elegibilidade da conta (10 vendas/30 dias)

---

**Última atualização:** 14 de Maio de 2026
