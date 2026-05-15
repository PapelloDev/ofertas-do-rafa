// Netlify Function para tracking de cliques
const https = require('https');

exports.handler = async (event, context) => {
  // Apenas aceitar POST
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      body: JSON.stringify({ error: 'Method not allowed' })
    };
  }

  try {
    const clickData = JSON.parse(event.body);
    
    // Log do clique (em produção, você pode enviar para um serviço de analytics)
    console.log('📊 Clique registrado:', {
      asin: clickData.asin,
      product: clickData.product_title,
      category: clickData.category,
      timestamp: clickData.timestamp
    });

    // Em produção, você pode:
    // 1. Enviar para Google Analytics
    // 2. Salvar em um banco de dados
    // 3. Enviar para um webhook
    // 4. Usar um serviço como Plausible, Fathom, etc.

    // Por enquanto, apenas retornar sucesso
    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'POST, OPTIONS'
      },
      body: JSON.stringify({ 
        success: true,
        message: 'Clique registrado com sucesso'
      })
    };

  } catch (error) {
    console.error('Erro ao processar clique:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Erro ao processar clique' })
    };
  }
};
