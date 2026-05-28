// Ofertas do Rafa - Main JavaScript

// Estado global
let allProducts = [];
let categories = [];
let currentCategory = 'todos';

// Inicializar ao carregar a página
document.addEventListener('DOMContentLoaded', () => {
    initMobileMenu();
    loadProducts();
});

// Mobile Menu Toggle
function initMobileMenu() {
    const menuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (menuBtn && mobileMenu) {
        menuBtn.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        });
    }
}

// Carregar produtos do JSON
async function loadProducts() {
    try {
        const response = await fetch('data/produtos.json');
        const data = await response.json();
        
        allProducts = data.produtos || [];
        categories = data.categorias || [];
        
        // Atualizar última atualização
        if (data.config && data.config.ultima_atualizacao) {
            const lastUpdate = new Date(data.config.ultima_atualizacao);
            document.getElementById('last-update').textContent = lastUpdate.toLocaleDateString('pt-BR');
        }
        
        // Renderizar filtros de categoria
        renderCategoryFilters();
        
        // Renderizar produtos
        renderProducts(allProducts);
        
    } catch (error) {
        console.error('Erro ao carregar produtos:', error);
        showEmptyState();
    }
}

// Renderizar filtros de categoria dinamicamente
function renderCategoryFilters() {
    const container = document.getElementById('category-filters');
    
    // Botão "Todos"
    let filtersHTML = `
        <button class="btn btn-outline category-filter active" data-category="todos">
            Todos os Produtos
        </button>
    `;
    
    // Adicionar botões para cada categoria
    categories.forEach(category => {
        filtersHTML += `
            <button class="btn btn-outline category-filter" data-category="${category.id}">
                ${category.icone} ${category.nome}
            </button>
        `;
    });
    
    container.innerHTML = filtersHTML;
    
    // Reinicializar event listeners
    initCategoryFilters();
}

// Renderizar produtos na grid
function renderProducts(products) {
    const container = document.getElementById('products-container');
    const emptyState = document.getElementById('empty-state');
    
    if (!products || products.length === 0) {
        showEmptyState();
        return;
    }
    
    // Ocultar empty state
    emptyState.classList.add('hidden');
    
    // Filtrar apenas produtos ativos e não expirados
    const activeProducts = products.filter(p => {
        // Verificar se está ativo
        if (p.ativo === false) return false;
        
        // Verificar se está expirado
        if (p.expiry_date) {
            const now = new Date().getTime();
            const expiry = new Date(p.expiry_date).getTime();
            if (expiry < now) return false; // Produto expirado
        }
        
        return true;
    });
    
    if (activeProducts.length === 0) {
        showEmptyState();
        return;
    }
    
    // Gerar HTML dos produtos
    container.innerHTML = activeProducts.map(product => createProductCard(product)).join('');
}

// Criar card de produto
function createProductCard(product) {
    const discount = product.desconto_percent || 0;
    const category = categories.find(c => c.id === product.categoria) || {};
    
    return `
        <div class="product-card" data-category="${product.categoria}">
            <a href="produto/${product.asin}.html">
                <img src="${product.imagem_url}" alt="${product.titulo}" class="product-image" loading="lazy">
            </a>
            <div class="product-content">
                <div class="flex gap-2 mb-2">
                    <span class="badge badge-${product.categoria}">${category.icone || ''} ${category.nome || product.categoria}</span>
                    ${discount > 0 ? `<span class="badge badge-discount">${Math.round(discount)}% OFF</span>` : ''}
                </div>
                
                ${product.brand ? `<p class="product-brand">${product.brand}</p>` : ''}
                
                <h3 class="product-title">
                    <a href="produto/${product.asin}.html" class="text-inherit hover:text-primary">
                        ${product.titulo}
                    </a>
                </h3>
                
                <div class="product-prices mt-auto">
                    ${product.preco_original > product.preco_atual ? `
                        <p class="price-original">De: R$ ${formatPrice(product.preco_original)}</p>
                    ` : ''}
                    <p class="price-current">R$ ${formatPrice(product.preco_atual)}</p>
                    ${discount > 0 ? `
                        <p class="text-sm text-success font-semibold">
                            Economize R$ ${formatPrice(product.preco_original - product.preco_atual)}
                        </p>
                    ` : ''}
                </div>
                
                <a href="${product.link_afiliado}" target="_blank" rel="noopener noreferrer" class="btn btn-primary w-full mt-4">
                    🛒 Ver Oferta na Amazon
                </a>
            </div>
        </div>
    `;
}

// Formatar preço
function formatPrice(price) {
    return price.toFixed(2).replace('.', ',');
}

// Mostrar estado vazio
function showEmptyState() {
    const container = document.getElementById('products-container');
    const emptyState = document.getElementById('empty-state');
    
    container.innerHTML = '';
    emptyState.classList.remove('hidden');
}

// Inicializar filtros de categoria
function initCategoryFilters() {
    const filterButtons = document.querySelectorAll('.category-filter');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            const category = button.dataset.category;
            
            // Atualizar botões ativos
            filterButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            // Filtrar produtos
            filterProducts(category);
        });
    });
}

// Filtrar produtos por categoria
function filterProducts(category) {
    currentCategory = category;
    
    if (category === 'todos') {
        renderProducts(allProducts);
    } else {
        const filtered = allProducts.filter(p => p.categoria === category);
        renderProducts(filtered);
    }
}

// Utility: Scroll suave para elemento
function scrollToElement(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}
