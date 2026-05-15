// Layout padrão do Admin - Componentes reutilizáveis

// Verificar autenticação
function checkAuth() {
    if (!sessionStorage.getItem('admin_authenticated')) {
        window.location.href = '/admin/login.html';
        return false;
    }
    return true;
}

// Logout
function setupLogout() {
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            sessionStorage.removeItem('admin_authenticated');
            sessionStorage.removeItem('admin_login_time');
            window.location.href = '/admin/login.html';
        });
    }
}

// Criar header padrão
function createAdminHeader(currentPage = '') {
    return `
        <!-- Header -->
        <header class="bg-gradient-to-r from-[#1A5F5F] to-[#0D4444] text-white shadow-lg">
            <div class="container mx-auto px-4 py-4">
                <div class="flex items-center justify-between">
                    <div class="flex items-center space-x-4">
                        <a href="/admin/index.html" class="flex items-center space-x-3 hover:opacity-80 transition-opacity">
                            <span class="text-3xl">📦</span>
                            <div>
                                <h1 class="text-2xl font-bold">Ofertas do Rafa</h1>
                                <p class="text-xs text-white/70">Painel Administrativo</p>
                            </div>
                        </a>
                    </div>
                    <button id="logout-btn" class="bg-red-600 hover:bg-red-700 px-4 py-2 rounded-lg transition-colors font-semibold flex items-center space-x-2">
                        <span>🚪</span>
                        <span>Sair</span>
                    </button>
                </div>
            </div>
        </header>

        <!-- Navigation -->
        <nav class="bg-white shadow-md border-b border-gray-200">
            <div class="container mx-auto px-4">
                <div class="flex space-x-1 py-2">
                    <a href="/admin/index.html" class="nav-link ${currentPage === 'dashboard' ? 'active' : ''}">
                        <span>🏠</span>
                        <span>Dashboard</span>
                    </a>
                    <a href="/admin/adicionar-produto.html" class="nav-link ${currentPage === 'adicionar' ? 'active' : ''}">
                        <span>➕</span>
                        <span>Adicionar Produto</span>
                    </a>
                    <a href="/admin/listar-produtos.html" class="nav-link ${currentPage === 'listar' ? 'active' : ''}">
                        <span>📋</span>
                        <span>Gerenciar Produtos</span>
                    </a>
                    <a href="/admin/categorias.html" class="nav-link ${currentPage === 'categorias' ? 'active' : ''}">
                        <span>🏷️</span>
                        <span>Categorias</span>
                    </a>
                </div>
            </div>
        </nav>

        <style>
            .nav-link {
                display: flex;
                align-items: center;
                gap: 0.5rem;
                padding: 0.75rem 1.25rem;
                color: #4B5563;
                font-weight: 500;
                border-radius: 0.5rem;
                transition: all 0.2s;
                text-decoration: none;
            }
            .nav-link:hover {
                background-color: #F3F4F6;
                color: #1A5F5F;
            }
            .nav-link.active {
                background-color: #1A5F5F;
                color: white;
            }
        </style>
    `;
}

// Criar footer padrão
function createAdminFooter() {
    return `
        <!-- Footer -->
        <footer class="bg-gray-100 border-t border-gray-200 mt-12">
            <div class="container mx-auto px-4 py-6">
                <div class="flex flex-col md:flex-row justify-between items-center text-sm text-gray-600">
                    <div class="mb-2 md:mb-0">
                        <p>© 2026 Ofertas do Rafa - Painel Administrativo</p>
                    </div>
                    <div class="flex space-x-4">
                        <a href="https://ofertasdorafa.netlify.app" target="_blank" class="hover:text-[#1A5F5F] transition-colors">
                            🌐 Ver Site Público
                        </a>
                        <a href="https://github.com/PapelloDev/ofertas-do-rafa" target="_blank" class="hover:text-[#1A5F5F] transition-colors">
                            📦 GitHub
                        </a>
                    </div>
                </div>
            </div>
        </footer>
    `;
}

// Inicializar layout
function initAdminLayout(currentPage = '') {
    // Verificar autenticação
    if (!checkAuth()) return;
    
    // Setup logout
    setupLogout();
    
    // Adicionar classes ao body
    document.body.classList.add('bg-gray-50', 'min-h-screen', 'flex', 'flex-col');
    
    // Criar container principal se não existir
    const main = document.querySelector('main');
    if (main) {
        main.classList.add('flex-1', 'container', 'mx-auto', 'px-4', 'py-6');
    }
}

// Exportar funções
window.AdminLayout = {
    checkAuth,
    setupLogout,
    createHeader: createAdminHeader,
    createFooter: createAdminFooter,
    init: initAdminLayout
};
