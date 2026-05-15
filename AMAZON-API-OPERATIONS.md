# 🔧 Amazon Creators API - Operações Detalhadas

Documentação completa de todas as operações disponíveis na Creators API.

---

## 📑 Índice de Operações

1. [SearchItems](#searchitems) - Buscar produtos por palavra-chave ⭐ **PRINCIPAL**
2. [GetItems](#getitems) - Obter detalhes por ASIN
3. [GetBrowseNodes](#getbrowsenodes) - Obter categorias
4. [GetVariations](#getvariations) - Obter variações de produto

---

## 🔍 SearchItems ⭐

**Operação principal para buscar produtos na Amazon.**

### Endpoint
```
POST https://creatorsapi.amazon/catalog/v1/searchItems
```

### Descrição
Busca produtos baseado em query de pesquisa. Retorna até **10 itens por request**.

### Parâmetros Obrigatórios

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `partnerTag` | String | Seu Partner Tag |
| `marketplace` | String | Marketplace (ex: www.amazon.com.br) |
| **Um dos seguintes:** | | |
| `keywords` | String | Palavra-chave de busca |
| `actor` | String | Nome do ator |
| `artist` | String | Nome do artista |
| `author` | String | Nome do autor |
| `brand` | String | Nome da marca |
| `title` | String | Título do produto |

### Parâmetros Opcionais Importantes

| Parâmetro | Tipo | Valores | Descrição |
|-----------|------|---------|-----------|
| `itemCount` | Integer | 1-10 | Número de itens (padrão: 10) |
| `itemPage` | Integer | 1-10 | Página de resultados (padrão: 1) |
| `sortBy` | String | Ver tabela | Ordenação dos resultados |
| `searchIndex` | String | Ver tabela | Categoria de busca |
| `browseNodeId` | String | ID | Buscar em categoria específica |
| `minPrice` | Integer | | Preço mínimo (centavos) |
| `maxPrice` | Integer | | Preço máximo (centavos) |
| `minSavingPercent` | Integer | 1-99 | Desconto mínimo (%) |
| `minReviewsRating` | Integer | 1-4 | Avaliação mínima |
| `condition` | String | Any, New | Condição do produto |
| `availability` | String | Available, IncludeOutOfStock | Disponibilidade |
| `deliveryFlags` | Array | Prime, FreeShipping, etc | Filtros de entrega |

### SortBy - Ordenação

| Valor | Descrição |
|-------|-----------|
| `Relevance` | Relevância (padrão) |
| `Price:LowToHigh` | Menor preço primeiro |
| `Price:HighToLow` | Maior preço primeiro |
| `AvgCustomerReviews` | Melhor avaliado |
| `NewestArrivals` | Mais recentes |
| `Featured` | Destacados |

### SearchIndex - Categorias Brasil

| Categoria | Valor |
|-----------|-------|
| Todas | `All` |
| Eletrônicos | `Electronics` |
| Computadores | `Computers` |
| Livros | `Books` |
| Casa e Cozinha | `HomeAndKitchen` |
| Esportes | `SportingGoods` |
| Brinquedos | `Toys` |
| Video Games | `VideoGames` |

### Resources Disponíveis

```json
{
  "resources": [
    "images.primary.large",
    "itemInfo.title",
    "itemInfo.features",
    "offersV2.listings.price",
    "offersV2.listings.savingBasis",
    "offersV2.listings.availability",
    "offersV2.listings.dealDetails",
    "browseNodeInfo.browseNodes",
    "parentASIN"
  ]
}
```

### Exemplo de Request - Busca Simples

```json
{
  "partnerTag": "seu-tag-20",
  "marketplace": "www.amazon.com.br",
  "keywords": "fone bluetooth",
  "itemCount": 10,
  "resources": [
    "images.primary.large",
    "itemInfo.title",
    "offersV2.listings.price",
    "offersV2.listings.savingBasis"
  ]
}
```

### Exemplo de Request - Busca Avançada

```json
{
  "partnerTag": "seu-tag-20",
  "marketplace": "www.amazon.com.br",
  "keywords": "smartwatch",
  "searchIndex": "Electronics",
  "sortBy": "Price:LowToHigh",
  "minSavingPercent": 20,
  "minReviewsRating": 4,
  "condition": "New",
  "deliveryFlags": ["Prime"],
  "itemCount": 10,
  "resources": [
    "images.primary.large",
    "itemInfo.title",
    "itemInfo.features",
    "offersV2.listings.price",
    "offersV2.listings.savingBasis",
    "offersV2.listings.dealDetails"
  ]
}
```

### Exemplo de Response

```json
{
  "searchResult": {
    "totalResultCount": 1453,
    "searchURL": "https://www.amazon.com.br/s/?field-keywords=fone+bluetooth&tag=seu-tag-20",
    "items": [
      {
        "asin": "B08XYZ123",
        "detailPageURL": "https://www.amazon.com.br/dp/B08XYZ123?tag=seu-tag-20",
        "images": {
          "primary": {
            "large": {
              "url": "https://m.media-amazon.com/images/I/41abc.jpg",
              "height": 500,
              "width": 500
            }
          }
        },
        "itemInfo": {
          "title": {
            "displayValue": "Fone Bluetooth JBL Tune 510BT",
            "locale": "pt_BR"
          }
        },
        "offersV2": {
          "listings": [{
            "price": {
              "money": {
                "amount": 179.90,
                "currency": "BRL",
                "displayAmount": "R$ 179,90"
              },
              "savingBasis": {
                "money": {
                  "amount": 299.00,
                  "currency": "BRL",
                  "displayAmount": "R$ 299,00"
                }
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
            "availability": {
              "type": "IN_STOCK",
              "message": "Em estoque"
            },
            "dealDetails": {
              "accessType": "OPEN",
              "percentClaimed": 45
            }
          }]
        }
      }
    ]
  }
}
```

---

## 📦 GetItems

**Obter detalhes de produtos específicos por ASIN.**

### Endpoint
```
POST https://creatorsapi.amazon/catalog/v1/getItems
```

### Parâmetros Principais

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `itemIds` | Array | Lista de ASINs (até 10) |
| `itemIdType` | String | Tipo de ID (padrão: ASIN) |
| `partnerTag` | String | Seu Partner Tag |
| `marketplace` | String | Marketplace |
| `resources` | Array | Resources desejados |

### Exemplo de Request

```json
{
  "itemIds": ["B08XYZ123", "B09ABC456", "B07DEF789"],
  "itemIdType": "ASIN",
  "partnerTag": "seu-tag-20",
  "marketplace": "www.amazon.com.br",
  "resources": [
    "images.primary.large",
    "itemInfo.title",
    "itemInfo.features",
    "offersV2.listings.price",
    "offersV2.listings.savingBasis",
    "parentASIN"
  ]
}
```

### Resposta com Erros Parciais

```json
{
  "errors": [
    {
      "code": "ItemNotAccessible",
      "message": "The ItemId B09ABC456 is not accessible through the Creators API."
    }
  ],
  "itemsResult": {
    "items": [
      {
        "asin": "B08XYZ123",
        "detailPageURL": "https://www.amazon.com.br/dp/B08XYZ123?tag=seu-tag-20",
        "images": { /* ... */ },
        "itemInfo": { /* ... */ },
        "offersV2": { /* ... */ }
      },
      {
        "asin": "B07DEF789",
        "detailPageURL": "https://www.amazon.com.br/dp/B07DEF789?tag=seu-tag-20",
        "images": { /* ... */ },
        "itemInfo": { /* ... */ },
        "offersV2": { /* ... */ }
      }
    ]
  }
}
```

---

## 🗂️ GetBrowseNodes

**Obter informações sobre categorias (Browse Nodes).**

### Endpoint
```
POST https://creatorsapi.amazon/catalog/v1/getBrowseNodes
```

### Parâmetros

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `browseNodeIds` | Array | Lista de IDs (até 10) |
| `partnerTag` | String | Seu Partner Tag |
| `marketplace` | String | Marketplace |
| `resources` | Array | browseNodes.ancestor, browseNodes.children |

### Exemplo de Request

```json
{
  "browseNodeIds": ["16243663011", "16364346011"],
  "partnerTag": "seu-tag-20",
  "marketplace": "www.amazon.com.br",
  "resources": [
    "browseNodes.ancestor",
    "browseNodes.children"
  ]
}
```

### Exemplo de Response

```json
{
  "browseNodesResult": {
    "browseNodes": [
      {
        "id": "16243663011",
        "displayName": "Eletrônicos",
        "contextFreeName": "Eletrônicos",
        "isRoot": true,
        "children": [
          {
            "id": "16285268011",
            "displayName": "Câmeras e Foto",
            "contextFreeName": "Câmeras e Foto"
          },
          {
            "id": "16285269011",
            "displayName": "Fones de Ouvido",
            "contextFreeName": "Fones de Ouvido"
          }
        ]
      }
    ]
  }
}
```

---

## 🎨 GetVariations

**Obter variações de um produto (cores, tamanhos, etc).**

### Endpoint
```
POST https://creatorsapi.amazon/catalog/v1/getVariations
```

### Parâmetros

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `asin` | String | ASIN do produto (pai ou filho) |
| `partnerTag` | String | Seu Partner Tag |
| `marketplace` | String | Marketplace |
| `variationCount` | Integer | Itens por página (padrão: 10) |
| `variationPage` | Integer | Página (padrão: 1) |
| `resources` | Array | Resources desejados |

### Exemplo de Request

```json
{
  "asin": "B00422MCUS",
  "partnerTag": "seu-tag-20",
  "marketplace": "www.amazon.com.br",
  "variationCount": 10,
  "variationPage": 1,
  "resources": [
    "itemInfo.title",
    "offersV2.listings.price",
    "variationSummary.price.highestPrice",
    "variationSummary.price.lowestPrice",
    "variationSummary.variationDimension"
  ]
}
```

### Exemplo de Response

```json
{
  "variationsResult": {
    "items": [
      {
        "asin": "B00422MCW6",
        "detailPageURL": "https://www.amazon.com.br/dp/B00422MCW6?tag=seu-tag-20",
        "itemInfo": {
          "title": {
            "displayValue": "Carteira Tommy Hilfiger - Preto"
          }
        },
        "variationAttributes": [
          {
            "name": "color_name",
            "value": "Preto"
          },
          {
            "name": "size_name",
            "value": "Único"
          }
        ]
      }
    ],
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
          "values": ["Preto", "Marrom", "Azul", "Vermelho"]
        },
        {
          "name": "size_name",
          "displayName": "Tamanho",
          "values": ["Único"]
        }
      ]
    }
  }
}
```

---

## 📊 Resources Detalhados

### OffersV2 (Preços e Ofertas)

| Resource | Retorna |
|----------|---------|
| `offersV2.listings.price` | Preço atual |
| `offersV2.listings.savingBasis` | Preço original (para calcular desconto) |
| `offersV2.listings.availability` | Disponibilidade em estoque |
| `offersV2.listings.condition` | Condição (Novo, Usado) |
| `offersV2.listings.dealDetails` | Detalhes de promoção |
| `offersV2.listings.isBuyBoxWinner` | Se é o vendedor principal |
| `offersV2.listings.merchantInfo` | Informações do vendedor |

### ItemInfo (Informações do Produto)

| Resource | Retorna |
|----------|---------|
| `itemInfo.title` | Título do produto |
| `itemInfo.features` | Características principais |
| `itemInfo.byLineInfo` | Marca, fabricante |
| `itemInfo.productInfo` | Dimensões, peso, cor |
| `itemInfo.technicalInfo` | Especificações técnicas |
| `itemInfo.manufactureInfo` | Informações de fabricação |

### Images (Imagens)

| Resource | Retorna |
|----------|---------|
| `images.primary.small` | Imagem pequena (75px) |
| `images.primary.medium` | Imagem média (160px) |
| `images.primary.large` | Imagem grande (500px) |
| `images.primary.hiRes` | Alta resolução |
| `images.variants.large` | Imagens alternativas |

### BrowseNodeInfo (Categorias)

| Resource | Retorna |
|----------|---------|
| `browseNodeInfo.browseNodes` | Categorias do produto |
| `browseNodeInfo.browseNodes.ancestor` | Hierarquia de categorias |
| `browseNodeInfo.browseNodes.salesRank` | Ranking de vendas |
| `browseNodeInfo.websiteSalesRank` | Ranking geral no site |

---

## 🎯 Uso Recomendado para Nosso Sistema

### 1. Buscar Produtos com Desconto

```json
{
  "partnerTag": "seu-tag-20",
  "marketplace": "www.amazon.com.br",
  "keywords": "fone bluetooth",
  "sortBy": "Relevance",
  "minSavingPercent": 20,
  "condition": "New",
  "itemCount": 10,
  "resources": [
    "images.primary.large",
    "itemInfo.title",
    "offersV2.listings.price",
    "offersV2.listings.savingBasis",
    "offersV2.listings.availability"
  ]
}
```

### 2. Verificar Detalhes de Produtos Conhecidos

```json
{
  "itemIds": ["ASIN1", "ASIN2", "ASIN3"],
  "itemIdType": "ASIN",
  "partnerTag": "seu-tag-20",
  "marketplace": "www.amazon.com.br",
  "resources": [
    "images.primary.large",
    "itemInfo.title",
    "offersV2.listings.price",
    "offersV2.listings.savingBasis"
  ]
}
```

### 3. Calcular Desconto

```python
def calculate_discount(item):
    listings = item.get('offersV2', {}).get('listings', [])
    if not listings:
        return 0
    
    listing = listings[0]
    
    # Preço atual
    current_price = listing.get('price', {}).get('money', {}).get('amount', 0)
    
    # Preço original (savingBasis)
    saving_basis = listing.get('price', {}).get('savingBasis', {})
    original_price = saving_basis.get('money', {}).get('amount', 0)
    
    # Se não tem savingBasis, não tem desconto
    if not original_price or original_price <= current_price:
        return 0
    
    # Calcular desconto
    discount = ((original_price - current_price) / original_price) * 100
    return round(discount, 1)
```

---

## ⚠️ Pontos Importantes

1. **SearchItems retorna até 10 itens** - Use `itemPage` para paginação
2. **GetItems aceita até 10 ASINs** - Agrupe requests
3. **Preços em centavos** - `3241` = R$ 32,41
4. **savingBasis** - Nem sempre está presente (sem desconto)
5. **Erros parciais** - Alguns itens podem falhar, outros suceder
6. **Resources mínimos** - Peça só o necessário para melhor performance

---

**Última atualização:** 14 de Maio de 2026
