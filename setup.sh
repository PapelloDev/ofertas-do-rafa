#!/bin/bash

# Script de configuração inicial do sistema

echo "⚙️  CONFIGURAÇÃO INICIAL DO SISTEMA"
echo "===================================="
echo ""

# Ativar ambiente virtual
source venv/bin/activate
echo "✅ Ambiente virtual ativado"
echo ""

# Verificar se .env existe
if [ ! -f .env ]; then
    echo "📝 Criando arquivo .env..."
    cp .env.example .env
    echo "✅ Arquivo .env criado!"
    echo ""
    echo "⚠️  IMPORTANTE: Configure o arquivo .env com:"
    echo "   - Credenciais Amazon Associates"
    echo "   - Nome da instância Evolution API"
    echo "   - API Key"
    echo ""
    read -p "Pressione ENTER depois de configurar o .env..."
fi

echo ""
echo "� PASSO 1: Obter ID do Grupo"
echo "----------------------------"
echo "⚠️  Certifique-se que a instância WhatsApp está conectada externamente"
echo ""
read -p "Deseja listar os grupos do WhatsApp? (s/n): " list_groups

if [ "$list_groups" = "s" ] || [ "$list_groups" = "S" ]; then
    python get_group_id.py
    echo ""
    echo "📝 Copie o ID do grupo e adicione no arquivo .env"
    echo ""
    read -p "Pressione ENTER depois de adicionar o ID do grupo no .env..."
fi

echo ""
echo "🧪 PASSO 2: Testar Sistema"
echo "-------------------------"
read -p "Deseja executar os testes? (s/n): " run_tests

if [ "$run_tests" = "s" ] || [ "$run_tests" = "S" ]; then
    python test_system.py
fi

echo ""
echo "✅ CONFIGURAÇÃO CONCLUÍDA!"
echo ""
echo "Para iniciar o sistema, execute:"
echo "  ./start.sh"
echo ""
