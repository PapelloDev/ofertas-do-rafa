# 🚀 Guia de Uso - Sistema de Ofertas Amazon

Sistema automatizado que monitora gadgets tecnológicos na Amazon, identifica os mais vendidos com maior desconto e envia automaticamente para grupos do WhatsApp via Evolution API.

---

## 📋 Pré-requisitos

### 1. Conta Amazon Associates
- Acesse: https://associados.amazon.com.br/
- Crie sua conta de afiliado
- Obtenha suas credenciais da **Creators API**

### 2. Evolution API
- Tenha uma instância Evolution API rodando localmente ou em servidor
- URL padrão: `http://localhost:8080`
- Obtenha sua API Key e nome da instância

### 3. Grupo WhatsApp
- Crie um grupo no WhatsApp
- Obtenha o ID do grupo (veja seção abaixo)

---

## ⚙️ Configuração

### Passo 1: Clonar e Instalar Dependências

```bash
cd /caminho/do/projeto
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Passo 2: Configurar Variáveis de Ambiente

Copie o arquivo de exemplo:
```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais:

```bash
# Amazon Creators API
AMAZON_CREDENTIAL_ID=amzn1.application-oa2-client.xxxxx
AMAZON_CREDENTIAL_SECRET=seu_secret_aqui
AMAZON_CREDENTIAL_VERSION=2.1
AMAZON_PARTNER_TAG=seu-tag-20
AMAZON_MARKETPLACE=www.amazon.com.br

# Evolution API
EVOLUTION_API_URL=http://localhost:8080
EVOLUTION_API_KEY=sua_api_key_aqui
EVOLUTION_INSTANCE_NAME=amazon_gadgets

# WhatsApp
WHATSAPP_GROUP_ID=120363123456789012@g.us

# Configurações de Monitoramento
PRICE_DROP_THRESHOLD=20
CHECK_INTERVAL_MINUTES=60
MAX_PRODUCTS_PER_MESSAGE=5
```

### Passo 3: Obter ID do Grupo WhatsApp

Execute o script auxiliar:
```bash
python get_group_id.py
```

Isso listará todos os grupos disponíveis. Copie o ID do grupo desejado e cole no `.env`.

---

## 🎯 Como Funciona

### Fluxo de Operação

```
┌─────────────────────────────────────────────────────────┐
│  1. Sistema inicia e busca produtos na Amazon           │
│     - Usa keywords configuradas (fone bluetooth, etc)   │
│     - Filtra por desconto mínimo (ex: 20%)              │
│     - Busca em categoria Electronics                    │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  2. Salva produtos no banco de dados SQLite             │
│     - Armazena preço atual e histórico                  │
│     - Calcula porcentagem de desconto                   │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  3. Identifica melhores ofertas                         │
│     - Ordena por maior desconto                         │
│     - Remove produtos já enviados nas últimas 24h       │
│     - Seleciona top N produtos (configurável)           │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  4. Envia para WhatsApp via Evolution API               │
│     - Mensagem formatada com imagem                     │
│     - Link de afiliado Amazon                           │
│     - Informações de preço e desconto                   │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  5. Aguarda próximo ciclo (ex: 60 minutos)              │
│     - Repete o processo automaticamente                 │
└─────────────────────────────────────────────────────────┘
```

### Keywords Monitoradas

O sistema busca automaticamente por estas categorias de produtos:

- 📱 **Smartphones e Acessórios**: smartphone, carregador rápido, power bank
- 🎧 **Áudio**: fone bluetooth, airpods, soundbar
- ⌚ **Wearables**: smartwatch, smart band
- 💻 **Computação**: notebook, SSD, mouse gamer, teclado mecânico
- 📷 **Foto/Vídeo**: webcam, ring light
- 🏠 **Casa Inteligente**: alexa, chromecast
- 📱 **Tablets**: tablet, kindle

---

## 🚀 Executando o Sistema

### Modo Normal (Produção)

Inicia o sistema em loop contínuo:

```bash
python main.py
```

O sistema irá:
1. Executar primeira varredura imediatamente
2. Enviar ofertas encontradas para o grupo
3. Aguardar intervalo configurado (ex: 60 min)
4. Repetir o processo indefinidamente

### Modo Teste (Uma Execução)

Para testar sem loop contínuo:

```bash
python test_system.py
```

Isso executa um ciclo completo e mostra estatísticas.

---

## 📊 Exemplo de Mensagem Enviada

```
🔥 OFERTA IMPERDÍVEL 🔥

📦 Fone de Ouvido Bluetooth JBL Tune 510BT
🏷️ Marca: JBL

💰 De: ~R$ 299.00~
✅ Por: R$ 179.90
📉 Desconto: 40% OFF
💵 Economia: R$ 119.10

🛒 Compre agora:
https://www.amazon.com.br/dp/B08XYZ123?tag=seu-tag-20

⏰ Oferta por tempo limitado!
🤖 Atualizado automaticamente pelo bot
```

