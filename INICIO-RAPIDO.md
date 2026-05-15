# ⚡ Início Rápido - 5 Minutos

Guia super rápido para colocar o sistema funcionando.

## 🚀 Passo a Passo

### 1️⃣ Instalar (30 segundos)

```bash
cd "/Volumes/Storage Expansion/Windsurf/CascadeProjects/windsurf-project"
pip install -r requirements.txt
```

---

### 2️⃣ Configurar (1 minuto)

```bash
cp .env.example .env
nano .env  # ou use seu editor preferido
```

**Preencha apenas o essencial:**

```env
# Evolution API (sua instalação local)
EVOLUTION_API_URL=http://localhost:8080
EVOLUTION_API_KEY=B6D711FCDE4D4FD5936544120E713976
EVOLUTION_INSTANCE_NAME=ofertas_bot

# Amazon (obtenha em https://associados.amazon.com.br/)
AMAZON_ACCESS_KEY=sua_key
AMAZON_SECRET_KEY=sua_secret
AMAZON_PARTNER_TAG=seu_tag

# WhatsApp (vamos preencher no próximo passo)
WHATSAPP_GROUP_ID=
```

**💡 Dica:** Deixe `WHATSAPP_GROUP_ID` vazio por enquanto!

---

### 3️⃣ Conectar WhatsApp (1 minuto)

```bash
python connect_instance.py
```

1. ✅ Script cria a instância
2. 📱 QR Code aparece no terminal
3. 🔍 Abra WhatsApp > Aparelhos conectados > Escanear
4. ⏳ Aguarde "CONECTADO COM SUCESSO!"

---

### 4️⃣ Pegar ID do Grupo (30 segundos)

```bash
python get_group_id.py
```

**Saída:**
```
1. Nome: Ofertas Tech
   ID: 120363123456789012@g.us
   Copie este ID para o arquivo .env:
   WHATSAPP_GROUP_ID=120363123456789012@g.us
```

**Copie o ID** e cole no arquivo `.env`:

```env
WHATSAPP_GROUP_ID=120363123456789012@g.us
```

---

### 5️⃣ Testar (1 minuto)

```bash
python test_system.py
```

Quando perguntar sobre enviar mensagem de teste, digite `sim`.

**✅ Se a mensagem chegou no grupo, está tudo OK!**

---

### 6️⃣ Rodar! (5 segundos)

```bash
python main.py
```

**Pronto! 🎉** O sistema está monitorando e enviando ofertas automaticamente!

---

## 📊 O que acontece agora?

O sistema irá:

1. 🔍 **A cada 60 minutos** (configurável):
   - Buscar produtos tecnológicos na Amazon
   - Comparar preços com histórico
   - Detectar quedas de preço

2. 📱 **Quando encontrar ofertas** (desconto ≥ 10%):
   - Formatar mensagem bonita
   - Enviar para o grupo do WhatsApp
   - Salvar no banco para não repetir

3. 📝 **Registrar tudo** em logs:
   - `deal_monitor.log` - histórico completo
   - Console - status em tempo real

---

## 🎛️ Ajustes Rápidos

### Mudar frequência de verificação

Edite `.env`:
```env
CHECK_INTERVAL_MINUTES=30  # verifica a cada 30 min
```

### Ajustar desconto mínimo

```env
PRICE_DROP_THRESHOLD=15  # apenas 15% ou mais
```

### Limitar produtos por mensagem

```env
MAX_PRODUCTS_PER_MESSAGE=3  # máximo 3 produtos
```

---

## 🔍 Ver Logs

```bash
tail -f deal_monitor.log
```

---

## 🛑 Parar o Sistema

Pressione `Ctrl + C` no terminal onde o `main.py` está rodando.

---

## ❓ Problemas?

### Mensagem não chega no grupo

```bash
python test_system.py
```

Digite `sim` quando perguntar sobre enviar teste.

### WhatsApp desconectou

```bash
python connect_instance.py
```

Escaneie o QR Code novamente.

### Nenhuma oferta encontrada

É normal no início! O sistema precisa:
- Acumular histórico de preços (algumas horas)
- Encontrar produtos com desconto real

**Dica:** Reduza o threshold temporariamente:
```env
PRICE_DROP_THRESHOLD=5
```

---

## 📚 Quer saber mais?

- **Configuração detalhada:** [CONFIGURACAO.md](CONFIGURACAO.md)
- **Documentação completa:** [README.md](README.md)
- **API Evolution:** [EVO-API reference.md](EVO-API%20reference.md)

---

## ✅ Checklist Final

- [x] Dependências instaladas
- [x] Arquivo `.env` configurado
- [x] WhatsApp conectado
- [x] ID do grupo obtido
- [x] Teste enviado com sucesso
- [x] Sistema rodando

**🎉 Parabéns! Você está recebendo ofertas automáticas!**

---

**Tempo total:** ~5 minutos ⚡
