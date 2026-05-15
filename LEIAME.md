# 🚀 Sistema de Ofertas Amazon - Início Rápido

Sistema automatizado que monitora produtos tecnológicos na Amazon e envia ofertas para grupos do WhatsApp.

## ⚡ Início Rápido (3 passos)

### **1. Configure o `.env`**

```bash
cp .env.example .env
nano .env
```

Preencha:
```env
# Amazon Associates
AMAZON_ACCESS_KEY=sua_access_key
AMAZON_SECRET_KEY=sua_secret_key
AMAZON_PARTNER_TAG=seu_partner_tag

# Evolution API (instância gerenciada externamente)
EVOLUTION_INSTANCE_NAME=amazon_gadgets
EVOLUTION_API_KEY=sua_api_key

# WhatsApp (obtenha com ./get-groups.sh)
WHATSAPP_GROUP_ID=
```

### **2. Obtenha o ID do Grupo**

```bash
./get-groups.sh
```

Copie o ID do grupo desejado e cole no `.env`

### **3. Inicie o Sistema**

```bash
./start.sh
```

Pronto! O sistema está monitorando ofertas. 🎉

---

## 📋 Scripts Disponíveis

| Script | Descrição |
|--------|-----------|
| `./setup.sh` | Configuração inicial interativa |
| `./start.sh` | Iniciar monitoramento de ofertas |
| `./get-groups.sh` | Listar grupos do WhatsApp |
| `./test.sh` | Testar sistema |

---

## ⚙️ Configurações

Edite o `.env` para ajustar:

```env
PRICE_DROP_THRESHOLD=10          # Desconto mínimo (%)
CHECK_INTERVAL_MINUTES=60        # Intervalo de verificação
MAX_PRODUCTS_PER_MESSAGE=5       # Produtos por vez
```

---

## 📱 Formato das Mensagens

Cada produto é enviado como uma mensagem individual com:
- ✅ Imagem do produto
- ✅ Título
- ✅ Preço original e atual
- ✅ Percentual de desconto
- ✅ Link de afiliado

---

## 🔧 Pré-requisitos

- ✅ Python 3.8+
- ✅ Evolution API rodando (instância gerenciada externamente)
- ✅ Instância WhatsApp conectada
- ✅ Conta Amazon Associates

---

## 📊 Monitoramento

Ver logs em tempo real:
```bash
tail -f deal_monitor.log
```

Executar em background:
```bash
nohup ./start.sh > output.log 2>&1 &
```

---

## 📚 Documentação Completa

- **CONFIGURACAO.md** - Guia detalhado de configuração
- **SCRIPTS.md** - Detalhes sobre todos os scripts
- **README.md** - Documentação técnica completa

---

## ⚠️ Notas Importantes

- A **instância WhatsApp** deve ser gerenciada externamente
- O sistema **não cria** nem **conecta** instâncias
- Certifique-se que a instância está **conectada** antes de usar
- O nome da instância no `.env` deve **corresponder exatamente** ao nome real

---

**Desenvolvido para monitoramento inteligente de ofertas Amazon** 🛒🤖
