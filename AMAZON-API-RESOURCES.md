# 📦 Amazon Creators API - Resources Detalhados

Documentação completa de todos os resources (campos) disponíveis nas respostas da API.

---

## 📑 Índice de Resources

1. [OffersV2](#offersv2) - Preços, descontos, disponibilidade ⭐ **PRINCIPAL**
2. [ItemInfo](#iteminfo) - Informações do produto
3. [Images](#images) - Imagens do produto
4. [BrowseNodeInfo](#browsenodeinfo) - Categorias e rankings
5. [ParentASIN](#parentasin) - ASIN pai (variações)
6. [SearchRefinements](#searchrefinements) - Refinamentos dinâmicos
7. [VariationSummary](#variationsummary) - Resumo de variações

---

## 💰 OffersV2 ⭐

**Resource principal para preços, descontos e disponibilidade.**

### Estrutura Completa

```json
{
  "offersV2": {
    "listings": [{
      "availability": {
        "maxOrderQuantity": 30,
        "minOrderQuantity": 1,
        "message": "Em estoque",
        "type": "IN_STOCK"
      },
      "condition": {
        "value": "New",
        "subCondition": "Unknown",
        "conditionNote": ""
      },
      "dealDetails": {
        "accessType": "PRIME_EXCLUSIVE",
        "badge": "Oferta relâmpago",
        "startTime": "2026-05-14T08:00Z",
        "endTime": "2026-05-14T20:00Z",
        "percentClaimed": 45,
        "earlyAccessDurationInMilliseconds": 1800000
      },
      "isBuyBoxWinner": true,
      "merchantInfo": {
        "id": "ATVPDKIKX0DER",
        "name": "Amazon.com.br"
      },
      "price": {
        "money": {
          "amount": 179.90,
          "currency": "BRL",
          "displayAmount": "R$ 179,90"
        },
        "pricePerUnit": {
          "amount": 89.95,
          "currency": "BRL",
          "displayAmount": "R$ 89,95 / unidade"
        },
        "savingBasis": {
          "money": {
            "amount": 299.00,
            "currency": "BRL",
            "displayAmount": "R$ 299,00"
          },
          "savingBasisType": "LIST_PRICE",
          "savingBasisTypeLabel": "Preço de Lista"
        },
        "savings": {
          "money": {
            "amount": 119.10,
            "currency": "BRL",
            "displayAmount": "R$ 119,10"
          },
          "percentage": 40
        }
      },
      "type": "LIGHTNING_DEAL",
      "violatesMAP": false
    }]
  }
}
```

### Resources Disponíveis

| Resource | Descrição |
|----------|-----------|
| `offersV2.listings.price` | **Preço atual** (obrigatório para descontos) |
| `offersV2.listings.savingBasis` | **Preço original** (para calcular desconto) |
| `offersV2.listings.availability` | Disponibilidade em estoque |
| `offersV2.listings.condition` | Condição (Novo, Usado) |
| `offersV2.listings.dealDetails` | **Detalhes de promoções** |
| `offersV2.listings.isBuyBoxWinner` | Se é o vendedor principal |
| `offersV2.listings.merchantInfo` | Informações do vendedor |
| `offersV2.listings.type` | Tipo de oferta (LIGHTNING_DEAL, etc) |

### Availability Types

| Tipo | Descrição |
|------|-----------|
| `IN_STOCK` | Em estoque |
| `IN_STOCK_SCARCE` | Estoque limitado |
| `OUT_OF_STOCK` | Fora de estoque |
| `AVAILABLE_DATE` | Disponível em data futura |
| `PREORDER` | Pré-venda |
| `LEADTIME` | Disponível após prazo |
| `UNAVAILABLE` | Indisponível |
| `UNKNOWN` | Desconhecido |

### Deal Details (Promoções)

**AccessType:**
- `ALL` - Todos os clientes
- `PRIME_EXCLUSIVE` - Apenas Prime
- `PRIME_EARLY_ACCESS` - Prime primeiro, depois todos

**Badge Examples:**
- "Oferta por tempo limitado"
- "Com Prime"
- "Oferta Black Friday"
- "Termina em" (com countdown)

### Cálculo de Desconto

```python
def calculate_discount(listing):
    """Calcula desconto percentual"""
    price = listing.get('price', {})
    
    # Preço atual
    current = price.get('money', {}).get('amount', 0)
    
    # Preço original (savingBasis)
    saving_basis = price.get('savingBasis', {})
    original = saving_basis.get('money', {}).get('amount', 0)
    
    # Se não tem savingBasis, não tem desconto
    if not original or original <= current:
        return 0
    
    # Calcular
    discount = ((original - current) / original) * 100
    return round(discount, 1)
```

---

## 📝 ItemInfo

**Informações detalhadas do produto.**

### Sub-Resources

| Resource | Descrição |
|----------|-----------|
| `itemInfo.title` | **Título do produto** |
| `itemInfo.features` | **Características principais** |
| `itemInfo.byLineInfo` | Marca, fabricante |
| `itemInfo.productInfo` | Cor, tamanho, dimensões |
| `itemInfo.technicalInfo` | Especificações técnicas |
| `itemInfo.classifications` | Categoria, binding |
| `itemInfo.contentInfo` | Edição, idioma, páginas |
| `itemInfo.manufactureInfo` | Modelo, número de peça |
| `itemInfo.externalIds` | EAN, ISBN, UPC |
| `itemInfo.tradeInInfo` | Informações de troca |

### Exemplo - Title

```json
{
  "itemInfo": {
    "title": {
      "displayValue": "Fone Bluetooth JBL Tune 510BT",
      "label": "Title",
      "locale": "pt_BR"
    }
  }
}
```

### Exemplo - Features

```json
{
  "itemInfo": {
    "features": {
      "displayValues": [
        "Bateria de até 40 horas",
        "Bluetooth 5.0",
        "Dobrável e portátil",
        "Controles integrados"
      ],
      "label": "Features",
      "locale": "pt_BR"
    }
  }
}
```

### Exemplo - ByLineInfo

```json
{
  "itemInfo": {
    "byLineInfo": {
      "brand": {
        "displayValue": "JBL",
        "label": "Brand",
        "locale": "pt_BR"
      },
      "manufacturer": {
        "displayValue": "Harman",
        "label": "Manufacturer",
        "locale": "pt_BR"
      }
    }
  }
}
```

---

## 🖼️ Images

**URLs de imagens em diferentes tamanhos.**

### Tamanhos Disponíveis

| Resource | Tamanho | Uso |
|----------|---------|-----|
| `images.primary.small` | 75px | Thumbnails |
| `images.primary.medium` | 160px | Listas |
| `images.primary.large` | 500px | **Detalhes** ⭐ |
| `images.primary.hiRes` | Original | Alta resolução |
| `images.variants.large` | 500px | Imagens alternativas |

### Estrutura

```json
{
  "images": {
    "primary": {
      "large": {
        "url": "https://m.media-amazon.com/images/I/41abc._SL500_.jpg",
        "height": 500,
        "width": 500
      }
    },
    "variants": [
      {
        "large": {
          "url": "https://m.media-amazon.com/images/I/51xyz._SL500_.jpg",
          "height": 500,
          "width": 500
        }
      }
    ]
  }
}
```

### Formato da URL

```
https://m.media-amazon.com/images/I/41abc._SL500_.jpg
                                              ^^^^
                                              Tamanho
```

- `_SL75_` - Small (75px)
- `_SL160_` - Medium (160px)
- `_SL500_` - Large (500px)
- Sem sufixo - Original

---

## 🗂️ BrowseNodeInfo

**Categorias e rankings de vendas.**

### Resources

| Resource | Descrição |
|----------|-----------|
| `browseNodeInfo.browseNodes` | Categorias do produto |
| `browseNodeInfo.browseNodes.ancestor` | Hierarquia completa |
| `browseNodeInfo.browseNodes.salesRank` | Ranking na categoria |
| `browseNodeInfo.websiteSalesRank` | Ranking geral do site |

### Exemplo - BrowseNodes

```json
{
  "browseNodeInfo": {
    "browseNodes": [
      {
        "id": "16285269011",
        "displayName": "Fones de Ouvido",
        "contextFreeName": "Fones de Ouvido Eletrônicos",
        "isRoot": false,
        "salesRank": 15
      }
    ]
  }
}
```

### Exemplo - WebsiteSalesRank

```json
{
  "browseNodeInfo": {
    "websiteSalesRank": {
      "displayName": "Eletrônicos",
      "contextFreeName": "Eletrônicos",
      "salesRank": 1247
    }
  }
}
```

### Hierarquia (Ancestor)

```json
{
  "browseNodes": [{
    "id": "16285269011",
    "displayName": "Fones de Ouvido",
    "ancestor": {
      "id": "16243663011",
      "displayName": "Eletrônicos",
      "ancestor": {
        "id": "1",
        "displayName": "Todas as Categorias"
      }
    }
  }]
}
```

---

## 🎨 ParentASIN

**ASIN pai para produtos com variações.**

### Uso

```json
{
  "asin": "B08XYZ123",
  "parentASIN": "B07ABC456"
}
```

**Quando usar:**
- Produto tem variações (cores, tamanhos)
- Quer buscar todas as variações
- Quer agrupar produtos relacionados

---

## 🔍 SearchRefinements

**Refinamentos dinâmicos para busca.**

### Tipos de Refinements

1. **SearchIndex** - Categorias relevantes (quando busca em "All")
2. **BrowseNode** - Subcategorias (quando busca em categoria específica)
3. **OtherRefinements** - Filtros dinâmicos (Brand, Author, Actor, Artist)

### Exemplo - SearchIndex

```json
{
  "searchRefinements": {
    "searchIndex": {
      "id": "SearchIndex",
      "displayName": "Departamento",
      "bins": [
        {
          "id": "Electronics",
          "displayName": "Eletrônicos"
        },
        {
          "id": "Computers",
          "displayName": "Computadores"
        }
      ]
    }
  }
}
```

### Exemplo - Brand Refinement

```json
{
  "searchRefinements": {
    "otherRefinements": [{
      "id": "Brand",
      "displayName": "Marca",
      "bins": [
        {
          "id": "JBL",
          "displayName": "JBL"
        },
        {
          "id": "Sony",
          "displayName": "Sony"
        }
      ]
    }]
  }
}
```

---

## 🎯 VariationSummary

**Resumo de variações de produto.**

### Resources

| Resource | Descrição |
|----------|-----------|
| `variationSummary.price.highestPrice` | Maior preço entre variações |
| `variationSummary.price.lowestPrice` | Menor preço entre variações |
| `variationSummary.variationDimension` | Dimensões (cor, tamanho, etc) |

### Exemplo Completo

```json
{
  "variationSummary": {
    "variationCount": 13,
    "pageCount": 2,
    "price": {
      "highestPrice": {
        "amount": 189.90,
        "currency": "BRL",
        "displayAmount": "R$ 189,90"
      },
      "lowestPrice": {
        "amount": 99.90,
        "currency": "BRL",
        "displayAmount": "R$ 99,90"
      }
    },
    "variationDimensions": [
      {
        "name": "color_name",
        "displayName": "Cor",
        "values": ["Preto", "Branco", "Azul", "Vermelho"]
      },
      {
        "name": "size_name",
        "displayName": "Tamanho",
        "values": ["P", "M", "G", "GG"]
      }
    ]
  }
}
```

---

## 🎯 Resources Recomendados para Nosso Sistema

### Para SearchItems (Buscar Ofertas)

```json
{
  "resources": [
    "images.primary.large",
    "itemInfo.title",
    "itemInfo.features",
    "offersV2.listings.price",
    "offersV2.listings.savingBasis",
    "offersV2.listings.availability",
    "offersV2.listings.dealDetails"
  ]
}
```

### Para GetItems (Verificar Detalhes)

```json
{
  "resources": [
    "images.primary.large",
    "itemInfo.title",
    "itemInfo.byLineInfo",
    "offersV2.listings.price",
    "offersV2.listings.savingBasis",
    "browseNodeInfo.browseNodes"
  ]
}
```

---

## 📊 Mapeamento OffersV1 → OffersV2

Para quem migra da API antiga:

| OffersV1 | OffersV2 |
|----------|----------|
| `Offers.Listings.Price.Amount` | `OffersV2.Listings.Price.Money.Amount` |
| `Offers.Listings.SavingBasis.Amount` | `OffersV2.Listings.Price.SavingBasis.Money.Amount` |
| `Offers.Listings.Availability` | `OffersV2.Listings.Availability` |
| `Offers.Listings.Condition` | `OffersV2.Listings.Condition` |
| `Offers.Summaries` | ❌ Não disponível |
| `Offers.Listings.DeliveryInfo` | ❌ Não disponível |
| `Offers.Listings.Promotions` | ❌ Não disponível |
| N/A | ✅ `OffersV2.Listings.DealDetails` (novo) |
| N/A | ✅ `OffersV2.Listings.Price.Savings` (novo) |

---

## ⚠️ Pontos Importantes

1. **savingBasis** - Nem sempre presente (produtos sem desconto)
2. **dealDetails** - Só presente se houver promoção ativa
3. **isBuyBoxWinner** - Indica a melhor oferta (recomendada pela Amazon)
4. **Preços** - Sempre em formato decimal (179.90, não 17990)
5. **Images** - Primary é a imagem principal, Variants são alternativas
6. **SalesRank** - Menor = melhor posição
7. **Availability.Type** - Sempre verificar antes de mostrar produto

---

## 💡 Dicas de Uso

### 1. Verificar Disponibilidade

```python
def is_available(listing):
    availability = listing.get('availability', {})
    return availability.get('type') == 'IN_STOCK'
```

### 2. Extrair Preço com Desconto

```python
def get_prices(listing):
    price = listing.get('price', {})
    
    current = price.get('money', {}).get('amount')
    original = price.get('savingBasis', {}).get('money', {}).get('amount')
    
    return {
        'current': current,
        'original': original or current,
        'has_discount': bool(original and original > current)
    }
```

### 3. Verificar se é Promoção

```python
def has_deal(listing):
    return 'dealDetails' in listing
```

---

**Última atualização:** 14 de Maio de 2026
