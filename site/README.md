# 🔥 Ofertas do Rafa - Site

Site estático para exibir ofertas de produtos Amazon com links de afiliados.

## 🎨 Identidade Visual

- **Logo**: Ofertas do Rafa
- **Cores**:
  - Primary: `#1A5F5F` (Verde-azulado)
  - Secondary: `#F5A623` (Laranja)
  - Success: `#00A650` (Verde desconto)
- **Slogan**: "Ofertas Cuidadosamente Curadas"

## 📂 Estrutura

```
site/
├── index.html              # Página principal
├── categoria/              # Páginas por categoria
│   ├── eletronicos.html
│   └── corrida.html
├── produto/                # Páginas individuais (geradas dinamicamente)
├── assets/
│   ├── css/style.css      # Estilos customizados
│   ├── js/main.js         # JavaScript principal
│   └── images/logo/       # Logo e assets
└── data/
    └── produtos.json      # Dados dos produtos
```

## 🚀 Como Usar

### Desenvolvimento Local

```bash
# Na raiz do projeto
python serve_site.py
```

Acesse: http://localhost:8000

### Adicionar Produtos

Edite `data/produtos.json`:

```json
{
  "produtos": [
    {
      "asin": "B08ABC123",
      "titulo": "Nome do Produto",
      "descricao": "Descrição...",
      "categoria": "eletronicos",
      "preco_original": 299.90,
      "preco_atual": 179.90,
      "desconto_percent": 40,
      "imagem_url": "https://...",
      "brand": "Marca",
      "features": ["Feature 1", "Feature 2"],
      "link_afiliado": "https://amazon.com.br/dp/B08ABC123?tag=seu-tag",
      "ativo": true
    }
  ]
}
```

### Deploy

#### Netlify (Recomendado)

1. Conecte o repositório Git
2. Configure:
   - Build command: (vazio)
   - Publish directory: `site`
3. Deploy!

#### Vercel

1. Conecte o repositório Git
2. Configure:
   - Framework Preset: Other
   - Root Directory: `site`
3. Deploy!

## 📱 Categorias

- **Eletrônicos** 📱: Smartphones, tablets, gadgets
- **Itens de Corrida** 🏃: Tênis, roupas, acessórios

## ⚖️ Aviso de Afiliados

O site inclui aviso de programa de afiliados conforme requisitos da Amazon:
- Visível no footer de todas as páginas
- Informa sobre comissões de afiliados
- Transparente com os usuários

## 🔧 Tecnologias

- HTML5
- TailwindCSS (via CDN)
- Vanilla JavaScript
- JSON para dados
