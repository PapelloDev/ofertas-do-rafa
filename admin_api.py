#!/usr/bin/env python3
"""
API Backend para Admin - Ofertas do Rafa
Extrai dados de produtos da Amazon e gerencia o site
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import os
import json
import re
import random
import string
from datetime import datetime
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
from github import Github
import base64

# Carregar variáveis de ambiente (forçar reload)
load_dotenv(override=True)

app = Flask(__name__)
CORS(app)  # Permitir requisições do frontend

# Paths
SITE_DIR = 'site'
DATA_FILE = os.path.join(SITE_DIR, 'data', 'produtos.json')
PRODUCTS_DIR = os.path.join(SITE_DIR, 'produto')

# Headers para simular navegador
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

def expand_short_url(short_url):
    """Expande URLs encurtadas (amzn.to) para obter a URL completa"""
    try:
        response = requests.head(short_url, allow_redirects=True, timeout=10)
        return response.url
    except Exception as e:
        print(f"Erro ao expandir URL: {e}")
        return short_url

def extract_asin_from_url(url):
    """Extrai ASIN de uma URL da Amazon"""
    # Se for link encurtado, expandir primeiro
    if 'amzn.to' in url or 'a.co' in url:
        print(f"Expandindo link encurtado: {url}")
        url = expand_short_url(url)
        print(f"URL expandida: {url}")
    
    # Padrões de URL da Amazon
    patterns = [
        r'/dp/([A-Z0-9]{10})',           # /dp/B08XYZ1234
        r'/gp/product/([A-Z0-9]{10})',   # /gp/product/B08XYZ1234
        r'/product/([A-Z0-9]{10})',      # /product/B08XYZ1234
        r'asin=([A-Z0-9]{10})',          # ?asin=B08XYZ1234
        r'/([A-Z0-9]{10})(?:/|\?|$)',    # Genérico
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match and match.group(1):
            return match.group(1)
    
    return None

def extract_from_pa_api(asin):
    """Extrai dados usando Amazon Product Advertising API como fallback"""
    try:
        from amazon_client import AmazonClient
        
        # Inicializar cliente
        client = AmazonClient()
        
        # Buscar produto
        items = client.get_items([asin])
        
        if not items or len(items) == 0:
            return None
        
        item = items[0]
        
        # Extrair dados
        data = {}
        
        # Título
        if 'title' in item:
            data['titulo'] = item['title']
        
        # Preços
        if 'price' in item and item['price']:
            data['preco_atual'] = item['price']
            data['preco_original'] = item.get('original_price', item['price'])
        
        # Imagem
        if 'image_url' in item:
            data['imagem_url'] = item['image_url']
        
        # Marca
        if 'brand' in item:
            data['brand'] = item['brand']
        
        # Features
        if 'features' in item and item['features']:
            data['features'] = item['features'][:5]  # Limitar a 5
        
        return data
        
    except Exception as e:
        print(f"Erro ao usar PA-API: {e}")
        return None

@app.route('/api/extract-product', methods=['POST'])
def extract_product():
    """Extrai dados do produto da Amazon"""
    try:
        data = request.json
        asin = data.get('asin')
        affiliate_link = data.get('affiliate_link')
        category = data.get('category')
        
        # Se não tiver ASIN, tentar extrair do link
        if not asin and affiliate_link:
            print(f"Extraindo ASIN do link: {affiliate_link}")
            asin = extract_asin_from_url(affiliate_link)
        
        if not asin:
            return jsonify({'error': 'Não foi possível extrair o ASIN do link. Verifique se o link está correto.'}), 400
        
        print(f"ASIN extraído: {asin}")
        print(f"Extraindo dados do produto...")
        
        # URL da Amazon
        amazon_url = f"https://www.amazon.com.br/dp/{asin}"
        
        # Fazer requisição
        response = requests.get(amazon_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        print(f"HTML recebido: {len(response.content)} bytes")
        print(f"Status code: {response.status_code}")
        
        # Extrair dados
        product_data = {
            'asin': asin,
            'titulo': extract_title(soup),
            'descricao': extract_description(soup),
            'categoria': category,
            'preco_original': extract_original_price(soup),
            'preco_atual': extract_current_price(soup),
            'desconto_percent': 0,  # Será calculado
            'imagem_url': extract_image(soup),
            'brand': extract_brand(soup),
            'features': extract_features(soup),
            'link_afiliado': affiliate_link,
            'ativo': True,
            'data_adicao': datetime.now().isoformat(),
            'data_atualizacao': datetime.now().isoformat()
        }
        
        # Calcular desconto
        if product_data['preco_original'] > product_data['preco_atual']:
            product_data['desconto_percent'] = round(
                ((product_data['preco_original'] - product_data['preco_atual']) / product_data['preco_original']) * 100,
                1
            )
        
        print(f"✅ Dados extraídos:")
        print(f"  - Título: {product_data['titulo']}")
        print(f"  - Preço atual: R$ {product_data['preco_atual']}")
        print(f"  - Preço original: R$ {product_data['preco_original']}")
        print(f"  - Desconto: {product_data['desconto_percent']}%")
        print(f"  - Marca: {product_data['brand']}")
        print(f"  - Features: {len(product_data['features'])} itens")
        
        # Se não conseguiu extrair dados básicos, tentar PA-API
        if product_data['titulo'] == "Produto sem título" or product_data['preco_atual'] == 0:
            print("⚠️ Scraping falhou, tentando Amazon PA-API...")
            try:
                pa_api_data = extract_from_pa_api(asin)
                if pa_api_data:
                    # Mesclar dados da PA-API
                    product_data.update(pa_api_data)
                    print(f"✅ Dados obtidos via PA-API")
            except Exception as e:
                print(f"⚠️ PA-API também falhou: {e}")
        
        return jsonify(product_data)
        
    except Exception as e:
        print(f"Erro ao extrair produto: {e}")
        return jsonify({'error': str(e)}), 500

def extract_title(soup):
    """Extrai título do produto"""
    selectors = [
        '#productTitle',
        'span#productTitle',
        'h1#title',
        'h1.product-title',
        '[data-feature-name="title"] h1',
        '.product-title-word-break'
    ]
    
    for selector in selectors:
        element = soup.select_one(selector)
        if element:
            title = element.get_text().strip()
            if title and len(title) > 5:  # Validar que tem conteúdo
                return title
    
    # Tentar pelo meta tag
    meta_title = soup.find('meta', {'name': 'title'})
    if meta_title and meta_title.get('content'):
        return meta_title['content'].strip()
    
    return "Produto sem título"

def extract_description(soup):
    """Extrai descrição do produto"""
    selectors = [
        '#feature-bullets',
        '#productDescription',
        '.product-description'
    ]
    
    for selector in selectors:
        element = soup.select_one(selector)
        if element:
            text = element.get_text().strip()
            # Limitar a 500 caracteres
            return text[:500] + '...' if len(text) > 500 else text
    
    return ""

def extract_current_price(soup):
    """Extrai preço atual"""
    selectors = [
        '.a-price[data-a-color="price"] .a-offscreen',
        '.a-price-whole',
        '#priceblock_ourprice',
        '#priceblock_dealprice',
        '.a-price .a-offscreen',
        '#corePrice_feature_div .a-price .a-offscreen',
        '.priceToPay .a-offscreen',
        '[data-feature-name="corePrice"] .a-offscreen'
    ]
    
    for selector in selectors:
        elements = soup.select(selector)
        for element in elements:
            price_text = element.get_text().strip()
            # Extrair apenas números e vírgula
            price = re.sub(r'[^\d,]', '', price_text)
            if price:
                price = price.replace('.', '').replace(',', '.')
                try:
                    price_float = float(price)
                    if price_float > 0:  # Validar que é um preço válido
                        return price_float
                except:
                    continue
    
    return 0.0

def extract_original_price(soup):
    """Extrai preço original (antes do desconto)"""
    selectors = [
        '.a-text-price .a-offscreen',
        '#priceblock_saleprice',
        '.basisPrice .a-offscreen'
    ]
    
    for selector in selectors:
        element = soup.select_one(selector)
        if element:
            price_text = element.get_text().strip()
            price = re.sub(r'[^\d,]', '', price_text)
            price = price.replace(',', '.')
            try:
                return float(price)
            except:
                continue
    
    # Se não encontrar preço original, retornar o preço atual
    return extract_current_price(soup)

def extract_image(soup):
    """Extrai URL da imagem principal"""
    # Tentar pegar imagem de alta resolução
    selectors = [
        '#landingImage',
        '#imgBlkFront',
        '#main-image',
        '.a-dynamic-image',
        '[data-a-dynamic-image]'
    ]
    
    for selector in selectors:
        element = soup.select_one(selector)
        if element:
            # Tentar pegar o src de alta resolução
            img_url = (element.get('data-old-hires') or 
                      element.get('data-a-dynamic-image') or 
                      element.get('src'))
            
            if img_url:
                # Se for JSON (data-a-dynamic-image), pegar a primeira URL
                if img_url.startswith('{'):
                    try:
                        import json
                        images = json.loads(img_url)
                        if images:
                            img_url = list(images.keys())[0]
                    except:
                        pass
                
                # Limpar URL se necessário
                if img_url and 'http' in img_url:
                    return img_url.split(',')[0].strip()
    
    # Tentar pelo meta tag
    meta_image = soup.find('meta', {'property': 'og:image'})
    if meta_image and meta_image.get('content'):
        return meta_image['content']
    
    return "https://via.placeholder.com/500x500?text=Sem+Imagem"

def extract_brand(soup):
    """Extrai marca do produto"""
    selectors = [
        '#bylineInfo',
        '.a-size-base.po-break-word',
        'a#brand'
    ]
    
    for selector in selectors:
        element = soup.select_one(selector)
        if element:
            brand = element.get_text().strip()
            # Remover "Marca:" ou "Visitar loja"
            brand = re.sub(r'(Marca:|Visitar.*loja)', '', brand).strip()
            return brand
    
    return ""

def extract_features(soup):
    """Extrai características do produto"""
    features = []
    
    # Tentar extrair de feature bullets
    bullets = soup.select('#feature-bullets li span.a-list-item')
    for bullet in bullets[:5]:  # Limitar a 5 features
        text = bullet.get_text().strip()
        if text and len(text) > 10:  # Ignorar textos muito curtos
            features.append(text)
    
    return features

@app.route('/api/save-product', methods=['POST'])
def save_product():
    """Salva produto no JSON"""
    try:
        product = request.json
        
        # Ler dados existentes
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Verificar se produto já existe (por ASIN)
        existing_index = next((i for i, p in enumerate(data['produtos']) if p['asin'] == product['asin']), None)
        
        if existing_index is not None:
            # Atualizar produto existente (manter short_code se existir)
            if 'short_code' not in product and 'short_code' in data['produtos'][existing_index]:
                product['short_code'] = data['produtos'][existing_index]['short_code']
            data['produtos'][existing_index] = product
            print(f"Produto atualizado: {product['asin']}")
        else:
            # Gerar código curto único para novo produto
            short_code = generate_short_code()
            # Verificar se já existe (improvável mas possível)
            while any(p.get('short_code') == short_code for p in data['produtos']):
                short_code = generate_short_code()
            
            product['short_code'] = short_code
            product['short_url'] = f"https://ofertasdorafa.app.br/{short_code}"
            
            # Adicionar novo produto
            data['produtos'].append(product)
            print(f"Novo produto adicionado: {product['asin']} | URL curta: {product['short_url']}")
        
        # Atualizar timestamp
        data['config']['ultima_atualizacao'] = datetime.now().isoformat()
        
        # Salvar
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return jsonify({'success': True, 'message': 'Produto salvo com sucesso'})
        
    except Exception as e:
        print(f"Erro ao salvar produto: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-product-page', methods=['POST'])
def generate_product_page():
    """Gera página HTML do produto"""
    try:
        data = request.json
        asin = data.get('asin')
        
        if not asin:
            return jsonify({'error': 'ASIN não fornecido'}), 400
        
        # Ler dados do produto
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            products_data = json.load(f)
        
        product = next((p for p in products_data['produtos'] if p['asin'] == asin), None)
        
        if not product:
            return jsonify({'error': 'Produto não encontrado'}), 404
        
        # Gerar HTML
        html = generate_product_html(product, products_data['categorias'])
        
        # Salvar arquivo
        product_file = os.path.join(PRODUCTS_DIR, f"{asin}.html")
        os.makedirs(PRODUCTS_DIR, exist_ok=True)
        
        with open(product_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"Página gerada: {product_file}")
        
        return jsonify({'success': True, 'message': 'Página gerada com sucesso', 'file': product_file})
        
    except Exception as e:
        print(f"Erro ao gerar página: {e}")
        return jsonify({'error': str(e)}), 500

def generate_short_code(length=6):
    """Gera um código curto único para URL"""
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def generate_category_html(category):
    """Gera HTML da página de categoria"""
    html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{category['nome']} - {category.get('descricao', '')}">
    
    <title>{category['nome']} - Ofertas do Rafa</title>
    
    <link rel="icon" type="image/png" href="../assets/images/logo/favicon.png">
    <link rel="apple-touch-icon" href="../assets/images/logo/favicon.png">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="../assets/css/style.css">
</head>
<body>
    <!-- Header e Footer serão inseridos via JavaScript -->
    
    <!-- Category Hero -->
    <section class="category-hero" style="background: linear-gradient(135deg, {category['cor']} 0%, {category['cor']}dd 100%);">
        <div class="container text-center">
            <div class="category-icon">{category['icone']}</div>
            <h1 class="category-title">{category['nome']}</h1>
            <p class="category-description">{category.get('descricao', '')}</p>
        </div>
    </section>
    
    <!-- Products Grid -->
    <section class="py-12">
        <div class="container">
            <div id="products-grid" class="products-grid">
                <!-- Products will be loaded here -->
            </div>
            
            <!-- Empty State -->
            <div id="empty-state" class="empty-state hidden">
                <div class="empty-state-icon">🔍</div>
                <h3 class="empty-state-title">Nenhuma oferta encontrada</h3>
                <p>Ainda não temos produtos nesta categoria. Volte em breve!</p>
            </div>
        </div>
    </section>
    
    <!-- Layout Components -->
    <script src="../assets/js/site-layout.js"></script>
    <script>
        // Inicializar layout
        SiteLayout.init('{category['id']}');
    </script>
    
    <script>
        // Load products for this category
        async function loadProducts() {{
            try {{
                const response = await fetch('../data/produtos.json');
                const data = await response.json();
                
                const produtos = data.produtos.filter(p => p.categoria === '{category['id']}');
                
                if (produtos.length === 0) {{
                    document.getElementById('empty-state').classList.remove('hidden');
                    return;
                }}
                
                const grid = document.getElementById('products-grid');
                grid.innerHTML = produtos.map(product => `
                    <div class="product-card">
                        <div class="product-image">
                            <img src="${{product.imagem_url}}" alt="${{product.titulo}}">
                            <span class="badge badge-discount">${{Math.round(product.desconto_percent)}}% OFF</span>
                        </div>
                        <div class="product-content">
                            <h3 class="product-title">${{product.titulo}}</h3>
                            ${{product.brand ? `<p class="product-brand">${{product.brand}}</p>` : ''}}
                            <div class="product-prices">
                                ${{product.preco_original > product.preco_atual ? 
                                    `<span class="price-old">R$ ${{product.preco_original.toFixed(2)}}</span>` : ''}}
                                <span class="price-current">R$ ${{product.preco_atual.toFixed(2)}}</span>
                            </div>
                            <a href="../produto/${{product.asin}}.html" class="btn btn-primary">
                                Ver Oferta
                            </a>
                        </div>
                    </div>
                `).join('');
                
            }} catch (error) {{
                console.error('Erro ao carregar produtos:', error);
                document.getElementById('empty-state').classList.remove('hidden');
            }}
        }}
        
        loadProducts();
    </script>
</body>
</html>'''
    
    return html


def generate_product_html(product, categories):
    """Gera HTML da página do produto"""
    category = next((c for c in categories if c['id'] == product['categoria']), {})
    
    html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{product.get('descricao', product['titulo'])}">
    <meta name="keywords" content="{product['titulo']}, {category.get('nome', '')}, oferta, desconto, Amazon">
    
    <!-- Open Graph -->
    <meta property="og:title" content="{product['titulo']} - {product['desconto_percent']}% OFF">
    <meta property="og:description" content="De R$ {product['preco_original']:.2f} por R$ {product['preco_atual']:.2f}">
    <meta property="og:image" content="{product['imagem_url']}">
    <meta property="og:type" content="product">
    
    <title>{product['titulo']} - Ofertas do Rafa</title>
    
    <link rel="icon" type="image/png" href="../assets/images/logo/favicon.png">
    <link rel="apple-touch-icon" href="../assets/images/logo/favicon.png">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="../assets/css/style.css">
    <style>
        @keyframes bounce-slow {{
            0%, 100% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-10px); }}
        }}
        .animate-bounce-slow {{
            animation: bounce-slow 2s ease-in-out infinite;
        }}
    </style>
</head>
<body>
    <!-- Header -->
    <header class="header">
        <div class="container">
            <nav class="flex items-center justify-between py-4">
                <a href="../index.html" class="flex items-center">
                    <img src="../assets/images/logo/logo-full.png" alt="Ofertas do Rafa" class="logo-img">
                </a>
                
                <div class="hidden md:flex items-center gap-2">
                    <a href="../index.html" class="nav-link">Início</a>
                    <a href="../categoria/eletronicos.html" class="nav-link">📱 Eletrônicos</a>
                    <a href="../categoria/corrida.html" class="nav-link">🏃 Corrida</a>
                </div>
            </nav>
        </div>
    </header>
    
    <!-- WhatsApp Group Banner -->
    <div id="whatsapp-banner" class="hidden fixed bottom-6 left-1/2 transform -translate-x-1/2 z-50 w-full max-w-md px-4">
        <div class="bg-gradient-to-r from-green-500 to-green-600 rounded-2xl shadow-2xl p-4 animate-bounce-slow">
            <div class="flex items-center justify-between">
                <div class="flex items-center gap-3 flex-1">
                    <div class="bg-white rounded-full p-2">
                        <svg class="w-8 h-8 text-green-600" fill="currentColor" viewBox="0 0 24 24">
                            <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
                        </svg>
                    </div>
                    <div class="text-white flex-1">
                        <p class="font-bold text-sm">📢 Entre no Grupo!</p>
                        <p class="text-xs opacity-90">Receba ofertas em primeira mão</p>
                    </div>
                </div>
                <a id="whatsapp-group-link" href="#" target="_blank" rel="noopener noreferrer" class="bg-white text-green-600 px-4 py-2 rounded-full font-bold text-sm hover:bg-green-50 transition-colors whitespace-nowrap ml-2">
                    Entrar →
                </a>
            </div>
        </div>
    </div>
    
    <!-- Product Detail -->
    <main class="container py-8">
        <div class="max-w-6xl mx-auto">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                <!-- Image -->
                <div>
                    <img src="{product['imagem_url']}" alt="{product['titulo']}" class="w-full rounded-lg shadow-lg">
                </div>
                
                <!-- Info -->
                <div>
                    <div class="mb-4">
                        <span class="badge badge-{product['categoria']}">{category.get('icone', '')} {category.get('nome', '')}</span>
                        <span class="badge badge-discount ml-2">{round(product['desconto_percent'])}% OFF</span>
                    </div>
                    
                    <h1 class="text-3xl font-bold text-gray-900 mb-4">{product['titulo']}</h1>
                    
                    <!-- Botão de Compra no Topo -->
                    <a href="{product['link_afiliado']}" 
                       target="_blank" 
                       rel="noopener noreferrer" 
                       class="btn-buy-top btn btn-primary w-full text-center text-xl py-4 mb-6 animate-pulse"
                       data-asin="{product['asin']}"
                       data-title="{product['titulo']}"
                       data-category="{product['categoria']}">
                        🛒 COMPRAR NA AMAZON AGORA
                    </a>
                    
                    {f'<p class="text-lg text-gray-600 mb-4">Marca: <strong>{product["brand"]}</strong></p>' if product.get('brand') else ''}
                    
                    <div class="bg-gray-50 rounded-lg p-6 mb-6">
                        {f'<p class="text-gray-500 line-through text-lg mb-2">De: R$ {product["preco_original"]:.2f}</p>' if product['preco_original'] > product['preco_atual'] else ''}
                        <p class="text-4xl font-bold text-[#1A5F5F] mb-2">R$ {product['preco_atual']:.2f}</p>
                        <p class="text-green-600 font-semibold">Economize R$ {(product['preco_original'] - product['preco_atual']):.2f}</p>
                    </div>
                    
                    <a href="{product['link_afiliado']}" 
                       target="_blank" 
                       rel="noopener noreferrer" 
                       class="btn btn-primary w-full text-center text-xl py-4 mb-6"
                       data-asin="{product['asin']}"
                       data-title="{product['titulo']}"
                       data-category="{product['categoria']}">
                        🛒 Comprar na Amazon
                    </a>
                    
                    <!-- Contador Regressivo -->
                    <div id="countdown-container" class="bg-gradient-to-r from-red-50 to-orange-50 border-2 border-red-300 rounded-lg p-6 mb-4">
                        <div class="text-center">
                            <p class="text-red-600 font-bold text-lg mb-3">⏰ OFERTA TERMINA EM:</p>
                            <div id="countdown" class="flex justify-center gap-4 text-2xl font-bold text-red-600">
                                <div class="flex flex-col items-center">
                                    <span id="hours" class="text-4xl">00</span>
                                    <span class="text-xs text-gray-600">HORAS</span>
                                </div>
                                <span class="text-4xl">:</span>
                                <div class="flex flex-col items-center">
                                    <span id="minutes" class="text-4xl">00</span>
                                    <span class="text-xs text-gray-600">MIN</span>
                                </div>
                                <span class="text-4xl">:</span>
                                <div class="flex flex-col items-center">
                                    <span id="seconds" class="text-4xl">00</span>
                                    <span class="text-xs text-gray-600">SEG</span>
                                </div>
                            </div>
                            <p class="text-sm text-gray-600 mt-3">🔥 Não perca esta oportunidade!</p>
                        </div>
                    </div>
                    
                    <!-- Oferta Expirada -->
                    <div id="expired-container" class="hidden bg-gray-100 border-2 border-gray-400 rounded-lg p-6 mb-4">
                        <div class="text-center">
                            <p class="text-gray-600 font-bold text-xl mb-2">⏰ OFERTA EXPIRADA</p>
                            <p class="text-gray-500">Esta promoção não está mais disponível.</p>
                            <a href="../index.html" class="inline-block mt-4 text-[#1A5F5F] hover:underline">
                                ← Ver outras ofertas
                            </a>
                        </div>
                    </div>
                    
                    <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4 text-sm text-yellow-800">
                        ⚡ <strong>Oferta por tempo limitado!</strong> Preços e disponibilidade podem variar.
                    </div>
                </div>
            </div>
            
            <!-- Features -->
            {f'''<div class="mt-12">
                <h2 class="text-2xl font-bold text-gray-900 mb-4">Características</h2>
                <ul class="space-y-2">
                    {"".join([f'<li class="flex items-start"><span class="text-green-600 mr-2">✓</span><span>{feature}</span></li>' for feature in product.get('features', [])])}
                </ul>
            </div>''' if product.get('features') else ''}
        </div>
    </main>
    
    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="disclaimer">
                <h4 class="font-bold mb-2">⚠️ Aviso de Programa de Afiliados</h4>
                <p>Este site participa do Programa de Associados da Amazon. Como Associado da Amazon, eu ganho com compras qualificadas.</p>
            </div>
            <div class="text-center mt-6 text-sm opacity-75">
                <p>&copy; 2026 Ofertas do Rafa. Todos os direitos reservados.</p>
            </div>
        </div>
    </footer>
    
    <!-- Analytics -->
    <script src="../assets/js/analytics.js"></script>
    
    <!-- WhatsApp Group Banner -->
    <script>
        // Carregar link do grupo WhatsApp
        fetch('../data/produtos.json')
            .then(response => response.json())
            .then(data => {{
                const whatsappGroupUrl = data.config?.whatsapp_group_url;
                
                if (whatsappGroupUrl) {{
                    const banner = document.getElementById('whatsapp-banner');
                    const link = document.getElementById('whatsapp-group-link');
                    
                    link.href = whatsappGroupUrl;
                    
                    // Mostrar banner após 3 segundos
                    setTimeout(() => {{
                        banner.classList.remove('hidden');
                    }}, 3000);
                }}
            }})
            .catch(error => console.error('Erro ao carregar config:', error));
    </script>
    
    <!-- Countdown Timer -->
    <script>
        const expiryDate = '{product.get("expiry_date", "")}';
        
        if (expiryDate) {{
            const countdownContainer = document.getElementById('countdown-container');
            const expiredContainer = document.getElementById('expired-container');
            const buyButtons = document.querySelectorAll('.btn-primary');
            
            function updateCountdown() {{
                const now = new Date().getTime();
                const expiry = new Date(expiryDate).getTime();
                const distance = expiry - now;
                
                if (distance < 0) {{
                    // Oferta expirada - redirecionar para home
                    console.log('⚠️ Produto expirado, redirecionando para home...');
                    setTimeout(() => {{
                        window.location.href = '/';
                    }}, 2000); // Aguarda 2 segundos para mostrar mensagem
                    
                    countdownContainer.classList.add('hidden');
                    expiredContainer.classList.remove('hidden');
                    buyButtons.forEach(btn => {{
                        btn.classList.add('hidden');
                        btn.disabled = true;
                    }});
                    return;
                }}
                
                // Calcular tempo restante
                const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
                const seconds = Math.floor((distance % (1000 * 60)) / 1000);
                
                // Atualizar display
                document.getElementById('hours').textContent = String(hours).padStart(2, '0');
                document.getElementById('minutes').textContent = String(minutes).padStart(2, '0');
                document.getElementById('seconds').textContent = String(seconds).padStart(2, '0');
                
                // Adicionar efeito de urgência quando faltam menos de 1 hora
                if (hours === 0 && minutes < 60) {{
                    countdownContainer.classList.add('animate-pulse');
                }}
            }}
            
            // Atualizar a cada segundo
            updateCountdown();
            setInterval(updateCountdown, 1000);
        }} else {{
            // Se não tem data de expiração, esconder contador
            document.getElementById('countdown-container').classList.add('hidden');
        }}
    </script>
</body>
</html>'''
    
    return html

@app.route('/api/save-category', methods=['POST'])
def save_category():
    """Salva nova categoria no JSON"""
    try:
        category = request.json
        
        # Ler dados existentes
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Verificar se categoria já existe
        existing_index = next((i for i, c in enumerate(data['categorias']) if c['id'] == category['id']), None)
        
        if existing_index is not None:
            return jsonify({'error': 'Categoria com este ID já existe'}), 400
        
        # Adicionar nova categoria
        data['categorias'].append(category)
        print(f"Nova categoria adicionada: {category['id']}")
        
        # Atualizar timestamp
        data['config']['ultima_atualizacao'] = datetime.now().isoformat()
        
        # Salvar
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        # Gerar página HTML da categoria
        try:
            category_html = generate_category_html(category)
            category_file = os.path.join(SITE_DIR, 'categoria', f"{category['id']}.html")
            os.makedirs(os.path.dirname(category_file), exist_ok=True)
            
            with open(category_file, 'w', encoding='utf-8') as f:
                f.write(category_html)
            
            print(f"   ✅ Página da categoria gerada: {category['id']}.html")
        except Exception as page_error:
            print(f"⚠️ Erro ao gerar página da categoria: {page_error}")
        
        # Deploy automático
        try:
            print("🚀 Iniciando deploy automático...")
            deploy_result = deploy_changes(f"Nova categoria adicionada: {category['nome']}")
            print(f"✅ Deploy concluído: {deploy_result}")
        except Exception as deploy_error:
            print(f"⚠️ Erro no deploy: {deploy_error}")
        
        return jsonify({'success': True, 'message': 'Categoria salva com sucesso'})
        
    except Exception as e:
        print(f"Erro ao salvar categoria: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/send-to-whatsapp', methods=['POST'])
def send_to_whatsapp():
    """Envia produto para o WhatsApp"""
    try:
        data_request = request.json
        asin = data_request.get('asin')
        renew_expiry = data_request.get('renew_expiry', False)
        expiry_hours = data_request.get('expiry_hours', 24)
        
        if not asin:
            return jsonify({'error': 'ASIN não fornecido'}), 400
        
        # Ler dados do produto
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        product = next((p for p in data['produtos'] if p['asin'] == asin), None)
        
        if not product:
            return jsonify({'error': 'Produto não encontrado'}), 404
        
        # Renovar validade se solicitado
        if renew_expiry and expiry_hours > 0:
            try:
                from datetime import datetime, timedelta
                print(f"🔄 Renovando validade do produto {asin} para {expiry_hours}h...")
                
                now = datetime.now()
                expiry_date = now + timedelta(hours=expiry_hours)
                
                product['expiry_date'] = expiry_date.isoformat()
                product['expiry_hours'] = expiry_hours
                
                print(f"📝 Nova data de expiração: {expiry_date.isoformat()}")
                
                # Salvar alterações no JSON
                print(f"💾 Salvando alterações no JSON...")
                with open(DATA_FILE, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"✅ JSON atualizado!")
                
                # Regenerar página HTML
                print(f"🔨 Regenerando página HTML...")
                categories = data.get('categorias', [])
                html = generate_product_html(product, categories)
                product_file = os.path.join(PRODUCTS_DIR, f"{asin}.html")
                os.makedirs(PRODUCTS_DIR, exist_ok=True)
                with open(product_file, 'w', encoding='utf-8') as f:
                    f.write(html)
                print(f"✅ Página HTML regenerada: {product_file}")
                
                print(f"✅ Validade renovada: {expiry_hours}h (até {expiry_date.strftime('%d/%m/%Y %H:%M')})")
            except Exception as e:
                print(f"❌ Erro ao renovar validade: {e}")
                import traceback
                traceback.print_exc()
                return jsonify({'error': f'Erro ao renovar validade: {str(e)}'}), 500
        
        # URL do produto
        site_url = data['config'].get('site_url', 'https://ofertasdorafa.netlify.app')
        product_url = f"{site_url}/produto/{asin}.html"
        
        # Importar e executar envio
        from send_product_whatsapp import send_product_to_whatsapp
        
        success = send_product_to_whatsapp(product, product_url)
        
        if success:
            message = 'Produto enviado para WhatsApp'
            if renew_expiry and expiry_hours > 0:
                message += f' (validade renovada para {expiry_hours}h)'
            return jsonify({'success': True, 'message': message})
        else:
            return jsonify({'error': 'Falha ao enviar para WhatsApp'}), 500
        
    except Exception as e:
        print(f"Erro ao enviar para WhatsApp: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/delete-category', methods=['POST'])
def delete_category():
    """Exclui categoria do JSON"""
    try:
        data_request = request.json
        category_id = data_request.get('id')
        
        if not category_id:
            return jsonify({'error': 'ID da categoria não fornecido'}), 400
        
        # Ler dados existentes
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Verificar se há produtos usando esta categoria
        products_with_category = [p for p in data['produtos'] if p.get('categoria') == category_id]
        
        if products_with_category:
            return jsonify({
                'error': f'Não é possível excluir. Existem {len(products_with_category)} produto(s) usando esta categoria.'
            }), 400
        
        # Remover categoria
        data['categorias'] = [c for c in data['categorias'] if c['id'] != category_id]
        print(f"Categoria excluída: {category_id}")
        
        # Atualizar timestamp
        data['config']['ultima_atualizacao'] = datetime.now().isoformat()
        
        # Salvar
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return jsonify({'success': True, 'message': 'Categoria excluída com sucesso'})
        
    except Exception as e:
        print(f"Erro ao excluir categoria: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/delete-product', methods=['POST'])
def delete_product():
    """Excluir um produto"""
    try:
        data = request.json
        asin = data.get('asin')
        
        if not asin:
            return jsonify({'error': 'ASIN não fornecido'}), 400
        
        # Ler produtos
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            produtos_data = json.load(f)
        
        # Encontrar e remover produto
        produtos_data['produtos'] = [p for p in produtos_data['produtos'] if p['asin'] != asin]
        
        # Atualizar última atualização
        produtos_data['config']['ultima_atualizacao'] = datetime.now().isoformat()
        
        # Salvar
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(produtos_data, f, ensure_ascii=False, indent=2)
        
        # Remover página HTML do produto
        product_file = os.path.join(PRODUCTS_DIR, f'{asin}.html')
        if os.path.exists(product_file):
            os.remove(product_file)
            print(f"   ✅ Página HTML removida: {asin}.html")
        
        print(f"✅ Produto excluído: {asin}")
        
        # Deploy automático para GitHub
        try:
            print("🚀 Iniciando deploy automático...")
            deploy_result = deploy_changes(f"Produto removido: {asin}")
            print(f"✅ Deploy concluído: {deploy_result}")
        except Exception as deploy_error:
            print(f"⚠️ Erro no deploy (produto foi deletado localmente): {deploy_error}")
        
        return jsonify({'success': True, 'message': 'Produto excluído com sucesso'})
        
    except Exception as e:
        print(f"Erro ao excluir produto: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/remove-expired', methods=['POST'])
def remove_expired():
    """Remover todos os produtos expirados"""
    try:
        # Ler produtos
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            produtos_data = json.load(f)
        
        # Filtrar produtos expirados
        now = datetime.now()
        produtos_ativos = []
        produtos_removidos = []
        
        for produto in produtos_data['produtos']:
            if produto.get('expiry_date'):
                expiry_date = datetime.fromisoformat(produto['expiry_date'].replace('Z', '+00:00'))
                if now > expiry_date:
                    produtos_removidos.append(produto)
                    # Remover página HTML
                    product_file = os.path.join(PRODUCTS_DIR, f"{produto['asin']}.html")
                    if os.path.exists(product_file):
                        os.remove(product_file)
                else:
                    produtos_ativos.append(produto)
            else:
                # Produtos sem prazo de validade permanecem
                produtos_ativos.append(produto)
        
        # Atualizar produtos
        produtos_data['produtos'] = produtos_ativos
        produtos_data['config']['ultima_atualizacao'] = datetime.now().isoformat()
        
        # Salvar
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(produtos_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ {len(produtos_removidos)} produto(s) expirado(s) removido(s)")
        
        # Deploy automático se houver produtos removidos
        if len(produtos_removidos) > 0:
            try:
                print("🚀 Iniciando deploy automático...")
                deploy_result = deploy_changes(f"Removidos {len(produtos_removidos)} produto(s) expirado(s)")
                print(f"✅ Deploy concluído: {deploy_result}")
            except Exception as deploy_error:
                print(f"⚠️ Erro no deploy: {deploy_error}")
        
        return jsonify({
            'success': True,
            'removed_count': len(produtos_removidos),
            'message': f'{len(produtos_removidos)} produto(s) removido(s)'
        })
        
    except Exception as e:
        print(f"Erro ao remover produtos expirados: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/track-click', methods=['POST'])
def track_click():
    """Registrar clique em produto"""
    try:
        data = request.json
        
        analytics_file = os.path.join(SITE_DIR, 'data', 'analytics.json')
        
        # Ler analytics existente
        if os.path.exists(analytics_file):
            with open(analytics_file, 'r', encoding='utf-8') as f:
                analytics_data = json.load(f)
        else:
            analytics_data = {
                'clicks': [],
                'summary': {
                    'total_clicks': 0,
                    'clicks_by_product': {},
                    'clicks_by_category': {},
                    'clicks_by_date': {}
                },
                'last_updated': ''
            }
        
        # Adicionar novo clique
        click_data = {
            'asin': data.get('asin'),
            'product_title': data.get('product_title'),
            'category': data.get('category'),
            'timestamp': data.get('timestamp'),
            'user_agent': data.get('user_agent', ''),
            'referrer': data.get('referrer', '')
        }
        
        analytics_data['clicks'].append(click_data)
        
        # Atualizar sumário
        analytics_data['summary']['total_clicks'] += 1
        
        # Por produto
        asin = click_data['asin']
        if asin not in analytics_data['summary']['clicks_by_product']:
            analytics_data['summary']['clicks_by_product'][asin] = {
                'count': 0,
                'title': click_data['product_title']
            }
        analytics_data['summary']['clicks_by_product'][asin]['count'] += 1
        
        # Por categoria
        category = click_data['category']
        if category:
            if category not in analytics_data['summary']['clicks_by_category']:
                analytics_data['summary']['clicks_by_category'][category] = 0
            analytics_data['summary']['clicks_by_category'][category] += 1
        
        # Por data
        date = click_data['timestamp'][:10]  # YYYY-MM-DD
        if date not in analytics_data['summary']['clicks_by_date']:
            analytics_data['summary']['clicks_by_date'][date] = 0
        analytics_data['summary']['clicks_by_date'][date] += 1
        
        # Atualizar timestamp
        analytics_data['last_updated'] = datetime.now().isoformat()
        
        # Salvar
        with open(analytics_file, 'w', encoding='utf-8') as f:
            json.dump(analytics_data, f, ensure_ascii=False, indent=2)
        
        print(f"📊 Clique registrado: {click_data['product_title']}")
        
        return jsonify({'success': True})
        
    except Exception as e:
        print(f"Erro ao registrar clique: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """Obter dados de analytics"""
    try:
        analytics_file = os.path.join(SITE_DIR, 'data', 'analytics.json')
        
        if not os.path.exists(analytics_file):
            return jsonify({
                'clicks': [],
                'summary': {
                    'total_clicks': 0,
                    'clicks_by_product': {},
                    'clicks_by_category': {},
                    'clicks_by_date': {}
                }
            })
        
        with open(analytics_file, 'r', encoding='utf-8') as f:
            analytics_data = json.load(f)
        
        # Limitar clicks aos últimos 1000 para não sobrecarregar
        if len(analytics_data['clicks']) > 1000:
            analytics_data['clicks'] = analytics_data['clicks'][-1000:]
        
        return jsonify(analytics_data)
        
    except Exception as e:
        print(f"Erro ao obter analytics: {e}")
        return jsonify({'error': str(e)}), 500


def deploy_changes(commit_message):
    """Função auxiliar para fazer deploy de mudanças no GitHub"""
    # Configurações do GitHub
    token = os.getenv('GITHUB_TOKEN')
    repo_name = os.getenv('GITHUB_REPO')
    branch = os.getenv('GITHUB_BRANCH', 'main')
    
    if not token or not repo_name:
        raise Exception('GitHub não configurado no .env')
    
    print(f"📤 Deploy para GitHub...")
    print(f"   Repositório: {repo_name}")
    print(f"   Mensagem: {commit_message}")
    
    # Conectar ao GitHub
    g = Github(token)
    repo = g.get_repo(repo_name)
    
    # Ler arquivo produtos.json local
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        produtos_content = f.read()
    
    # Atualizar produtos.json no GitHub
    try:
        contents = repo.get_contents('site/data/produtos.json', ref=branch)
        repo.update_file(
            'site/data/produtos.json',
            commit_message,
            produtos_content,
            contents.sha,
            branch=branch
        )
        print(f"   ✅ produtos.json atualizado no GitHub")
    except Exception as e:
        # Se não existir, criar
        repo.create_file(
            'site/data/produtos.json',
            commit_message,
            produtos_content,
            branch=branch
        )
        print(f"   ✅ produtos.json criado no GitHub")
    
    return "Deploy concluído com sucesso"


@app.route('/api/deploy', methods=['POST'])
def deploy_to_github():
    """Commit e push automático para GitHub"""
    try:
        data = request.json
        asin = data.get('asin', 'produto')
        message = data.get('message', f'Novo produto: {asin}')
        
        # Configurações do GitHub
        token = os.getenv('GITHUB_TOKEN')
        repo_name = os.getenv('GITHUB_REPO')
        branch = os.getenv('GITHUB_BRANCH', 'main')
        
        if not token or not repo_name:
            return jsonify({'error': 'GitHub não configurado no .env'}), 500
        
        print(f"📤 Iniciando deploy para GitHub...")
        print(f"   Repositório: {repo_name}")
        print(f"   Branch: {branch}")
        
        # Conectar ao GitHub
        g = Github(token)
        repo = g.get_repo(repo_name)
        
        # Ler arquivo produtos.json local
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            produtos_content = f.read()
        
        # Atualizar produtos.json no GitHub
        try:
            contents = repo.get_contents('site/data/produtos.json', ref=branch)
            repo.update_file(
                'site/data/produtos.json',
                message,
                produtos_content,
                contents.sha,
                branch=branch
            )
            print(f"   ✅ produtos.json atualizado")
        except Exception as e:
            # Se não existir, criar
            repo.create_file(
                'site/data/produtos.json',
                message,
                produtos_content,
                branch=branch
            )
            print(f"   ✅ produtos.json criado")
        
        # Atualizar página do produto
        product_file = f'site/produto/{asin}.html'
        if os.path.exists(product_file):
            with open(product_file, 'r', encoding='utf-8') as f:
                product_content = f.read()
            
            try:
                contents = repo.get_contents(f'site/produto/{asin}.html', ref=branch)
                repo.update_file(
                    f'site/produto/{asin}.html',
                    message,
                    product_content,
                    contents.sha,
                    branch=branch
                )
                print(f"   ✅ Página do produto atualizada")
            except:
                repo.create_file(
                    f'site/produto/{asin}.html',
                    message,
                    product_content,
                    branch=branch
                )
                print(f"   ✅ Página do produto criada")
        
        print(f"✅ Deploy realizado com sucesso!")
        print(f"   Netlify vai fazer rebuild em ~2 minutos")
        
        return jsonify({
            'success': True,
            'message': 'Deploy iniciado! Site será atualizado em ~2 minutos.',
            'commit_message': message
        })
        
    except Exception as e:
        print(f"❌ Erro no deploy: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/save-config', methods=['POST'])
def save_config():
    """Salvar configurações"""
    try:
        config_data = request.json
        
        # Ler dados atuais
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Atualizar config
        if 'config' not in data:
            data['config'] = {}
        
        data['config'].update(config_data)
        data['config']['ultima_atualizacao'] = datetime.now().isoformat()
        
        # Salvar
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Configurações salvas")
        return jsonify({'success': True})
        
    except Exception as e:
        print(f"Erro ao salvar configurações: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-hook', methods=['POST'])
def generate_hook():
    """Gerar gancho de venda com OpenAI"""
    try:
        data_request = request.json
        title = data_request.get('title', '')
        features = data_request.get('features', '')
        
        if not title:
            return jsonify({'error': 'Título é obrigatório'}), 400
        
        # Ler configurações do .env (forçar reload)
        import os
        from dotenv import load_dotenv
        load_dotenv(override=True)
        
        api_key = os.getenv('OPENAI_API_KEY')
        model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
        
        print(f"🔑 Chave carregada (primeiros 20 chars): {api_key[:20] if api_key else 'NENHUMA'}...")
        print(f"🤖 Modelo: {model}")
        
        if not api_key:
            return jsonify({
                'error': 'Chave API da OpenAI não configurada',
                'details': 'Configure OPENAI_API_KEY no arquivo .env'
            }), 400
        
        # Chamar OpenAI
        import openai
        openai.api_key = api_key
        
        prompt = f"""Você é um especialista em copywriting para vendas online.

