# 🔐 Guia do Admin - Ofertas do Rafa

Sistema de administração para gerenciar produtos do site com extração automática de dados da Amazon.

---

## 🚀 Como Usar

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

Novas dependências adicionadas:
- `flask` - Framework web para API
- `flask-cors` - Permitir requisições cross-origin
- `beautifulsoup4` - Parser HTML para extrair dados
- `lxml` - Parser rápido para BeautifulSoup

### 2. Iniciar Servidor Backend

```bash
python admin_api.py
```

O servidor iniciará em: **http://localhost:5000**

### 3. Acessar Interface Admin

Abra no navegador: **http://localhost:8000/admin/login.html**

**Senha padrão**: `ofertas2026`

---

## 📝 Fluxo de Trabalho

### Adicionar Produto

1. **Login** em `/admin/login.html`
2. **Dashboard** - Ver estatísticas
3. **Adicionar Produto**:
   - Cole o link de afiliado (ex: `https://amzn.to/4tAHaQS`)
   - Selecione a categoria (Eletrônicos ou Corrida)
   - Clique em "Extrair Dados"
   - Sistema busca automaticamente:
     - ✅ Título
     - ✅ Descrição
     - ✅ Preço original e atual
     - ✅ Desconto %
     - ✅ Imagem principal
     - ✅ Marca
     - ✅ Características
   - Revise o preview
   - Clique em "Publicar Produto"

4. **Resultado**:
   - Produto salvo em `site/data/produtos.json`
   - Página HTML gerada em `site/produto/{ASIN}.html`
   - Produto aparece no site automaticamente

---

## 🔧 Arquitetura

### Frontend (Admin)
```
admin/
├── login.html              # Página de login
├── index.html              # Dashboard
├── adicionar-produto.html  # Formulário de adicionar
├── listar-produtos.html    # Lista de produtos (TODO)
└── assets/
    └── js/
        └── adicionar-produto.js  # Lógica de extração
```

### Backend (API)
```
admin_api.py                # API Flask
```

**Endpoints**:
- `POST /api/extract-product` - Extrai dados da Amazon
- `POST /api/save-product` - Salva produto no JSON
- `POST /api/generate-product-page` - Gera página HTML

---

## 🔍 Como Funciona a Extração

### 1. Extração do ASIN
O sistema aceita vários formatos de URL:
- `https://amzn.to/4tAHaQS` (link curto)
- `https://www.amazon.com.br/dp/B08XYZ123`
- `https://www.amazon.com.br/produto/dp/B08XYZ123`

### 2. Scraping da Página
- Faz requisição HTTP para `amazon.com.br/dp/{ASIN}`
- Usa BeautifulSoup para parsear HTML
- Extrai dados com seletores CSS específicos

### 3. Dados Extraídos
- **Título**: `#productTitle`
- **Preço Atual**: `.a-price-whole`
- **Preço Original**: `.a-text-price`
- **Imagem**: `#landingImage` (alta resolução)
- **Marca**: `#bylineInfo`
- **Features**: `#feature-bullets li`

### 4. Processamento
- Calcula desconto automaticamente
- Formata preços (R$ X,XX)
- Limpa textos (remove espaços, caracteres especiais)
- Valida dados obrigatórios

### 5. Geração de Página
- Template HTML com dados do produto
- SEO otimizado (meta tags, Open Graph)
- Responsivo e acessível
- Link de afiliado integrado

---

## 🔐 Segurança

### Senha de Admin
**Localização**: `admin/login.html` (linha ~56)

```javascript
const ADMIN_PASSWORD = 'ofertas2026';
```

**⚠️ IMPORTANTE**: Em produção, use autenticação real:
- Backend com JWT
- Banco de dados de usuários
- Hash de senhas (bcrypt)
- Rate limiting

### Sessão
- Armazenada em `sessionStorage`
- Expira ao fechar navegador
- Verificada em todas as páginas admin

---

## 📊 Estrutura de Dados

### Produto no JSON
```json
{
  "asin": "B08XYZ123",
  "titulo": "Fone JBL Tune 510BT",
  "descricao": "Fone de ouvido sem fio...",
  "categoria": "eletronicos",
  "preco_original": 299.90,
  "preco_atual": 179.90,
  "desconto_percent": 40.0,
  "imagem_url": "https://m.media-amazon.com/...",
  "brand": "JBL",
  "features": [
    "Bluetooth 5.0",
    "40h de bateria"
  ],
  "link_afiliado": "https://amzn.to/4tAHaQS",
  "ativo": true,
  "data_adicao": "2026-05-14T17:50:00Z",
  "data_atualizacao": "2026-05-14T17:50:00Z"
}
```

---

## 🐛 Troubleshooting

### Erro: "Servidor backend não está rodando"
**Solução**: Inicie o servidor backend
```bash
python admin_api.py
```

### Erro: "Não foi possível extrair dados"
**Causas possíveis**:
1. Link inválido ou ASIN incorreto
2. Produto não disponível na Amazon
3. Amazon bloqueou o scraping (rate limit)

**Soluções**:
- Verifique o link
- Aguarde alguns segundos e tente novamente
- Use VPN se necessário

### Erro: "Senha incorreta"
**Solução**: Use a senha padrão `ofertas2026`

### Produto não aparece no site
**Verificações**:
1. Produto foi salvo? (verifique `site/data/produtos.json`)
2. Página foi gerada? (verifique `site/produto/{ASIN}.html`)
3. Recarregue a página do site (Ctrl+F5)

---

## 🎯 Próximas Melhorias

- [ ] **Lista de Produtos**: Página para editar/excluir produtos
- [ ] **Autenticação Real**: JWT, banco de dados
- [ ] **Upload de Imagens**: Hospedar imagens localmente
- [ ] **Agendamento**: Atualizar preços automaticamente
- [ ] **Analytics**: Tracking de cliques nos links
- [ ] **Multi-usuário**: Diferentes níveis de acesso
- [ ] **API Pública**: Integração com outros sistemas

---

## 📚 Recursos

- **Flask Docs**: https://flask.palletsprojects.com/
- **BeautifulSoup Docs**: https://www.crummy.com/software/BeautifulSoup/
- **Amazon Associates**: https://associados.amazon.com.br/

---

## ⚖️ Avisos Legais

- ✅ Scraping para uso pessoal é permitido
- ✅ Respeite os termos de serviço da Amazon
- ✅ Não faça scraping excessivo (rate limiting)
- ✅ Use User-Agent apropriado
- ✅ Mantenha aviso de afiliados visível

---

**Status**: ✅ Sistema Admin Completo e Funcional!
