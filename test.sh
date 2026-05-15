#!/bin/bash

# Script de teste do sistema

echo "🧪 Testando Sistema de Ofertas Amazon + WhatsApp"
echo "================================================"
echo ""

# Ativar ambiente virtual
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✓ Ambiente virtual ativado"
else
    echo "❌ Ambiente virtual não encontrado. Execute ./setup.sh primeiro"
    exit 1
fi

echo ""
echo "📋 Executando testes unitários..."
echo ""

# Executar testes com pytest
pytest -v --tb=short

echo ""
echo "✅ Testes concluídos!"
echo ""
echo "Para validar credenciais: python validate_credentials.py"
echo "Para ver cobertura: pytest --cov=. --cov-report=html"
