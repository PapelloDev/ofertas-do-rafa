#!/bin/bash

# Script de inicialização do sistema de ofertas Amazon

echo "🚀 Iniciando Sistema de Ofertas Amazon..."
echo ""

# Ativar ambiente virtual
source venv/bin/activate

# Verificar se .env existe
if [ ! -f .env ]; then
    echo "⚠️  Arquivo .env não encontrado!"
    echo "📝 Copie o .env.example para .env e configure suas credenciais:"
    echo "   cp .env.example .env"
    exit 1
fi

# Executar o sistema principal
echo "✅ Ambiente virtual ativado"
echo "🔄 Iniciando monitoramento de ofertas..."
echo ""

python main.py
