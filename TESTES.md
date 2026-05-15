# 🧪 Guia de Testes

Documentação sobre a estrutura de testes e como executá-los.

---

## 📋 Estrutura de Testes

```
tests/
├── __init__.py
├── test_amazon_auth.py      # Testes de autenticação
├── test_amazon_client.py    # Testes do cliente Amazon (futuro)
└── test_evolution_client.py # Testes do cliente WhatsApp (futuro)
```

---

## 🚀 Executando Testes

### Todos os Testes

```bash
# Ativar venv
source venv/bin/activate

# Executar todos os testes
pytest

# Com cobertura
pytest --cov=. --cov-report=html
```

### Testes Específicos

```bash
# Apenas testes de autenticação
pytest tests/test_amazon_auth.py

# Teste específico
pytest tests/test_amazon_auth.py::TestAmazonAuth::test_init_valid_version

# Testes por marcador
pytest -m unit
pytest -m integration
```

### Modo Verbose

```bash
# Mais detalhes
pytest -v

# Muito detalhes
pytest -vv

# Com print statements
pytest -s
```

---

## ✅ Validação de Credenciais

### Script Standalone

```bash
# Validar credenciais do .env
python validate_credentials.py
```

**Output esperado:**
```
============================================================
  Amazon Creators API - Validação de Credenciais
============================================================

ℹ Verificando variáveis de ambiente...
✓ AMAZON_CREDENTIAL_ID: amzn1.application-oa...
✓ AMAZON_CREDENTIAL_SECRET: ********************
✓ AMAZON_PARTNER_TAG: seu-tag-20

ℹ Validando credenciais com Amazon (versão 2.1)...
✓ Credenciais válidas!
ℹ   Tipo de token: Cognito
ℹ   Validade: 3600 segundos (1 hora)

============================================================
  Próximos Passos
============================================================

✓ Todas as validações passaram!

ℹ Você pode agora:
  1. Executar os testes: ./test.sh
  2. Iniciar o sistema: ./start.sh
  3. Testar busca de produtos manualmente
```

---

## 🧪 Testes Implementados

### `test_amazon_auth.py`

| Teste | Descrição |
|-------|-----------|
| `test_init_valid_version` | Inicialização com versão válida |
| `test_init_invalid_version` | Rejeita versão inválida |
| `test_get_token_endpoint_v2` | Endpoint correto para v2.x |
| `test_get_token_endpoint_v3` | Endpoint correto para v3.x |
| `test_is_v2` | Identifica versão corretamente |
| `test_fetch_new_token_success_v2` | Obtém token v2.x com sucesso |
| `test_fetch_new_token_success_v3` | Obtém token v3.x com sucesso |
| `test_fetch_new_token_invalid_credentials` | Trata credenciais inválidas |
| `test_fetch_new_token_rate_limit` | Trata rate limit |
| `test_get_valid_token_caches` | Cache de token funciona |
| `test_get_valid_token_renews_when_expired` | Renova token expirado |
| `test_get_auth_header_v2` | Formata header v2.x |
| `test_get_auth_header_v3` | Formata header v3.x |
| `test_validate_credentials_success` | Validação bem-sucedida |
| `test_validate_credentials_failure` | Validação com erro |
| `test_clear_cache` | Limpa cache |

**Total:** 16 testes

---

## 📊 Cobertura de Código

### Gerar Relatório

```bash
pytest --cov=. --cov-report=html
```

### Ver Relatório

```bash
open htmlcov/index.html
```

### Meta de Cobertura

- **Mínimo:** 80%
- **Ideal:** 90%+

---

## 🎯 Boas Práticas de Testes

### 1. Nomenclatura

```python
# ✅ BOM - Descritivo
def test_get_valid_token_caches():
    """Deve cachear token e não buscar novamente"""
    pass

# ❌ RUIM - Vago
def test_token():
    pass
```

### 2. Arrange-Act-Assert

```python
def test_example():
    # Arrange - Preparar
    auth = AmazonAuth('id', 'secret', '2.1')
    
    # Act - Executar
    result = auth.validate_credentials()
    
    # Assert - Verificar
    assert result['valid'] is True
```

### 3. Mocks

```python
@patch('amazon_auth.requests.post')
def test_with_mock(mock_post):
    # Configurar mock
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {'access_token': 'test'}
    
    # Testar
    auth = AmazonAuth('id', 'secret', '2.1')
    token = auth.get_valid_token()
    
    # Verificar
    assert token == 'test'
    mock_post.assert_called_once()
```

### 4. Fixtures

```python
import pytest

@pytest.fixture
def auth():
    """Fixture de autenticação"""
    return AmazonAuth('test_id', 'test_secret', '2.1')

def test_with_fixture(auth):
    assert auth.version == '2.1'
```

---

## 🔍 Debugging de Testes

### Executar com Debugger

```bash
# Parar no primeiro erro
pytest -x

# Parar no primeiro erro e abrir debugger
pytest --pdb

# Mostrar variáveis locais em falhas
pytest -l
```

### Logs

```python
import logging

def test_with_logs(caplog):
    caplog.set_level(logging.INFO)
    
    auth = AmazonAuth('id', 'secret', '2.1')
    auth.get_valid_token()
    
    assert "Token obtido" in caplog.text
```

---

## 📝 Checklist de Testes

Antes de fazer commit:

- [ ] Todos os testes passam
- [ ] Cobertura >= 80%
- [ ] Sem warnings
- [ ] Código formatado (black/autopep8)
- [ ] Docstrings atualizadas
- [ ] CHANGELOG.md atualizado

---

## 🚦 CI/CD (Futuro)

### GitHub Actions

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest --cov=. --cov-report=xml
      - uses: codecov/codecov-action@v2
```

---

## 📚 Recursos

- [Pytest Documentation](https://docs.pytest.org/)
- [Pytest-cov](https://pytest-cov.readthedocs.io/)
- [Pytest-mock](https://pytest-mock.readthedocs.io/)
- [Testing Best Practices](https://docs.python-guide.org/writing/tests/)

---

**Última atualização:** 14 de Maio de 2026
