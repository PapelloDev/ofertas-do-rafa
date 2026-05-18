// Analytics - Tracking de cliques

// Função para registrar clique
async function trackClick(asin, productTitle, category) {
    try {
        const clickData = {
            asin: asin,
            product_title: productTitle,
            category: category,
            timestamp: new Date().toISOString(),
            user_agent: navigator.userAgent,
            referrer: document.referrer
        };

        // Determinar URL da API (localhost ou produção)
        const apiUrl = window.location.hostname === 'localhost' 
            ? 'http://localhost:5001/api/track-click'
            : '/.netlify/functions/track-click';

        // Enviar para API
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(clickData)
        });

        if (response.ok) {
            console.log('✅ Clique registrado:', clickData);
        } else {
            console.warn('⚠️ Resposta não OK:', response.status);
        }
    } catch (error) {
        console.error('❌ Erro ao registrar clique:', error);
        // Não bloquear navegação mesmo se falhar
    }
}

// Adicionar tracking a todos os links de afiliado
document.addEventListener('DOMContentLoaded', function() {
    console.log('🔍 Analytics: Inicializando tracking...');
    
    // Encontrar todos os botões "Ver Oferta"
    const affiliateButtons = document.querySelectorAll('[data-asin]');
    
    console.log(`📊 Analytics: Encontrados ${affiliateButtons.length} botões com data-asin`);
    
    if (affiliateButtons.length === 0) {
        console.warn('⚠️ Analytics: Nenhum botão com data-asin encontrado!');
        return;
    }
    
    affiliateButtons.forEach((button, index) => {
        const asin = button.getAttribute('data-asin');
        const title = button.getAttribute('data-title');
        const category = button.getAttribute('data-category');
        
        console.log(`✅ Analytics: Botão ${index + 1} configurado:`, { asin, title, category });
        
        button.addEventListener('click', function(e) {
            console.log('🖱️ Analytics: Clique detectado no botão!');
            
            const clickAsin = this.getAttribute('data-asin');
            const clickTitle = this.getAttribute('data-title');
            const clickCategory = this.getAttribute('data-category');
            
            console.log('📤 Analytics: Enviando dados:', { clickAsin, clickTitle, clickCategory });
            
            // Registrar clique (não bloqueia navegação)
            trackClick(clickAsin, clickTitle, clickCategory);
        });
    });
    
    console.log('✅ Analytics: Tracking configurado com sucesso!');
});

// Exportar função para uso global
window.trackClick = trackClick;
