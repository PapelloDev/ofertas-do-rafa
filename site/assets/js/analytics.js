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

        // Enviar para API
        await fetch('http://localhost:5001/api/track-click', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(clickData)
        });

        console.log('✅ Clique registrado:', clickData);
    } catch (error) {
        console.error('❌ Erro ao registrar clique:', error);
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
