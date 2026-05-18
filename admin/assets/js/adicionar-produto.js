// Admin - Adicionar Produto (Modo Manual)

// Estado do produto
let currentProduct = null;

// Aguardar DOM carregar
document.addEventListener('DOMContentLoaded', function() {

// Carregar categorias dinamicamente
async function loadCategories() {
    try {
        const response = await fetch('http://localhost:8000/data/produtos.json');
        const data = await response.json();
        
        const categorySelect = document.getElementById('category');
        categorySelect.innerHTML = '<option value="">Selecione uma categoria</option>';
        
        data.categorias.forEach(cat => {
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
    const patterns = [
        /\/dp\/([A-Z0-9]{10})/,
        /\/gp\/product\/([A-Z0-9]{10})/,
        /\/product\/([A-Z0-9]{10})/,
        /asin=([A-Z0-9]{10})/,
        /\/([A-Z0-9]{10})(?:\/|\?|$)/
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
    
    // Usar preço promocional se existir, senão usar preço atual
    const precoExibicao = product.preco_promocional || product.preco_atual;
    const precoOriginal = product.preco_original || product.preco_atual;
    
    if (precoOriginal > precoExibicao) {
        document.getElementById('preview-price-original').textContent = `De: R$ ${precoOriginal.toFixed(2)}`;
    } else {
        document.getElementById('preview-price-original').textContent = '';
    }
    
    document.getElementById('preview-price-current').textContent = `R$ ${precoExibicao.toFixed(2)}`;
    
    // Recalcular desconto se houver preço promocional
    let desconto = product.desconto_percent;
    if (product.preco_promocional && precoOriginal > product.preco_promocional) {
        desconto = Math.round(((precoOriginal - product.preco_promocional) / precoOriginal) * 100);
    }
    
    document.getElementById('preview-discount').textContent = `${Math.round(desconto)}% OFF`;
    
    // Features
    const featuresList = document.getElementById('features-list');
    if (product.features && product.features.length > 0) {
        featuresList.innerHTML = product.features.map(f => `<li>${f}</li>`).join('');
    } else {
        featuresList.innerHTML = '<li class="text-gray-500">Nenhuma característica disponível</li>';
    }
    
    // Limpar prazo de validade anterior se existir
    const existingExpiry = document.querySelector('.expiry-info');
    if (existingExpiry) {
        existingExpiry.remove();
    }
    
    // Mostrar prazo de validade se existir
    if (product.expiry_date) {
        const expiryDate = new Date(product.expiry_date);
        const expiryInfo = document.createElement('div');
        expiryInfo.className = 'expiry-info mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg';
        expiryInfo.innerHTML = `
            <p class="text-sm font-medium text-yellow-800">
                ⏰ Oferta válida até: ${expiryDate.toLocaleString('pt-BR')}
            </p>
            <p class="text-xs text-yellow-600 mt-1">
                (${product.expiry_hours} horas a partir de agora)
            </p>
        `;
        const previewContainer = document.querySelector('#product-preview .border');
        if (previewContainer) {
            previewContainer.appendChild(expiryInfo);
        }
    }
    
    document.getElementById('product-preview').classList.remove('hidden');
    
    // Scroll para o preview
    document.getElementById('product-preview').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Visualizar produto (botão preview)
document.getElementById('preview-btn').addEventListener('click', function() {
    const affiliateLink = document.getElementById('affiliate-link').value.trim();
    const category = document.getElementById('category').value;
    const title = document.getElementById('manual-title').value.trim();
    const price = parseFloat(document.getElementById('manual-price').value);
    const image = document.getElementById('manual-image').value.trim();
    
    // Validações
    if (!affiliateLink) {
        alert('Por favor, insira o link de afiliado da Amazon');
        return;
    }
    
    if (!category) {
        alert('Por favor, selecione uma categoria');
        return;
    }
    
    if (!title) {
        alert('Por favor, preencha o título do produto');
        return;
    }
    
    if (!price || price <= 0) {
        alert('Por favor, preencha um preço válido');
        return;
    }
    
    if (!image) {
        alert('Por favor, insira a URL da imagem');
        return;
    }
    
    // Extrair ASIN do link
    const asin = extractASIN(affiliateLink) || 'MANUAL_' + Date.now();
    
    // Montar dados do produto
    const originalPrice = parseFloat(document.getElementById('manual-original-price').value) || price;
    const brand = document.getElementById('manual-brand').value.trim() || '';
    const featuresText = document.getElementById('manual-features').value.trim();
    const features = featuresText ? featuresText.split('\n').filter(f => f.trim()) : [];
    
    const discount = originalPrice > price ? 
        Math.round(((originalPrice - price) / originalPrice) * 100) : 0;
    
    currentProduct = {
        asin: asin,
        titulo: title,
        descricao: '',
        categoria: category,
        preco_original: originalPrice,
        preco_atual: price,
        preco_promocional: null, // Será definido ao editar preço
        desconto_percent: discount,
        imagem_url: image,
        link_afiliado: affiliateLink,
        brand: brand,
        features: features,
        data_atualizacao: new Date().toISOString()
    };
    
    // Adicionar prazo de validade
    const expiryHours = parseInt(document.getElementById('expiry-hours').value);
    if (expiryHours > 0) {
        const expiryDate = new Date();
        expiryDate.setHours(expiryDate.getHours() + expiryHours);
        currentProduct.expiry_date = expiryDate.toISOString();
        currentProduct.expiry_hours = expiryHours;
    }
    
    // Mostrar preview
    displayProductPreview(currentProduct);
});

// Publicar produto
document.getElementById('publish-btn').addEventListener('click', async () => {
    if (!currentProduct) {
        alert('Nenhum produto para publicar');
        return;
    }
    
    try {
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
        }
        
        // Fazer deploy automático para GitHub
        try {
            console.log('📤 Iniciando deploy para GitHub...');
            const deployResponse = await fetch('http://localhost:5001/api/deploy', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    asin: currentProduct.asin,
                    message: `Novo produto: ${currentProduct.titulo}`
                })
            });
            
            if (deployResponse.ok) {
                const deployData = await deployResponse.json();
                console.log('✅ Deploy iniciado!', deployData.message);
                alert('✅ Produto publicado com sucesso!\n\n' + 
                      '📱 WhatsApp: Enviado\n' +
                      '🚀 Deploy: Iniciado\n' +
                      '⏱️ Site será atualizado em ~2 minutos\n\n' +
                      'Acesse: https://ofertasdorafa.app.br');
            } else {
                console.warn('⚠️ Deploy falhou, mas produto foi salvo localmente');
                alert('⚠️ Produto salvo localmente.\n\nFaça git push manual para publicar no site.');
            }
        } catch (deployError) {
            console.error('❌ Erro no deploy:', deployError);
            alert('⚠️ Produto salvo localmente.\n\nFaça git push manual para publicar no site.');
        }
        
        // Mostrar mensagem de sucesso
        document.getElementById('product-preview').classList.add('hidden');
        document.getElementById('success-message').classList.remove('hidden');
        
    } catch (error) {
        console.error('Erro ao publicar:', error);
        alert('Erro ao publicar produto: ' + error.message + '\n\nVerifique se o servidor backend está rodando.');
    }
});

}); // Fim DOMContentLoaded
