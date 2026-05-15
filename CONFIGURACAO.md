# 🚀 Guia de Configuração - Sistema de Ofertas Amazon

Este guia vai te ajudar a configurar o sistema passo a passo.

## 📋 Pré-requisitos

1. **Python 3.8+** instalado
2. **Evolution API** rodando localmente (porta 8080)
3. **Conta Amazon Associates** (para links de afiliado)

---

## 🔧 Passo 1: Instalar Dependências

```bash
cd "/Volumes/Storage Expansion/Windsurf/CascadeProjects/windsurf-project"
pip install -r requirements.txt
```

---

## ⚙️ Passo 2: Configurar Variáveis de Ambiente

### 2.1. Copiar arquivo de exemplo

```bash
cp .env.example .env
```

### 2.2. Editar o arquivo `.env`

Abra o arquivo `.env` e configure:

```env
# Amazon Associates - Obtenha em https://associados.amazon.com.br/
AMAZON_ACCESS_KEY=sua_access_key_aqui
AMAZON_SECRET_KEY=sua_secret_key_aqui
AMAZON_PARTNER_TAG=seu_partner_tag_aqui
AMAZON_REGION=BR

# Evolution API - Configure conforme sua instalação
EVOLUTION_API_URL=http://localhost:8080
EVOLUTION_API_KEY=B6D711FCDE4D4FD5936544120E713976
EVOLUTION_INSTANCE_NAME=ofertas_amazon

# WhatsApp - Será preenchido no Passo 4
WHATSAPP_GROUP_ID=

# Configurações do Sistema
PRICE_DROP_THRESHOLD=10
CHECK_INTERVAL_MINUTES=60
MAX_PRODUCTS_PER_MESSAGE=5
```

**⚠️ IMPORTANTE:**
- **EVOLUTION_API_KEY**: Altere para sua chave de API (encontre no painel da Evolution API)
- **EVOLUTION_INSTANCE_NAME**: Escolha um nome para sua instância (ex: `ofertas_amazon`, `bot_ofertas`)
- **WHATSAPP_GROUP_ID**: Deixe vazio por enquanto, vamos preencher no Passo 4

---

## 📱 Passo 3: Conectar WhatsApp

### 3.1. Criar e conectar instância

Execute o script de conexão:

```bash
python connect_instance.py
```

Este script irá:
1. ✅ Criar a instância na Evolution API
2. 📱 Exibir um QR Code no terminal
3. ⏳ Aguardar você escanear com o WhatsApp

### 3.2. Escanear QR Code

1. Abra o **WhatsApp** no seu celular
2. Toque em **Mais opções (⋮)** > **Aparelhos conectados**
3. Toque em **Conectar um aparelho**
4. **Escaneie o QR Code** que apareceu no terminal

### 3.3. Aguardar confirmação

O script irá detectar automaticamente quando a conexão for estabelecida e exibirá:

```
✅ CONECTADO COM SUCESSO!
```

---

## 🔍 Passo 4: Obter ID do Grupo WhatsApp

### 4.1. Listar grupos

Execute o script para listar seus grupos:

```bash
python get_group_id.py
```

### 4.2. Copiar ID do grupo

O script exibirá todos os seus grupos do WhatsApp:

```
📱 GRUPOS DO WHATSAPP ENCONTRADOS
================================================================================

1. Nome: Ofertas Tech
   ID: 120363123456789012@g.us
   Copie este ID para o arquivo .env:
   WHATSAPP_GROUP_ID=120363123456789012@g.us
--------------------------------------------------------------------------------

✅ Total de grupos encontrados: 1
```

### 4.3. Atualizar arquivo `.env`

Copie o ID do grupo desejado e cole no arquivo `.env`:

```env
WHATSAPP_GROUP_ID=120363123456789012@g.us
```

**💡 Dica:** O ID do grupo sempre termina com `@g.us`

---

## 🧪 Passo 5: Testar o Sistema

### 5.1. Executar testes

```bash
python test_system.py
```

Este script irá testar:
- ✅ Conexão com Evolution API
- ✅ Banco de dados
- ✅ (Opcional) Varredura de produtos
- ✅ (Opcional) Envio de mensagem de teste

### 5.2. Enviar mensagem de teste

