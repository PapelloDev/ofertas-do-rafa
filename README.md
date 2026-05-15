# 🤖 Sistema de Monitoramento de Ofertas Amazon para WhatsApp

Sistema automatizado que monitora **gadgets tecnológicos mais vendidos** na Amazon, identifica os **maiores descontos** e envia automaticamente para grupos do WhatsApp através da Evolution API.

## 🚀 Funcionalidades

- ✅ Busca automática de produtos tecnológicos mais vendidos
- ✅ Identifica produtos com **maior queda de preço**
- ✅ Histórico de preços em banco de dados SQLite
- ✅ Envio automático de ofertas para grupos do WhatsApp
- ✅ Links de afiliado Amazon Associates
- ✅ Mensagens formatadas com imagem e detalhes
- ✅ Agendamento automático de verificações
- ✅ Evita envio duplicado de ofertas (cooldown de 24h)
- ✅ Rate limiting e retry automático

## 📋 Pré-requisitos

1. **Conta Amazon Associates**
   - Acesse: https://associados.amazon.com.br/
   - Obtenha suas credenciais da **Amazon Creators API**
   - Obtenha seu Partner Tag (ID de afiliado)

2. **Evolution API**
   - Sistema local rodando Evolution API
   - Instância do WhatsApp conectada
   - API Key da instância

3. **Python 3.8+**

## ⚡ Início Rápido

### 1. Instalar Dependências

```bash
# Criar ambiente virtual (recomendado)
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

### 2. Configurar Credenciais

```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar com suas credenciais
nano .env  # ou use seu editor preferido
```

**Configuração mínima necessária:**

```env
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

# WhatsApp (obtenha executando: python get_group_id.py)
WHATSAPP_GROUP_ID=120363123456789012@g.us

# Configurações
PRICE_DROP_THRESHOLD=20
CHECK_INTERVAL_MINUTES=60
MAX_PRODUCTS_PER_MESSAGE=5
```

### 3. Obter ID do Grupo WhatsApp

```bash
python get_group_id.py
```

Copie o ID do grupo desejado e cole no `.env`.

### 4. Testar Configuração

```bash
python test_quick.py
```

Este script valida todas as configurações e mostra um preview das mensagens.

### 5. Executar Sistema

```bash
python main.py
```

**Pronto!** O sistema começará a monitorar ofertas automaticamente. ✨

## 📱 Como obter o ID do grupo WhatsApp

**Método Fácil (Recomendado):**

Execute o script auxiliar:
```bash
python get_group_id.py
```

Este script listará todos os seus grupos com seus respectivos IDs.

**Método Manual:**

Use o endpoint da Evolution API:
```bash
curl -X POST "http://localhost:8080/chat/findChats/INSTANCE_NAME" \
  -H "apikey: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}'
```

Procure pelo nome do grupo e copie o `remoteJid` (formato: `120363123456789012@g.us`)

## 🎯 Uso

### Scripts Disponíveis

| Script | Descrição |
|--------|-----------|
| `python test_quick.py` | **Teste rápido** - Valida configuração completa |
| `python get_group_id.py` | Obtém ID dos grupos WhatsApp |
| `python validate_credentials.py` | Valida credenciais Amazon |
| `python test_system.py` | Teste completo do sistema |
| `python main.py` | **Execução principal** - Inicia monitoramento |

### Execução Principal

Para iniciar o monitoramento contínuo:

```bash
python main.py
```

**O sistema irá:**
1. 🔍 Buscar produtos tecnológicos com desconto na Amazon
2. 💾 Salvar no banco de dados com histórico de preços
3. 📊 Identificar os maiores descontos
4. 📱 Enviar para o grupo WhatsApp (com imagem)
5. ⏰ Aguardar intervalo configurado e repetir

### Execução em Background

**Linux/Mac:**
```bash
nohup python main.py > output.log 2>&1 &
```

**Verificar logs:**
```bash
tail -f deal_monitor.log
```

**Para Windows**, use o Task Scheduler ou crie um serviço.

## 📊 Estrutura do Projeto

```
.
├── main.py                    # Script principal com agendamento
├── deal_monitor.py            # Lógica de monitoramento de ofertas
├── amazon_auth.py             # Autenticação Amazon Creators API
├── amazon_client.py           # Cliente Amazon (busca produtos)
├── evolution_client.py        # Cliente Evolution API (WhatsApp)
├── database.py                # Gerenciamento SQLite
├── config.py                  # Configurações do sistema
├── test_quick.py              # ⚡ Teste rápido de configuração
├── test_system.py             # Teste completo
├── get_group_id.py            # Obter ID do grupo WhatsApp
├── validate_credentials.py    # Validar credenciais Amazon
├── requirements.txt           # Dependências Python
├── .env.example               # Exemplo de variáveis de ambiente
├── products.db                # Banco de dados (criado automaticamente)
├── GUIA-USO.md               # 📖 Guia completo de uso
├── CONFIGURACAO.md            # Guia de configuração
└── README.md                  # Este arquivo
```

## ⚙️ Configurações

### Ajustar Desconto Mínimo

No arquivo `.env`:
```env
PRICE_DROP_THRESHOLD=20  # Apenas produtos com 20% ou mais de desconto
```

**Recomendado**: 15-25% para bom volume de ofertas

### Alterar Intervalo de Verificação

```env
CHECK_INTERVAL_MINUTES=60  # Verifica a cada 60 minutos
```

**Recomendado**: 30-120 minutos (respeita rate limits da API)

### Personalizar Keywords

Edite `config.py`:

```python
SEARCH_KEYWORDS = [
    'smartphone',
    'fone bluetooth',
    'smartwatch',
    'notebook',
    'mouse gamer',
    # Adicione suas keywords aqui
]
```

**Categorias monitoradas**: Eletrônicos, Áudio, Wearables, Computação, Casa Inteligente

## 📝 Formato das Mensagens

Cada produto é enviado individualmente com imagem:

```
🔥 OFERTA IMPERDÍVEL 🔥