---

## 🔧 Configurações Avançadas

### Ajustar Desconto Mínimo

No arquivo `.env`:
```bash
PRICE_DROP_THRESHOLD=30  # Apenas produtos com 30% ou mais de desconto
```

### Alterar Intervalo de Verificação

```bash
CHECK_INTERVAL_MINUTES=30  # Verifica a cada 30 minutos
```

### Limitar Produtos por Envio

```bash
MAX_PRODUCTS_PER_MESSAGE=3  # Envia apenas top 3 ofertas
```

### Adicionar Novas Keywords

Edite `config.py`:

```python
SEARCH_KEYWORDS = [
    'smartphone',
    'fone bluetooth',
    'smartwatch',
    # Adicione suas keywords aqui
    'drone',
    'gopro',
    'console'
]
```

---

## 🐛 Solução de Problemas

### Erro: "Token expirado"

**Causa**: Credenciais Amazon inválidas ou expiradas

**Solução**:
1. Verifique suas credenciais no `.env`
2. Confirme que a versão está correta (2.1, 2.2, 2.3, etc)
3. Teste com: `python validate_credentials.py`

### Erro: "Evolution API não conectada"

**Causa**: Evolution API não está rodando ou configuração incorreta

**Solução**:
1. Verifique se Evolution API está rodando: `curl http://localhost:8080`
2. Confirme API Key e Instance Name no `.env`
3. Teste conexão: `python -c "from evolution_client import EvolutionAPIClient; print(EvolutionAPIClient().check_connection())"`

### Erro: "Nenhum produto encontrado"

**Causa**: Filtros muito restritivos ou API sem resultados

**Solução**:
1. Reduza `PRICE_DROP_THRESHOLD` (ex: de 30% para 15%)
2. Adicione mais keywords em `config.py`
3. Verifique logs: `tail -f deal_monitor.log`

### Produtos já enviados não aparecem novamente

**Comportamento esperado**: Sistema evita spam enviando cada produto apenas 1x a cada 24h

**Para resetar**: Delete o banco de dados
```bash
rm products.db
```

---

## 📈 Monitoramento

### Ver Logs em Tempo Real

```bash
tail -f deal_monitor.log
```

### Verificar Banco de Dados

```bash
sqlite3 products.db "SELECT COUNT(*) FROM products;"
sqlite3 products.db "SELECT title, discount_percentage FROM products ORDER BY discount_percentage DESC LIMIT 10;"
```

### Estatísticas do Sistema

```python
from deal_monitor import DealMonitor
monitor = DealMonitor()
stats = monitor.get_statistics()
print(stats)
```

---

## 🔒 Segurança

### Boas Práticas

✅ **FAÇA**:
- Mantenha `.env` fora do Git (já está no `.gitignore`)
- Use variáveis de ambiente em produção
- Rotacione API keys periodicamente
- Monitore logs de erro

❌ **NÃO FAÇA**:
- Commitar credenciais no código
- Compartilhar seu `.env`
- Usar credenciais de produção em testes
- Expor API keys publicamente

---

## 🚦 Limites da API Amazon

### Rate Limits

- **TPS (Transactions Per Second)**: 1 request/segundo
- **TPD (Transactions Per Day)**: 8640 requests/dia
- **Token Limit**: Máximo 300 tokens por 5 minutos

### O Sistema Respeita Automaticamente

✅ Rate limiting implementado (1 TPS)
✅ Retry automático em caso de erro 429
✅ Cache de tokens (reutiliza por 1 hora)
✅ Exponential backoff em falhas

---

## 📞 Suporte

### Documentação Adicional

- `AMAZON-CREATORS-API.md` - Detalhes da API Amazon
- `AMAZON-API-EXAMPLES.md` - Exemplos de requests
- `PLANO-FUTURO.md` - Roadmap de funcionalidades
- `CONFIGURACAO.md` - Guia de configuração detalhado

### Logs de Debug

Para mais detalhes nos logs, edite `main.py`:

```python
logging.basicConfig(
    level=logging.DEBUG,  # Mude de INFO para DEBUG
    ...
)
```

---

## 🎉 Pronto!

Seu sistema está configurado e pronto para monitorar ofertas automaticamente!

**Próximos passos**:
1. Execute `python main.py`
2. Aguarde as primeiras ofertas serem enviadas
3. Monitore os logs
4. Ajuste configurações conforme necessário

**Dica**: Comece com `PRICE_DROP_THRESHOLD=15` e `CHECK_INTERVAL_MINUTES=60` para ter um bom volume de ofertas sem spam.

---

**Última atualização**: 14 de Maio de 2026
