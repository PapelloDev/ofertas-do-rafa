# 📱 Integração WhatsApp - Ofertas do Rafa

## ✅ Implementação Completa

### 🎯 Funcionalidade

Ao **publicar um produto** no admin, o sistema **automaticamente**:

1. ✅ Salva o produto no JSON
2. ✅ Gera a página HTML do produto
3. ✅ **Envia mensagem para o grupo WhatsApp** 📲

---

## 🔧 Arquivos Criados

### 1. `send_product_whatsapp.py`
Script que formata e envia a mensagem do produto para o WhatsApp.

**Funcionalidades:**
- Formata mensagem bonita com emojis
- Inclui imagem do produto
- Mostra preço, desconto e economia
- Link para a página do produto no site

### 2. Endpoint na API
`POST /api/send-to-whatsapp`

**Payload:**
```json
{
  "asin": "B08XYZ123"
}
```

### 3. Integração no Frontend
Após publicar, chama automaticamente o endpoint de WhatsApp.

---

## 📨 Formato da Mensagem

```
🔥 *NOVA OFERTA!* 🔥

📦 *[Título do Produto]*
🏷️ Marca: [Marca]

💰 De: ~R$ 299,90~
✅ Por: *R$ 179,90*
📉 Desconto: *40% OFF*
💵 Economia: *R$ 120,00*

👉 *Ver oferta completa:*
https://ofertasdorafa.netlify.app/produto/B08XYZ123.html

⏰ _Oferta por tempo limitado!_
🤖 _Atualizado automaticamente_
```

**Com imagem do produto anexada!**

---

## ⚙️ Configuração Necessária

### 1. Variáveis de Ambiente (`.env`)

```bash
# Evolution API
EVOLUTION_API_URL=https://sua-api.evolution.com
EVOLUTION_API_KEY=sua-chave-api
EVOLUTION_INSTANCE_NAME=sua-instancia

# WhatsApp
WHATSAPP_GROUP_ID=5511999999999-1234567890@g.us
```

### 2. URL do Site (`site/data/produtos.json`)

```json
{
  "config": {
    "site_url": "https://ofertasdorafa.netlify.app"
  }
}
```

---

## 🚀 Como Funciona

### Fluxo Automático

```
1. Admin adiciona produto
   ↓
2. Clica "Publicar Produto"
   ↓
3. Sistema salva no JSON
   ↓
4. Gera página HTML
   ↓
5. 📲 ENVIA PARA WHATSAPP AUTOMATICAMENTE
   ↓
6. Mensagem aparece no grupo
```

### Tratamento de Erros

- ✅ Se WhatsApp falhar, **produto é publicado normalmente**
- ✅ Erro de WhatsApp não bloqueia publicação
- ✅ Logs detalhados no console do servidor

---

## 🎨 Emojis Dinâmicos

O emoji da mensagem muda baseado no desconto:

- **50%+ de desconto**: 🔥 (FOGO)
- **30-49% de desconto**: 💥 (EXPLOSÃO)
- **Menos de 30%**: ⚡ (RAIO)

---

## 🧪 Testar Manualmente

### Via Script

```bash
python send_product_whatsapp.py B08XYZ123
```

### Via API

```bash
curl -X POST http://localhost:5001/api/send-to-whatsapp \
  -H "Content-Type: application/json" \
  -d '{"asin":"B08XYZ123"}'
```

---

## 📊 Logs do Servidor

Quando envia para WhatsApp, você verá:

```
📤 Enviando para WhatsApp...
   Grupo: 5511999999999-1234567890@g.us
✅ Mensagem enviada com sucesso!
```

Ou em caso de erro:

```
❌ Evolution API não está conectada
```

---

## 🔍 Verificar Conexão

O sistema verifica automaticamente se o WhatsApp está conectado antes de enviar.

**Métodos:**
- `evolution_client.check_connection()` - Verifica status
- Retorna `True` se conectado, `False` caso contrário

---

## ⚠️ Importante

### Antes de Usar em Produção

1. ✅ Configure as variáveis de ambiente
2. ✅ Teste a conexão com Evolution API
3. ✅ Verifique o ID do grupo WhatsApp
4. ✅ Atualize a URL do site no JSON

### Limitações

- Requer Evolution API configurada e rodando
- Requer instância WhatsApp conectada
- Grupo deve existir e bot deve ser membro

---

## 🎯 Próximas Melhorias

- [ ] Opção de desabilitar envio automático
- [ ] Escolher múltiplos grupos
- [ ] Agendar envio para horário específico
- [ ] Preview da mensagem antes de enviar
- [ ] Estatísticas de envios

---

## 📚 Arquivos Relacionados

- `send_product_whatsapp.py` - Script de envio
- `evolution_client.py` - Cliente Evolution API
- `admin_api.py` - Endpoint `/api/send-to-whatsapp`
- `admin/assets/js/adicionar-produto.js` - Integração frontend
- `config.py` - Configurações

---

**Status**: ✅ **IMPLEMENTADO E FUNCIONAL**

Ao publicar um produto, ele será **automaticamente enviado para o grupo WhatsApp**! 🎉
