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
    // Encontrar todos os botões "Ver Oferta"
    const affiliateButtons = document.querySelectorAll('[data-asin]');
    
    affiliateButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const asin = this.getAttribute('data-asin');
            const title = this.getAttribute('data-title');
            const category = this.getAttribute('data-category');
            
            // Registrar clique (não bloqueia navegação)
            trackClick(asin, title, category);
        });
    });
});

// Exportar função para uso global
window.trackClick = trackClick;
