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
        document.getElementById('openai-api-key').value = config.openai_api_key || '';
        document.getElementById('openai-model').value = config.openai_model || 'gpt-4o-mini';
        
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
        whatsapp_group_url: document.getElementById('whatsapp-group-url').value,
        openai_api_key: document.getElementById('openai-api-key').value,
        openai_model: document.getElementById('openai-model').value
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

// Testar conexão OpenAI
async function testOpenAI() {
    const apiKey = document.getElementById('openai-api-key').value;
    const model = document.getElementById('openai-model').value;
    
    if (!apiKey) {
        alert('⚠️ Por favor, insira a chave API da OpenAI');
        return;
    }
    
    const btn = document.getElementById('test-openai-btn');
    btn.disabled = true;
    btn.textContent = '🔄 Testando...';
    
    try {
        const response = await fetch('http://localhost:5001/api/test-openai', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ api_key: apiKey, model: model })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            alert(`✅ Conexão bem-sucedida!\n\nResposta: ${result.message}`);
        } else {
            alert(`❌ Erro: ${result.error}`);
        }
    } catch (error) {
        console.error('Erro:', error);
        alert('❌ Erro ao testar conexão');
    } finally {
        btn.disabled = false;
        btn.textContent = '🧪 Testar Conexão';
    }
}

// Event listeners
document.getElementById('save-config-btn').addEventListener('click', saveConfig);
document.getElementById('test-openai-btn').addEventListener('click', testOpenAI);

// Carregar ao iniciar
loadConfig();