Quando o script perguntar:

```
⚠️  Deseja enviar uma mensagem de teste para o grupo?
Digite 'sim' para continuar:
```

Digite `sim` e pressione Enter. Uma mensagem de teste será enviada para o grupo.

---

## 🎯 Passo 6: Executar o Sistema

### 6.1. Modo de produção

Para iniciar o monitoramento contínuo:

```bash
python main.py
```

O sistema irá:
1. 🔍 Fazer uma varredura inicial de produtos
2. 📊 Analisar quedas de preço
3. 📱 Enviar ofertas para o grupo (se encontrar)
4. ⏰ Repetir a cada X minutos (configurável)

### 6.2. Executar em background (opcional)

**Linux/Mac:**
```bash
nohup python main.py > ofertas.log 2>&1 &
```

**Para parar:**
```bash
ps aux | grep main.py
kill [PID]
```

---

## 📊 Monitoramento

### Ver logs em tempo real

```bash
tail -f deal_monitor.log
```

### Ver estatísticas

Os logs mostrarão:
- Número de produtos encontrados
- Ofertas com desconto
- Mensagens enviadas
- Erros (se houver)

---

## 🔧 Configurações Avançadas

### Ajustar threshold de desconto

No arquivo `.env`, altere:

```env
PRICE_DROP_THRESHOLD=15  # Apenas produtos com 15% ou mais de desconto
```

### Alterar frequência de verificação

```env
CHECK_INTERVAL_MINUTES=30  # Verifica a cada 30 minutos
```

### Limitar produtos por mensagem

```env
MAX_PRODUCTS_PER_MESSAGE=3  # Envia no máximo 3 produtos por vez
```

### Personalizar palavras-chave

Edite o arquivo `config.py` e modifique:

```python
SEARCH_KEYWORDS = [
    'iphone',
    'airpods',
    'kindle',
    'echo dot',
    # adicione mais...
]
```

---

## ❓ Solução de Problemas

### Erro: "Evolution API not connected"

**Solução:**
1. Verifique se a Evolution API está rodando: `http://localhost:8080`
2. Execute novamente: `python connect_instance.py`
3. Verifique se o QR Code foi escaneado

### Erro: "Amazon API credentials invalid"

**Solução:**
1. Verifique suas credenciais no arquivo `.env`
2. Confirme que a API está ativa em: https://webservices.amazon.com/paapi5/documentation/

### Nenhuma oferta encontrada

**Solução:**
1. Ajuste o `PRICE_DROP_THRESHOLD` para um valor menor (ex: 5)
2. Aguarde mais tempo para acumular histórico de preços
3. Execute `python test_system.py` para verificar produtos

### Mensagens não chegam no grupo

**Solução:**
1. Confirme o ID do grupo executando: `python get_group_id.py`
2. Verifique se o bot tem permissão para enviar mensagens no grupo
3. Execute `python test_system.py` e envie uma mensagem de teste

---

## 📚 Estrutura de Arquivos

```
.
├── main.py                 # Script principal
├── connect_instance.py     # Conectar WhatsApp
├── get_group_id.py         # Obter ID dos grupos
├── test_system.py          # Testar sistema
├── deal_monitor.py         # Lógica de monitoramento
├── amazon_client.py        # Cliente Amazon API
├── evolution_client.py     # Cliente Evolution API
├── database.py             # Banco de dados
├── config.py               # Configurações
├── .env                    # Variáveis de ambiente (CRIAR)
├── .env.example            # Exemplo de configuração
├── requirements.txt        # Dependências
├── products.db             # Banco de dados (criado automaticamente)
└── deal_monitor.log        # Logs (criado automaticamente)
```

---

## 🎉 Pronto!

Seu sistema está configurado e rodando! As ofertas serão enviadas automaticamente para o grupo do WhatsApp.

**Próximos passos:**
- Monitore os logs para acompanhar o funcionamento
- Ajuste as configurações conforme necessário
- Adicione mais palavras-chave de produtos que deseja monitorar

---

## 📞 Suporte

Se encontrar problemas:
1. Verifique os logs: `tail -f deal_monitor.log`
2. Execute os testes: `python test_system.py`
3. Revise este guia de configuração

**Boa sorte com suas ofertas! 🚀**
