// Layout Components para Site Público - Ofertas do Rafa

// Criar Header
function createHeader(currentPage = '') {
    const header = document.createElement('header');
    header.className = 'header';
    header.innerHTML = `
        <div class="container">
            <nav class="flex items-center justify-between py-4">
                <a href="/index.html" class="flex items-center">
                    <img src="/assets/images/logo/logo-original.jpg" alt="Ofertas do Rafa" class="logo-img">
                </a>
                
                <div class="hidden md:flex items-center gap-2" id="main-nav">
                    <!-- Navigation will be loaded dynamically -->
                </div>
                
                <button id="mobile-menu-btn" class="md:hidden p-2">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
                    </svg>
                </button>
            </nav>
            
            <!-- Mobile Menu -->
            <div id="mobile-menu" class="hidden md:hidden py-4 space-y-2">
                <!-- Mobile navigation will be loaded dynamically -->
            </div>
        </div>
    `;
    
    // Inserir no início do body
    document.body.insertBefore(header, document.body.firstChild);
    
    // Carregar navegação dinâmica
    loadNavigation(currentPage);
    
    // Mobile menu toggle
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    
    mobileMenuBtn.addEventListener('click', () => {
        mobileMenu.classList.toggle('hidden');
    });
}

// Carregar navegação dinâmica baseada nas categorias
async function loadNavigation(currentPage = '') {
    try {
        const response = await fetch('/data/produtos.json');
        const data = await response.json();
        const categorias = data.categorias || [];
        
        // Navegação desktop
        const mainNav = document.getElementById('main-nav');
        let navHTML = `<a href="/index.html" class="nav-link ${currentPage === 'home' ? 'active' : ''}">Início</a>`;
        
        categorias.forEach(cat => {
            const isActive = currentPage === cat.id ? 'active' : '';
            navHTML += `<a href="/categoria/${cat.id}.html" class="nav-link ${isActive}">${cat.icone} ${cat.nome}</a>`;
        });
        
        mainNav.innerHTML = navHTML;
        
        // Navegação mobile
        const mobileMenu = document.getElementById('mobile-menu');
        let mobileHTML = `<a href="/index.html" class="block px-4 py-2 hover:bg-gray-100 rounded ${currentPage === 'home' ? 'bg-gray-100' : ''}">Início</a>`;
        
        categorias.forEach(cat => {
            const isActive = currentPage === cat.id ? 'bg-gray-100' : '';
            mobileHTML += `<a href="/categoria/${cat.id}.html" class="block px-4 py-2 hover:bg-gray-100 rounded ${isActive}">${cat.icone} ${cat.nome}</a>`;
        });
        
        mobileMenu.innerHTML = mobileHTML;
        
    } catch (error) {
        console.error('Erro ao carregar navegação:', error);
        // Fallback para navegação básica
        const mainNav = document.getElementById('main-nav');
        mainNav.innerHTML = `
            <a href="/index.html" class="nav-link ${currentPage === 'home' ? 'active' : ''}">Início</a>
            <a href="/categoria/eletronicos.html" class="nav-link ${currentPage === 'eletronicos' ? 'active' : ''}">📱 Eletrônicos</a>
            <a href="/categoria/corrida.html" class="nav-link ${currentPage === 'corrida' ? 'active' : ''}">🏃 Corrida</a>
            <a href="/categoria/outros.html" class="nav-link ${currentPage === 'outros' ? 'active' : ''}">✌️ Outros</a>
        `;
    }
}

// Criar Footer
function createFooter() {
    const footer = document.createElement('footer');
    footer.className = 'footer';
    footer.innerHTML = `
        <div class="container">
            <div class="text-center mb-6">
                <img src="/assets/images/logo/logo-original.jpg" alt="Ofertas do Rafa" class="logo-img mx-auto mb-4" style="border-radius: 12px;">
                <h3 class="text-xl font-bold mb-2">Ofertas do Rafa</h3>
                <p class="opacity-90">As melhores ofertas da Amazon em um só lugar</p>
            </div>
            
            <div class="disclaimer">
                <h4 class="font-bold mb-2">⚠️ Programa de Afiliados</h4>
                <p>
                    Participamos do <strong>Programa de Associados da Amazon</strong>. 
                    Ao comprar através dos nossos links, você nos ajuda a manter o site 
                    sem custo adicional para você.
                </p>
            </div>
            
            <div class="text-center mt-6 text-sm opacity-75">
                <p>&copy; 2026 Ofertas do Rafa. Todos os direitos reservados.</p>
            </div>
        </div>
    `;
    
    // Inserir no final do body
    document.body.appendChild(footer);
}

// Inicializar layout
function initSiteLayout(currentPage = '') {
    // Aguardar DOM carregar
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            createHeader(currentPage);
            createFooter();
        });
    } else {
        createHeader(currentPage);
        createFooter();
    }
}

// Exportar funções
window.SiteLayout = {
    init: initSiteLayout,
    createHeader: createHeader,
    createFooter: createFooter
};