📦 Fone de Ouvido Bluetooth JBL Tune 510BT
🏷️ Marca: JBL

💰 De: ~R$ 299.00~
✅ Por: R$ 179.90
📉 Desconto: 40% OFF
� Economia: R$ 119.10

🛒 Compre agora:
https://www.amazon.com.br/dp/B08XYZ123?tag=seu-tag-20

⏰ Oferta por tempo limitado!
🤖 Atualizado automaticamente pelo bot
```

**Recursos**:
- ✅ Imagem do produto
- ✅ Marca e título
- ✅ Preço de/por com economia
- ✅ Link de afiliado
- ✅ Emojis dinâmicos baseados no desconto

## 🔍 Monitoramento e Logs

Os logs são salvos em:
- Console (stdout)
- Arquivo `deal_monitor.log`

Para visualizar logs em tempo real:
```bash
tail -f deal_monitor.log
```

## 🛠️ Troubleshooting

### ❌ Erro: "Token expirado" ou "Credenciais inválidas"

**Causa**: Credenciais Amazon Creators API incorretas

**Solução**:
```bash
# 1. Validar credenciais
python validate_credentials.py

# 2. Verificar no .env:
# - AMAZON_CREDENTIAL_ID (formato: amzn1.application-oa2-client.xxxxx)
# - AMAZON_CREDENTIAL_SECRET
# - AMAZON_CREDENTIAL_VERSION (2.1, 2.2, 2.3, etc)
```

### ❌ Erro: "Evolution API não conectada"

**Causa**: Evolution API não está rodando ou configuração incorreta

**Solução**:
```bash
# 1. Verificar se Evolution API está rodando
curl http://localhost:8080

# 2. Testar conexão
python test_quick.py

# 3. Verificar no .env:
# - EVOLUTION_API_URL
# - EVOLUTION_API_KEY
# - EVOLUTION_INSTANCE_NAME
```

### ⚠️ Nenhuma oferta encontrada

**Causa**: Filtros muito restritivos

**Solução**:
- Reduza `PRICE_DROP_THRESHOLD` (ex: de 30% para 15%)
- Adicione mais keywords em `config.py`
- Aguarde acumular histórico (primeira execução pode ter poucos resultados)

### 📱 Mensagens não chegam no grupo

**Causa**: ID do grupo incorreto ou sem permissão

**Solução**:
```bash
# 1. Obter ID correto do grupo
python get_group_id.py

# 2. Verificar formato: 120363123456789012@g.us

# 3. Confirmar que o bot está no grupo
```

## 📚 Documentação Adicional

- **[GUIA-USO.md](GUIA-USO.md)** - Guia completo de uso com exemplos
- **[CONFIGURACAO.md](CONFIGURACAO.md)** - Configuração detalhada
- **[AMAZON-CREATORS-API.md](AMAZON-CREATORS-API.md)** - Documentação da API Amazon
- **[PLANO-FUTURO.md](PLANO-FUTURO.md)** - Roadmap e funcionalidades futuras

## 📈 Roadmap

**Fase Atual**: Sistema básico funcional ✅

**Próximas Funcionalidades**:
- [ ] Interface web para gerenciamento
- [ ] Múltiplos grupos por nicho (fones, notebooks, etc)
- [ ] Filtros avançados (marca, faixa de preço)
- [ ] Dashboard de estatísticas
- [ ] Notificações personalizadas por usuário
- [ ] Integração com Telegram
- [ ] API REST para consultas

## ⚖️ Avisos Legais

- Respeite os Termos de Serviço da Amazon Associates
- Não faça requisições excessivas à API
- Declare seus links de afiliado conforme exigido pela Amazon
- Este sistema é para uso pessoal/educacional

## 📄 Licença

Este projeto é fornecido "como está" para fins educacionais.

## 🤝 Contribuições

Sugestões e melhorias são bem-vindas!

---

**Desenvolvido para monitoramento inteligente de ofertas Amazon** 🛒🤖
