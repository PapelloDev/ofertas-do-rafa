// Admin - Adicionar Produto
// Extração automática de dados da Amazon

// Verificar autenticação
if (!sessionStorage.getItem('admin_authenticated')) {
    window.location.href = 'login.html';
}

// Modo manual é o padrão agora

// Logout
document.getElementById('logout-btn')?.addEventListener('click', () => {
    sessionStorage.removeItem('admin_authenticated');
    sessionStorage.removeItem('admin_login_time');
    window.location.href = 'login.html';
});

// Estado do produto
let currentProduct = null;

// Carregar categorias disponíveis
async function loadCategories() {
    try {
        const response = await fetch('../site/data/produtos.json');
        const data = await response.json();
        
        const categorySelect = document.getElementById('category');
        const categories = data.categorias || [];
        
        // Limpar opções existentes (exceto a primeira)
        categorySelect.innerHTML = '<option value="">Selecione uma categoria</option>';
        
        // Adicionar categorias
        categories.forEach(cat => {
            const option = document.createElement('option');
            option.value = cat.id;
            option.textContent = `${cat.icone} ${cat.nome}`;
            categorySelect.appendChild(option);
        });
        
    } catch (error) {
        console.error('Erro ao carregar categorias:', error);
    }
}

// Carregar categorias ao iniciar
loadCategories();

// Extrair ASIN do link
function extractASIN(url) {
    // Padrões de URL da Amazon
    const patterns = [
        /\/dp\/([A-Z0-9]{10})/,           // /dp/B08XYZ1234
        /\/gp\/product\/([A-Z0-9]{10})/,  // /gp/product/B08XYZ1234
        /\/product\/([A-Z0-9]{10})/,      // /product/B08XYZ1234
        /asin=([A-Z0-9]{10})/,            // ?asin=B08XYZ1234
        /\/([A-Z0-9]{10})(?:\/|\?|$)/     // Genérico
    ];
    
    for (const pattern of patterns) {
        const match = url.match(pattern);
        if (match && match[1]) {
            return match[1];
        }
    }
    
    return null;
}

// Mostrar preview do produto
function displayProductPreview(product) {
    document.getElementById('preview-image').src = product.imagem_url;
    document.getElementById('preview-title').textContent = product.titulo;
    document.getElementById('preview-brand').textContent = product.brand ? `Marca: ${product.brand}` : '';
    
    if (product.preco_original > product.preco_atual) {
        document.getElementById('preview-price-original').textContent = `De: R$ ${product.preco_original.toFixed(2)}`;
    } else {
        document.getElementById('preview-price-original').textContent = '';
    }
    
    document.getElementById('preview-price-current').textContent = `R$ ${product.preco_atual.toFixed(2)}`;
    document.getElementById('preview-discount').textContent = `${Math.round(product.desconto_percent)}% OFF`;
    
    // Features
    const featuresList = document.getElementById('features-list');
    if (product.features && product.features.length > 0) {
        featuresList.innerHTML = product.features.map(f => `<li>${f}</li>`).join('');
    } else {
        featuresList.innerHTML = '<li class="text-gray-500">Nenhuma característica disponível</li>';
    }
    
    // Mostrar prazo de validade se existir
    if (product.expiry_date) {
        const expiryDate = new Date(product.expiry_date);
        const expiryInfo = document.createElement('div');
        expiryInfo.className = 'mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg';
        expiryInfo.innerHTML = `
            <p class="text-sm font-medium text-yellow-800">
                ⏰ Oferta válida até: ${expiryDate.toLocaleString('pt-BR')}
            </p>
            <p class="text-xs text-yellow-600 mt-1">
                (${product.expiry_hours} horas a partir de agora)
            </p>
        `;
        document.getElementById('product-preview').querySelector('.bg-white').appendChild(expiryInfo);
    }
    
    document.getElementById('product-preview').classList.remove('hidden');
}

// Publicar produto
document.getElementById('publish-btn').addEventListener('click', async () => {
    if (!currentProduct) {
        alert('Nenhum produto para publicar');
        return;
    }
    
    try {
        // Ler produtos existentes
        const response = await fetch('../site/data/produtos.json');
        const data = await response.json();
        
        // Adicionar novo produto
        data.produtos.push(currentProduct);
        
        // Atualizar última atualização
        data.config.ultima_atualizacao = new Date().toISOString();
        
        // Salvar (em produção, isso seria uma chamada à API)
        // Por enquanto, vamos simular e mostrar os dados
        console.log('Produto a ser salvo:', currentProduct);
        console.log('Dados completos:', data);
        
        // Chamar API para salvar
        const saveResponse = await fetch('http://localhost:5001/api/save-product', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(currentProduct)
        });
        
        if (!saveResponse.ok) {
            throw new Error('Erro ao salvar produto');
        }
        
        // Gerar página do produto
        await fetch('http://localhost:5001/api/generate-product-page', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ asin: currentProduct.asin })
        });
        
        // Enviar para WhatsApp
        try {
            const whatsappResponse = await fetch('http://localhost:5001/api/send-to-whatsapp', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ asin: currentProduct.asin })
            });
            
            if (whatsappResponse.ok) {
                console.log('✅ Produto enviado para WhatsApp');
            } else {
                console.warn('⚠️ Falha ao enviar para WhatsApp (produto publicado com sucesso)');
            }
        } catch (whatsappError) {
            console.warn('⚠️ Erro ao enviar para WhatsApp:', whatsappError);
            // Não bloquear o fluxo se WhatsApp falhar
        }
        
        // Mostrar mensagem de sucesso
        document.getElementById('product-preview').classList.add('hidden');
        document.getElementById('success-message').classList.remove('hidden');
        
    } catch (error) {
        console.error('Erro ao publicar:', error);
        alert('Erro ao publicar produto: ' + error.message + '\n\nVerifique se o servidor backend está rodando.');
    }
});
