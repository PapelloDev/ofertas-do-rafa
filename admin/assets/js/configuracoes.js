// Admin - Configurações

// Carregar configurações
async function loadConfig() {
    try {
        const response = await fetch('http://localhost:8000/data/produtos.json');
        const data = await response.json();
        
        const config = data.config || {};
        
        // Preencher campos
        document.getElementById('site-name').value = config.site_name || '';
        document.getElementById('site-slogan').value = config.site_slogan || '';
        document.getElementById('site-url').value = config.site_url || '';
        document.getElementById('partner-tag').value = config.partner_tag || '';
        document.getElementById('whatsapp-group-url').value = config.whatsapp_group_url || '';
        
    } catch (error) {
        console.error('Erro ao carregar configurações:', error);
        alert('Erro ao carregar configurações');
    }
}

// Salvar configurações
async function saveConfig() {
    const config = {
        site_name: document.getElementById('site-name').value,
        site_slogan: document.getElementById('site-slogan').value,
        site_url: document.getElementById('site-url').value,
        partner_tag: document.getElementById('partner-tag').value,
        whatsapp_group_url: document.getElementById('whatsapp-group-url').value
    };
    
    try {
        const response = await fetch('http://localhost:5001/api/save-config', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(config)
        });
        
        if (response.ok) {
            alert('✅ Configurações salvas com sucesso!');
        } else {
            alert('❌ Erro ao salvar configurações');
        }
    } catch (error) {
        console.error('Erro:', error);
        alert('❌ Erro ao salvar configurações');
    }
}

// Event listeners
document.getElementById('save-config-btn').addEventListener('click', saveConfig);

// Carregar ao iniciar
loadConfig();
