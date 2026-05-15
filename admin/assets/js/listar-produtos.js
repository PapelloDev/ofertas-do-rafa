// Admin - Listar e Gerenciar Produtos

let allProducts = [];
let categories = [];

// Carregar produtos e categorias
async function loadData() {
    try {
        const response = await fetch('http://localhost:8000/data/produtos.json');
        const data = await response.json();
        
        allProducts = data.produtos || [];
        categories = data.categorias || [];
        
        // Preencher filtro de categorias
        const categoryFilter = document.getElementById('filter-category');
        categories.forEach(cat => {
            const option = document.createElement('option');
            option.value = cat.id;
            option.textContent = `${cat.icone} ${cat.nome}`;
            categoryFilter.appendChild(option);
        });
        
        // Renderizar produtos
        renderProducts();
        
    } catch (error) {
        console.error('Erro ao carregar dados:', error);
        alert('Erro ao carregar produtos');
    }
}

// Verificar se produto está expirado
function isExpired(product) {
    if (!product.expiry_date) return false;
    
    const expiryDate = new Date(product.expiry_date);
    const now = new Date();
    
    return now > expiryDate;
}

// Formatar data
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Renderizar produtos
function renderProducts() {
    const productsList = document.getElementById('products-list');
    const emptyState = document.getElementById('empty-state');
    
    // Aplicar filtros
    const categoryFilter = document.getElementById('filter-category').value;
    const statusFilter = document.getElementById('filter-status').value;
    const searchTerm = document.getElementById('search-input').value.toLowerCase();
    
    let filteredProducts = allProducts.filter(product => {
        // Filtro de categoria
        if (categoryFilter && product.categoria !== categoryFilter) {
            return false;
        }
        
        // Filtro de status
        if (statusFilter === 'active' && isExpired(product)) {
            return false;
        }
        if (statusFilter === 'expired' && !isExpired(product)) {
            return false;
        }
        
        // Filtro de busca
        if (searchTerm && !product.titulo.toLowerCase().includes(searchTerm)) {
            return false;
        }
        
        return true;
    });
    
    // Ordenar por data (mais recentes primeiro)
    filteredProducts.sort((a, b) => {
        return new Date(b.data_atualizacao) - new Date(a.data_atualizacao);
    });
    
    if (filteredProducts.length === 0) {
        productsList.innerHTML = '';
        emptyState.classList.remove('hidden');
        return;
    }
    
    emptyState.classList.add('hidden');
    
    productsList.innerHTML = filteredProducts.map(product => {
        const expired = isExpired(product);
        const category = categories.find(c => c.id === product.categoria);
        
        return `
            <div class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow ${expired ? 'bg-red-50 border-red-300' : ''}">
                <div class="flex items-start space-x-4">
                    <!-- Imagem -->
                    <img src="${product.imagem_url}" alt="${product.titulo}" class="w-24 h-24 object-cover rounded-lg">
                    
                    <!-- Informações -->
                    <div class="flex-1">
                        <div class="flex items-start justify-between">
                            <div>
                                <h3 class="font-bold text-lg text-gray-900">${product.titulo}</h3>
                                <p class="text-sm text-gray-600 mt-1">
                                    ${category ? category.icone + ' ' + category.nome : 'Sem categoria'}
                                    ${product.brand ? ' • ' + product.brand : ''}
                                </p>
                            </div>
                            ${expired ? '<span class="bg-red-600 text-white px-3 py-1 rounded-full text-sm font-semibold">EXPIRADO</span>' : '<span class="bg-green-600 text-white px-3 py-1 rounded-full text-sm font-semibold">ATIVO</span>'}
                        </div>
                        
                        <!-- Preços -->
                        <div class="mt-3 flex items-center space-x-4">
                            ${product.preco_original > product.preco_atual ? 
                                `<span class="text-gray-500 line-through">R$ ${product.preco_original.toFixed(2)}</span>` : ''}
                            <span class="text-2xl font-bold text-[#1A5F5F]">R$ ${product.preco_atual.toFixed(2)}</span>
                            ${product.desconto_percent > 0 ? 
                                `<span class="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-semibold">${Math.round(product.desconto_percent)}% OFF</span>` : ''}
                        </div>
                        
                        <!-- Informações adicionais -->
                        <div class="mt-3 text-sm text-gray-600">
                            <p>📅 Adicionado: ${formatDate(product.data_atualizacao)}</p>
                            ${product.expiry_date ? 
                                `<p class="${expired ? 'text-red-600 font-semibold' : 'text-yellow-600'}">
                                    ⏰ ${expired ? 'Expirou' : 'Expira'} em: ${formatDate(product.expiry_date)}
                                    ${product.expiry_hours ? ` (${product.expiry_hours}h)` : ''}
                                </p>` : 
                                '<p class="text-green-600">✅ Sem prazo de validade</p>'}
                            <p>🔗 ASIN: ${product.asin}</p>
                        </div>
                        
                        <!-- Ações -->
                        <div class="mt-4 flex space-x-2">
                            <a href="http://localhost:8000/produto/${product.asin}.html" target="_blank" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm transition-colors">
                                👁️ Ver no Site
                            </a>
                            <a href="${product.link_afiliado}" target="_blank" class="bg-[#F5A623] hover:bg-[#E09619] text-white px-4 py-2 rounded-lg text-sm transition-colors">
                                🔗 Ver na Amazon
                            </a>
                            <button class="delete-product-btn bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg text-sm transition-colors" data-asin="${product.asin}">
                                🗑️ Excluir
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

// Excluir produto
async function deleteProduct(asin) {
    if (!confirm('Tem certeza que deseja excluir este produto?')) {
        return;
    }
    
    try {
        const response = await fetch('http://localhost:5001/api/delete-product', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ asin })
        });
        
        if (!response.ok) {
            throw new Error('Erro ao excluir produto');
        }
        
        alert('Produto excluído com sucesso!');
        
        // Recarregar dados
        await loadData();
        
    } catch (error) {
        console.error('Erro ao excluir:', error);
        alert('Erro ao excluir produto: ' + error.message);
    }
}

// Remover todos os produtos expirados
document.getElementById('remove-expired-btn').addEventListener('click', async () => {
    const expiredProducts = allProducts.filter(p => isExpired(p));
    
    if (expiredProducts.length === 0) {
        alert('Não há produtos expirados para remover');
        return;
    }
    
    if (!confirm(`Tem certeza que deseja remover ${expiredProducts.length} produto(s) expirado(s)?`)) {
        return;
    }
    
    try {
        const response = await fetch('http://localhost:5001/api/remove-expired', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (!response.ok) {
            throw new Error('Erro ao remover produtos expirados');
        }
        
        const result = await response.json();
        alert(`${result.removed_count} produto(s) expirado(s) removido(s) com sucesso!`);
        
        // Recarregar dados
        await loadData();
        
    } catch (error) {
        console.error('Erro ao remover expirados:', error);
        alert('Erro ao remover produtos expirados: ' + error.message);
    }
});

// Event listeners para filtros
document.getElementById('filter-category').addEventListener('change', renderProducts);
document.getElementById('filter-status').addEventListener('change', renderProducts);
document.getElementById('search-input').addEventListener('input', renderProducts);

// Event delegation para botões de deletar
document.getElementById('products-list').addEventListener('click', function(e) {
    if (e.target.classList.contains('delete-product-btn') || e.target.closest('.delete-product-btn')) {
        const button = e.target.classList.contains('delete-product-btn') ? e.target : e.target.closest('.delete-product-btn');
        const asin = button.getAttribute('data-asin');
        if (asin) {
            deleteProduct(asin);
        }
    }
});

// Carregar dados ao iniciar
loadData();

// Atualizar a cada 30 segundos
setInterval(loadData, 30000);
