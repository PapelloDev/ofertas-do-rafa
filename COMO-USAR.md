# 🎯 Como Usar - Ofertas do Rafa

## 📌 Status Atual

**⚠️ IMPORTANTE**: A busca automática de produtos via API da Amazon está **DESATIVADA** até você conseguir 10 vendas para ser qualificado no programa de afiliados.

Por enquanto, você vai adicionar produtos **manualmente** através da interface admin.

---

## 🚀 Iniciar o Sistema

### Opção 1: Script Automático (Recomendado)
```bash
./start_interfaces.sh
```

### Opção 2: Manual
```bash
# Terminal 1 - API Admin
./venv/bin/python admin_api.py

# Terminal 2 - Servidor do Site
./venv/bin/python serve_site.py
```

---

## 🌐 Acessar as Interfaces

Após iniciar, você terá acesso a:

### 1. **Site Público** 
- URL: http://localhost:8000
- Para visitantes verem as ofertas que você publicar

### 2. **Painel Admin**
- URL: http://localhost:8000/admin/login.html
- Para você adicionar e gerenciar produtos

### 3. **API Backend**
- URL: http://localhost:5001
- Usada pelo admin para processar produtos

---

## 📝 Como Adicionar Produtos

1. Acesse o **Admin**: http://localhost:8000/admin/login.html

2. Faça login (se necessário)

3. Vá em **"Adicionar Produto"**

4. Cole o link do produto da Amazon (pode ser link encurtado amzn.to)

5. O sistema vai:
   - Extrair dados do produto (título, preço, imagem)
   - Adicionar seu tag de afiliado
   - Gerar página do produto
   - Permitir enviar para WhatsApp

---

## 📱 Enviar para WhatsApp

Após adicionar um produto no admin, você pode:

1. Clicar em **"Enviar para WhatsApp"**
2. O produto será enviado automaticamente para o grupo configurado
3. Mensagem inclui:
   - Imagem do produto
   - Título e descrição
   - Preço com desconto
   - Link de afiliado

---

## ⚙️ Configurações

### Arquivo `.env`

```bash
# Evolution API (WhatsApp)
EVOLUTION_API_URL=http://localhost:8080
EVOLUTION_API_KEY=sua_api_key
EVOLUTION_INSTANCE_NAME=amazon_gadgets
WHATSAPP_GROUP_ID=120363427077139746@g.us

# Amazon Afiliados
AMAZON_PARTNER_TAG=rahsinc-20
AMAZON_MARKETPLACE=www.amazon.com.br
```

---

## 🛑 Parar o Sistema

Pressione **Ctrl+C** no terminal onde os servidores estão rodando.

Se usou o script automático, ele para tudo de uma vez.

---

## 📂 Estrutura de Pastas

```
ofertas-do-rafa/
├── admin/              # Interface de administração
│   ├── login.html
│   ├── index.html
│   ├── adicionar-produto.html
│   └── categorias.html
├── site/               # Site público
│   ├── index.html
│   ├── data/
│   │   └── produtos.json
│   └── produto/        # Páginas de produtos geradas
├── admin_api.py        # API backend
├── serve_site.py       # Servidor HTTP
└── evolution_client.py # Cliente WhatsApp
```

---

## 🔄 Próximos Passos

### Quando conseguir 10 vendas:

1. Você será qualificado na Amazon Product Advertising API
2. Poderá ativar a busca automática de produtos
3. O sistema vai monitorar ofertas automaticamente
4. Produtos com desconto serão enviados para o grupo

### Por enquanto:

✅ Use o admin para adicionar produtos manualmente  
✅ Compartilhe no WhatsApp  
✅ Foque em conseguir as 10 primeiras vendas  
✅ Escolha produtos com bom desconto e relevantes  

---

## 💡 Dicas

- **Produtos que convertem bem**:
  - Fones bluetooth (sempre populares)
  - Carregadores rápidos
  - Power banks
  - Smartwatches
  - Acessórios de celular

- **Como encontrar bons descontos**:
  - Acesse https://www.amazon.com.br/gp/goldbox (Ofertas do Dia)
  - Filtre por categoria "Eletrônicos"
  - Procure descontos acima de 20%

- **Frequência de posts**:
  - 1-3 produtos por dia é ideal
  - Não faça spam no grupo
  - Qualidade > Quantidade

---

## 🆘 Problemas Comuns

### "Evolution API não conectada"
- Verifique se a Evolution API está rodando
- Confirme URL e API Key no `.env`

### "Não consegue extrair dados do produto"
- Alguns produtos da Amazon bloqueiam scraping
- Tente com outro produto
- Use links diretos (não encurtados) quando possível

### "Site não carrega"
- Verifique se os servidores estão rodando
- Confirme que as portas 5001 e 8000 estão livres

---

**Última atualização**: 15 de Maio de 2026
