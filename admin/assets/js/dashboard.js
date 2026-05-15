// Dashboard Analytics

let topProductsChart, categoryChart, timelineChart;

// Carregar dados
async function loadDashboard() {
    try {
        // Carregar analytics
        const analyticsResponse = await fetch('http://localhost:5001/api/analytics');
        const analytics = await analyticsResponse.json();
        
        // Carregar produtos
        const productsResponse = await fetch('http://localhost:8000/data/produtos.json');
        const productsData = await productsResponse.json();
        
        // Atualizar cards
        updateStatsCards(analytics, productsData);
        
        // Criar gráficos
        createTopProductsChart(analytics);
        createCategoryChart(analytics);
        createTimelineChart(analytics);
        
        // Mostrar produtos expirando
        showExpiringProducts(productsData);
        
    } catch (error) {
        console.error('Erro ao carregar dashboard:', error);
    }
}

// Atualizar cards de estatísticas
function updateStatsCards(analytics, productsData) {
    const summary = analytics.summary || {};
    
    // Total de cliques
    document.getElementById('total-clicks').textContent = summary.total_clicks || 0;
    
    // Total de produtos
    document.getElementById('total-products').textContent = productsData.produtos?.length || 0;
    
    // Cliques hoje
    const today = new Date().toISOString().split('T')[0];
    const clicksToday = summary.clicks_by_date?.[today] || 0;
    document.getElementById('clicks-today').textContent = clicksToday;
    
    // Produto mais clicado
    const clicksByProduct = summary.clicks_by_product || {};
    const topProduct = Object.values(clicksByProduct).sort((a, b) => b.count - a.count)[0];
    document.getElementById('top-product-clicks').textContent = topProduct?.count || 0;
}

// Gráfico de Top Produtos
function createTopProductsChart(analytics) {
    const clicksByProduct = analytics.summary?.clicks_by_product || {};
    
    // Ordenar e pegar top 5
    const sorted = Object.entries(clicksByProduct)
        .map(([asin, data]) => ({ asin, ...data }))
        .sort((a, b) => b.count - a.count)
        .slice(0, 5);
    
    const labels = sorted.map(p => p.title?.substring(0, 30) + '...' || p.asin);
    const data = sorted.map(p => p.count);
    
    const ctx = document.getElementById('topProductsChart');
    
    if (topProductsChart) {
        topProductsChart.destroy();
    }
    
    topProductsChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Cliques',
                data: data,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.8)',
                    'rgba(54, 162, 235, 0.8)',
                    'rgba(255, 206, 86, 0.8)',
                    'rgba(75, 192, 192, 0.8)',
                    'rgba(153, 102, 255, 0.8)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            }
        }
    });
}

// Gráfico de Categorias
function createCategoryChart(analytics) {
    const clicksByCategory = analytics.summary?.clicks_by_category || {};
    
    const labels = Object.keys(clicksByCategory);
    const data = Object.values(clicksByCategory);
    
    const ctx = document.getElementById('categoryChart');
    
    if (categoryChart) {
        categoryChart.destroy();
    }
    
    categoryChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels.map(l => l.charAt(0).toUpperCase() + l.slice(1)),
            datasets: [{
                data: data,
                backgroundColor: [
                    'rgba(26, 95, 95, 0.8)',
                    'rgba(245, 166, 35, 0.8)',
                    'rgba(52, 152, 219, 0.8)',
                    'rgba(46, 204, 113, 0.8)',
                    'rgba(155, 89, 182, 0.8)'
                ],
                borderColor: [
                    'rgba(26, 95, 95, 1)',
                    'rgba(245, 166, 35, 1)',
                    'rgba(52, 152, 219, 1)',
                    'rgba(46, 204, 113, 1)',
                    'rgba(155, 89, 182, 1)'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

// Gráfico de Timeline
function createTimelineChart(analytics) {
    const clicksByDate = analytics.summary?.clicks_by_date || {};
    
    // Últimos 7 dias
    const last7Days = [];
    for (let i = 6; i >= 0; i--) {
        const date = new Date();
        date.setDate(date.getDate() - i);
        last7Days.push(date.toISOString().split('T')[0]);
    }
    
    const labels = last7Days.map(date => {
        const d = new Date(date);
        return d.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' });
    });
    
    const data = last7Days.map(date => clicksByDate[date] || 0);
    
    const ctx = document.getElementById('timelineChart');
    
    if (timelineChart) {
        timelineChart.destroy();
    }
    
    timelineChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Cliques',
                data: data,
                fill: true,
                backgroundColor: 'rgba(26, 95, 95, 0.2)',
                borderColor: 'rgba(26, 95, 95, 1)',
                borderWidth: 3,
                tension: 0.4,
                pointBackgroundColor: 'rgba(26, 95, 95, 1)',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 5,
                pointHoverRadius: 7
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            }
        }
    });
}

// Mostrar produtos expirando
function showExpiringProducts(productsData) {
    const produtos = productsData.produtos || [];
    const now = new Date();
    
    // Filtrar produtos que expiram nas próximas 24 horas
    const expiring = produtos.filter(p => {
        if (!p.expiry_date) return false;
        const expiryDate = new Date(p.expiry_date);
        const hoursUntilExpiry = (expiryDate - now) / (1000 * 60 * 60);
        return hoursUntilExpiry > 0 && hoursUntilExpiry <= 24;
    }).sort((a, b) => new Date(a.expiry_date) - new Date(b.expiry_date));
    
    const container = document.getElementById('expiring-products');
    
    if (expiring.length === 0) {
        container.innerHTML = '<p class="text-gray-500 text-center py-8">Nenhum produto próximo de expirar</p>';
        return;
    }
    
    container.innerHTML = expiring.map(product => {
        const expiryDate = new Date(product.expiry_date);
        const hoursLeft = Math.floor((expiryDate - now) / (1000 * 60 * 60));
        const minutesLeft = Math.floor(((expiryDate - now) % (1000 * 60 * 60)) / (1000 * 60));
        
        return `
            <div class="flex items-center justify-between p-4 bg-yellow-50 border-l-4 border-yellow-500 rounded-lg">
                <div class="flex items-center space-x-4">
                    <img src="${product.imagem_url}" alt="${product.titulo}" class="w-16 h-16 object-cover rounded-lg">
                    <div>
                        <h3 class="font-semibold text-gray-900">${product.titulo}</h3>
                        <p class="text-sm text-yellow-700">⏰ Expira em ${hoursLeft}h ${minutesLeft}min</p>
                    </div>
                </div>
                <a href="listar-produtos.html" class="bg-yellow-500 hover:bg-yellow-600 text-white px-4 py-2 rounded-lg text-sm font-semibold transition-colors">
                    Gerenciar
                </a>
            </div>
        `;
    }).join('');
}

// Carregar ao iniciar
loadDashboard();

// Atualizar a cada 30 segundos
setInterval(loadDashboard, 30000);
