#!/bin/bash
# Script para iniciar as interfaces do Ofertas do Rafa

echo "🚀 Iniciando Ofertas do Rafa..."
echo ""

# Ativar ambiente virtual
source venv/bin/activate

# Iniciar API Admin em background
echo "📡 Iniciando API Admin (porta 5001)..."
./venv/bin/python admin_api.py &
API_PID=$!

# Aguardar 2 segundos
sleep 2

# Iniciar servidor do site
echo "🌐 Iniciando servidor do site (porta 8000)..."
echo ""
echo "============================================"
echo "✅ Servidores iniciados!"
echo "============================================"
echo ""
echo "🌐 Site público: http://localhost:8000"
echo "🔐 Admin: http://localhost:8000/admin/login.html"
echo "📡 API: http://localhost:5001"
echo ""
echo "Pressione Ctrl+C para parar todos os servidores"
echo "============================================"
echo ""

# Iniciar servidor do site (em foreground para capturar Ctrl+C)
./venv/bin/python serve_site.py

# Quando o servidor do site parar, matar a API também
echo ""
echo "🛑 Parando servidores..."
kill $API_PID 2>/dev/null
echo "✅ Servidores parados!"