Crie um gancho de venda CURTO (máximo 2 linhas) para este produto:

Produto: {title}
{f'Características: {features}' if features else ''}

O gancho deve:
1. Levantar um problema ou dor que o cliente tem
2. Apresentar o produto como a solução
3. Ser direto e impactante
4. Usar linguagem coloquial brasileira
5. NÃO usar emojis

Exemplo de formato:
"Cansado de perder suas chaves? Este rastreador inteligente resolve esse problema de vez!"

Retorne APENAS o gancho, sem aspas ou formatação extra."""

        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Você é um especialista em copywriting de vendas."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=100
        )
        
        hook = response.choices[0].message.content.strip()
        
        # Remover aspas se houver
        hook = hook.strip('"').strip("'")
        
        print(f"✅ Gancho gerado: {hook}")
        
        return jsonify({'hook': hook})
        
    except Exception as e:
        print(f"Erro ao gerar gancho: {e}")
        return jsonify({
            'error': 'Erro ao gerar gancho',
            'details': str(e)
        }), 500

@app.route('/api/test-openai', methods=['POST'])
def test_openai():
    """Testar conexão com OpenAI"""
    try:
        data_request = request.json
        api_key = data_request.get('api_key')
        model = data_request.get('model', 'gpt-4o-mini')
        
        if not api_key:
            return jsonify({'error': 'Chave API não fornecida'}), 400
        
        import openai
        openai.api_key = api_key
        
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": "Diga apenas 'OK'"}
            ],
            max_tokens=10
        )
        
        message = response.choices[0].message.content
        
        return jsonify({
            'success': True,
            'message': message,
            'model': model
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Erro ao conectar com OpenAI',
            'details': str(e)
        }), 500


if __name__ == '__main__':
    print("=" * 60)
    print("🚀 API Admin - Ofertas do Rafa")
    print("=" * 60)
    print()
    print("📡 Servidor rodando em: http://localhost:5001")
    print("📂 Diretório do site:", SITE_DIR)
    print()
    print("Endpoints disponíveis:")
    print("  POST /api/extract-product       - Extrair dados da Amazon")
    print("  POST /api/save-product          - Salvar produto no JSON")
    print("  POST /api/generate-product-page - Gerar página HTML")
    print("  POST /api/send-to-whatsapp      - Enviar produto para WhatsApp")
    print("  POST /api/deploy                - Deploy automático para GitHub")
    print("  POST /api/delete-product        - Excluir produto")
    print("  POST /api/remove-expired        - Remover produtos expirados")
    print("  POST /api/track-click           - Registrar clique em produto")
    print("  GET  /api/analytics             - Obter dados de analytics")
    print("  POST /api/save-category         - Salvar categoria")
    print("  POST /api/delete-category       - Excluir categoria")
    print("  POST /api/save-config           - Salvar configurações")
    print("  POST /api/generate-hook         - Gerar gancho com IA")
    print("  POST /api/test-openai           - Testar OpenAI")
    print()
    print("Pressione Ctrl+C para parar")
    print("=" * 60)
    print()
    
    app.run(debug=True, port=5001)
