const fetch = require('node-fetch');

exports.handler = async (event, context) => {
  // Apenas aceitar POST
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      body: JSON.stringify({ error: 'Method not allowed' })
    };
  }

  try {
    const { title, features } = JSON.parse(event.body);

    if (!title) {
      return {
        statusCode: 400,
        body: JSON.stringify({ error: 'Título é obrigatório' })
      };
    }

    // Ler chave da variável de ambiente do Netlify
    const apiKey = process.env.OPENAI_API_KEY;
    const model = process.env.OPENAI_MODEL || 'gpt-4o-mini';

    if (!apiKey) {
      return {
        statusCode: 500,
        body: JSON.stringify({ 
          error: 'Chave API da OpenAI não configurada',
          details: 'Configure OPENAI_API_KEY nas variáveis de ambiente do Netlify'
        })
      };
    }

    // Preparar prompt
    const featuresText = Array.isArray(features) ? features.join('\n- ') : features;
    const prompt = `Crie um gancho de venda curto e persuasivo (máximo 2 linhas) para este produto:

Produto: ${title}

Características:
- ${featuresText}

O gancho deve:
- Ser direto e impactante
- Destacar o principal benefício
- Criar urgência ou desejo
- Usar emojis quando apropriado
- Ter no máximo 150 caracteres

Responda APENAS com o gancho, sem aspas ou formatação extra.`;

    // Chamar OpenAI
    const response = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`
      },
      body: JSON.stringify({
        model: model,
        messages: [
          {
            role: 'system',
            content: 'Você é um especialista em copywriting e vendas. Crie ganchos de venda curtos, persuasivos e impactantes.'
          },
          {
            role: 'user',
            content: prompt
          }
        ],
        max_tokens: 100,
        temperature: 0.8
      })
    });

    if (!response.ok) {
      const error = await response.json();
      return {
        statusCode: response.status,
        body: JSON.stringify({ 
          error: 'Erro ao chamar OpenAI',
          details: error
        })
      };
    }

    const data = await response.json();
    const hook = data.choices[0].message.content.trim();

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type'
      },
      body: JSON.stringify({ hook })
    };

  } catch (error) {
    console.error('Erro:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({ 
        error: 'Erro interno',
        details: error.message
      })
    };
  }
};
