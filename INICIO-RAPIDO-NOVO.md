# ⚡ Início Rápido - Sistema de Ofertas Amazon

Guia rápido para colocar seu sistema funcionando em **5 minutos**.

---

## 📋 Checklist Pré-Requisitos

Antes de começar, certifique-se de ter:

- [ ] Conta Amazon Associates com credenciais da **Creators API**
- [ ] Evolution API rodando localmente (ou em servidor)
- [ ] Python 3.8+ instalado
- [ ] Grupo WhatsApp criado

---

## 🚀 Passo a Passo

### 1️⃣ Instalar Dependências (1 min)

```bash
# Navegar até o diretório do projeto
cd /caminho/do/projeto

# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate  # Mac/Linux
# OU
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt
```

---

### 2️⃣ Configurar Credenciais (2 min)

```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar arquivo (use seu editor preferido)
nano .env
```

**Cole suas credenciais:**

```env
# Amazon Creators API (obtenha em: https://associados.amazon.com.br/)
AMAZON_CREDENTIAL_ID=amzn1.application-oa2-client.xxxxxxxxxxxxx
AMAZON_CREDENTIAL_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
AMAZON_CREDENTIAL_VERSION=2.1
AMAZON_PARTNER_TAG=seu-tag-20
AMAZON_MARKETPLACE=www.amazon.com.br

# Evolution API (sua instância local)
EVOLUTION_API_URL=http://localhost:8080
EVOLUTION_API_KEY=sua_api_key_aqui
EVOLUTION_INSTANCE_NAME=amazon_gadgets

# WhatsApp (preencher no passo 3)
WHATSAPP_GROUP_ID=

# Configurações (pode deixar padrão)
PRICE_DROP_THRESHOLD=20
CHECK_INTERVAL_MINUTES=60
MAX_PRODUCTS_PER_MESSAGE=5
```

**Salve e feche** (Ctrl+X, Y, Enter no nano)

---

### 3️⃣ Obter ID do Grupo WhatsApp (1 min)

```bash
python get_group_id.py
```

**Saída esperada:**
```
Grupos encontrados:

1. Ofertas Tech
   ID: 120363123456789012@g.us
   
2. Família
   ID: 120363987654321098@g.us
```

**Copie o ID do grupo desejado** e cole no `.env`:

```bash
nano .env
# Adicione o ID:
WHATSAPP_GROUP_ID=120363123456789012@g.us
```

---

### 4️⃣ Testar Configuração (1 min)

```bash
python test_quick.py
```

**O que será testado:**
- ✅ Conexão com Amazon API
- ✅ Busca de produtos
- ✅ Conexão com Evolution API
- ✅ Validação do grupo WhatsApp
- ✅ Preview da mensagem

**Resultado esperado:**
```
🎉 TUDO PRONTO! Sistema configurado corretamente.

📌 Próximos passos:
   1. Execute: python main.py
   2. Aguarde as ofertas serem enviadas
   3. Monitore os logs: tail -f deal_monitor.log
```

---

### 5️⃣ Executar Sistema ✨

```bash
python main.py
```

**Pronto!** O sistema está rodando e monitorando ofertas automaticamente! 🎉

---

## 📊 O Que Acontece Agora?

```
┌─────────────────────────────────────────────────────┐
│  Sistema iniciado                                   │
│  ↓                                                  │
│  Buscando produtos na Amazon...                     │
│  ↓                                                  │
│  Encontrados 45 produtos com desconto              │
│  ↓                                                  │
│  Salvando no banco de dados...                      │
│  ↓                                                  │
│  Identificando melhores ofertas...                  │
│  ↓                                                  │
│  Enviando 5 produtos para WhatsApp...              │
│  ✅ Produto 1/5 enviado                            │
│  ✅ Produto 2/5 enviado                            │
│  ✅ Produto 3/5 enviado                            │
│  ✅ Produto 4/5 enviado                            │
│  ✅ Produto 5/5 enviado                            │
│  ↓                                                  │
│  Aguardando 60 minutos...                          │
│  ↓                                                  │
│  [Repete o processo]                               │
└─────────────────────────────────────────────────────┘
```

---

## 📱 Como Ficam as Mensagens

Cada oferta é enviada individualmente com:

- 📦 **Título do produto**
- 🏷️ **Marca**
- 💰 **Preço de/por**
- 📉 **% de desconto**
- 💵 **Economia em R$**
- 🖼️ **Imagem do produto**
- 🔗 **Link de afiliado**

**Exemplo:**

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

## 🔧 Ajustes Rápidos

### Mudar Desconto Mínimo

Edite `.env`:
```env
PRICE_DROP_THRESHOLD=15  # Mínimo 15% de desconto
```

### Mudar Frequência

```env
CHECK_INTERVAL_MINUTES=30  # Verifica a cada 30 minutos
```

### Mudar Quantidade de Produtos

```env
MAX_PRODUCTS_PER_MESSAGE=3  # Envia apenas 3 produtos por vez
```

---

## 🐛 Problemas Comuns

### ❌ "Token expirado"

**Solução**: Verifique credenciais no `.env`
```bash
python validate_credentials.py
```

### ❌ "Evolution API não conectada"

**Solução**: Verifique se Evolution API está rodando
```bash
curl http://localhost:8080
```

### ⚠️ "Nenhuma oferta encontrada"

**Solução**: Reduza o threshold de desconto
```env
PRICE_DROP_THRESHOLD=10  # Tente com 10%
```

---

## 📚 Próximos Passos

Agora que o sistema está funcionando:

1. **Monitore os logs**:
   ```bash
   tail -f deal_monitor.log
   ```

2. **Ajuste as configurações** conforme necessário

3. **Adicione mais keywords** em `config.py`

4. **Leia a documentação completa**: `GUIA-USO.md`

---

## 🎯 Dicas de Otimização

### Para Mais Ofertas
- Reduza `PRICE_DROP_THRESHOLD` para 10-15%
- Adicione mais keywords em `config.py`
- Aumente `MAX_PRODUCTS_PER_MESSAGE` para 7-10

### Para Ofertas Premium
- Aumente `PRICE_DROP_THRESHOLD` para 30-40%
- Reduza `MAX_PRODUCTS_PER_MESSAGE` para 2-3
- Filtre por marcas específicas

### Para Evitar Spam
- Mantenha `CHECK_INTERVAL_MINUTES` em 60-120
- Limite `MAX_PRODUCTS_PER_MESSAGE` em 3-5
- Sistema já evita duplicatas (24h cooldown)

---

## ✅ Checklist Final

- [x] Dependências instaladas
- [x] Credenciais configuradas
- [x] ID do grupo obtido
- [x] Teste executado com sucesso
- [x] Sistema rodando
- [x] Primeiras ofertas enviadas

**Parabéns! Seu sistema está funcionando! 🎉**

---

## 🆘 Precisa de Ajuda?

- **Guia Completo**: `GUIA-USO.md`
- **Configuração Detalhada**: `CONFIGURACAO.md`
- **API Amazon**: `AMAZON-CREATORS-API.md`
- **Troubleshooting**: Veja seção no `README.md`

---

**Última atualização**: 14 de Maio de 2026
