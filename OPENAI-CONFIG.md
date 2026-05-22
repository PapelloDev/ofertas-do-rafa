# 🤖 Configuração OpenAI (Geração de Ganchos)

## 🔒 Configuração Segura Local

A chave API da OpenAI é armazenada de forma **segura** no arquivo `.env` local, que **nunca** é commitado no Git.

---

## ⚙️ Como Configurar

### 1. Abra o arquivo `.env`

```bash
nano .env
```

Ou abra no seu editor de código.

### 2. Localize a seção OpenAI

```bash
# OpenAI API (para gerar ganchos de venda)
OPENAI_API_KEY=sua_chave_aqui
OPENAI_MODEL=gpt-4o-mini
```

### 3. Cole sua chave API

```bash
OPENAI_API_KEY=sk-proj-...
OPENAI_MODEL=gpt-4o-mini
```

### 4. Salve o arquivo

`Ctrl+O` (nano) ou `Cmd+S` (editor)

### 5. Reinicie o servidor

```bash
# Parar
Ctrl+C

# Iniciar novamente
./start_interfaces.sh
```

---

## 🧪 Como Testar

### 1. Acesse Adicionar Produto
```
http://localhost:8000/admin/adicionar-produto.html
```

### 2. Preencha os Campos
```
Título: Fone Bluetooth Premium
Características:
- Bluetooth 5.0
- Bateria 40h
- Cancelamento de ruído
```

### 3. Clique em "✨ Gerar com IA"

**Deve funcionar!** ✅

---

## 🔑 Onde Obter Chave API

1. Acesse: https://platform.openai.com/api-keys
2. Faça login na sua conta OpenAI
3. Clique em **Create new secret key**
4. Copie a chave (começa com `sk-proj-...`)
5. Cole no `.env`

---

## 💰 Modelos Disponíveis

### **gpt-4o-mini** (Recomendado)
- ✅ Rápido
- ✅ Barato (~$0.15 por 1000 ganchos)
- ✅ Qualidade excelente
- ✅ Ideal para produção

### **gpt-4o**
- ⚡ Mais inteligente
- 💰 Mais caro (~$2.50 por 1000 ganchos)
- 🎯 Para casos especiais

### **gpt-3.5-turbo**
- 💵 Mais barato
- ⚠️ Qualidade inferior
- 🔧 Para testes

---

## 🔒 Segurança

### ✅ **O Que Está Protegido:**

1. **Chave API no `.env`** - Nunca vai para o Git
2. **`.env` no `.gitignore`** - Impossível commitar acidentalmente
3. **Apenas servidor local acessa** - Não exposto publicamente
4. **Não está no JSON** - Não vai para produção
5. **Não está no admin** - Não pode ser editado via interface

### ✅ **Como Funciona:**

```
1. Você edita .env localmente
   ↓
2. Servidor Python lê do .env
   ↓
3. Chama OpenAI API
   ↓
4. Retorna gancho gerado
   ↓
5. Chave NUNCA sai do servidor local
```

---

## 🐛 Troubleshooting

### **Erro: "Chave API não configurada"**

**Solução:**
```bash
# 1. Verifique se .env existe
ls -la .env

# 2. Verifique se tem a chave
cat .env | grep OPENAI

# 3. Adicione se não tiver
echo "OPENAI_API_KEY=sk-proj-..." >> .env

# 4. Reinicie servidor
./start_interfaces.sh
```

### **Erro: "OpenAI API error"**

**Causas possíveis:**
1. Chave inválida ou expirada
2. Sem créditos na conta OpenAI
3. Modelo não disponível

**Solução:**
```bash
# Teste a chave em: https://platform.openai.com/playground
# Verifique créditos em: https://platform.openai.com/usage
```

### **Gancho não aparece**

**Solução:**
```bash
# 1. Abra console do navegador (F12)
# 2. Veja se há erros
# 3. Verifique se servidor está rodando
curl http://localhost:5001/api/generate-hook
```

---

## 📝 Exemplo de .env Completo

```bash
# Amazon Creators API Credentials
AMAZON_CREDENTIAL_ID=amzn1.application-oa2-client...
AMAZON_CREDENTIAL_SECRET=amzn1.oa2-cs.v1...
AMAZON_PARTNER_TAG=seu-tag-20

# Evolution API (WhatsApp)
EVOLUTION_API_URL=http://localhost:8080
EVOLUTION_API_KEY=sua_chave
EVOLUTION_INSTANCE_NAME=amazon_gadgets
WHATSAPP_GROUP_ID=120363...@g.us

# GitHub Deploy
GITHUB_TOKEN=ghp_...
GITHUB_REPO=SeuUser/seu-repo
GITHUB_BRANCH=main

# OpenAI API (para gerar ganchos de venda)
OPENAI_API_KEY=sk-proj-...
OPENAI_MODEL=gpt-4o-mini
```

---

## 🔄 Atualizar Chave

Se precisar trocar a chave:

```bash
# 1. Edite .env
nano .env

# 2. Substitua a chave
OPENAI_API_KEY=nova_chave_aqui

# 3. Salve (Ctrl+O)

# 4. Reinicie servidor
./start_interfaces.sh
```

**Não precisa alterar código!** 🎉

---

## ✅ Checklist

- [ ] Arquivo `.env` existe
- [ ] `OPENAI_API_KEY` configurada
- [ ] `OPENAI_MODEL` definido (opcional)
- [ ] Servidor reiniciado
- [ ] Testado geração de gancho
- [ ] ✅ Funcionando!

---

## 📚 Mais Informações

- **OpenAI Pricing:** https://openai.com/pricing
- **API Keys:** https://platform.openai.com/api-keys
- **Usage:** https://platform.openai.com/usage
- **Docs:** https://platform.openai.com/docs
