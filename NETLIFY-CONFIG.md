# 🚀 Configuração do Netlify

## 📋 Variáveis de Ambiente Necessárias

Para que a geração de ganchos com IA funcione em produção, você precisa configurar as seguintes variáveis de ambiente no Netlify:

### 1. Acesse o Dashboard do Netlify

1. Vá para [app.netlify.com](https://app.netlify.com)
2. Selecione seu site: **ofertas-do-rafa**
3. Clique em **Site settings**
4. No menu lateral, clique em **Environment variables**

### 2. Adicione as Variáveis

Clique em **Add a variable** e adicione cada uma das seguintes:

#### OPENAI_API_KEY
```
Key: OPENAI_API_KEY
Value: [SUA_CHAVE_OPENAI_AQUI]
Scopes: All scopes
```

**⚠️ IMPORTANTE:** Use sua chave real da OpenAI. Você pode obter uma em [platform.openai.com/api-keys](https://platform.openai.com/api-keys)

#### OPENAI_MODEL (Opcional)
```
Key: OPENAI_MODEL
Value: gpt-4o-mini
Scopes: All scopes
```

### 3. Salve e Faça Redeploy

1. Clique em **Save**
2. Vá para **Deploys**
3. Clique em **Trigger deploy** → **Clear cache and deploy site**

---

## ✅ Como Funciona

### Desenvolvimento Local
```
Admin → http://localhost:5001/api/generate-hook
         ↓
      Backend Python lê do .env local
```

### Produção (Netlify)
```
Admin → /.netlify/functions/generate-hook
         ↓
      Função Serverless lê variáveis de ambiente do Netlify
```

---

## 🔒 Segurança

✅ **Chave API não está mais no código**
✅ **Não está no JSON público**
✅ **Armazenada de forma segura no Netlify**
✅ **Não é exposta ao cliente**

---

## 🧪 Testar

### Após configurar:

1. Acesse: `https://ofertasdorafa.app.br/admin/adicionar-produto.html`
2. Preencha título e características
3. Clique em **✨ Gerar com IA**
4. Deve funcionar! ✅

---

## 🐛 Troubleshooting

### Erro: "Chave API não configurada"
- Verifique se adicionou `OPENAI_API_KEY` no Netlify
- Verifique se fez redeploy após adicionar
- Aguarde 1-2 minutos para propagação

### Erro: "Function not found"
- Verifique se o arquivo está em `site/netlify/functions/generate-hook.js`
- Verifique se `netlify.toml` tem `functions = "netlify/functions"`
- Faça redeploy

### Erro: "OpenAI API error"
- Verifique se a chave API está correta
- Verifique se a chave tem créditos
- Verifique se a chave não expirou

---

## 📝 Arquivos Importantes

```
site/
├── netlify/
│   └── functions/
│       ├── generate-hook.js    # Função serverless
│       └── package.json        # Dependências
└── netlify.toml                # Configuração do Netlify
```

---

## 🔄 Atualizar Chave API

Se precisar trocar a chave:

1. Netlify Dashboard → Site settings → Environment variables
2. Encontre `OPENAI_API_KEY`
3. Clique em **Edit**
4. Cole nova chave
5. Clique em **Save**
6. Faça redeploy

**Não precisa alterar código!** 🎉
