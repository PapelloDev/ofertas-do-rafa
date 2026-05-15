#!/usr/bin/env python3
"""
Servidor HTTP simples para testar o site e admin localmente
"""

import http.server
import socketserver
import os
import sys
from urllib.parse import unquote

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        """Traduz URLs para caminhos de arquivo corretos"""
        # Decodificar URL
        path = unquote(path)
        
        # Remover query string
        path = path.split('?', 1)[0]
        path = path.split('#', 1)[0]
        
        # Se começa com /admin, servir da pasta admin
        if path.startswith('/admin'):
            # Remover /admin do path
            path = path[6:]  # Remove '/admin'
            if not path or path == '/':
                path = '/login.html'
            base_path = os.path.join(os.getcwd(), 'admin')
            
            # Construir caminho completo
            full_path = os.path.normpath(os.path.join(base_path, path.lstrip('/')))
            
            # Se arquivo não existe no admin, tentar no site (para assets compartilhados)
            if not os.path.exists(full_path):
                site_path = os.path.normpath(os.path.join(os.getcwd(), 'site', path.lstrip('/')))
                if os.path.exists(site_path):
                    return site_path
            
            return full_path
        else:
            # Verificar se é uma URL curta (formato: /abc123)
            # URLs curtas têm 6 caracteres alfanuméricos e não têm extensão
            path_parts = path.strip('/').split('/')
            if len(path_parts) == 1 and len(path_parts[0]) == 6 and path_parts[0].isalnum() and '.' not in path_parts[0]:
                # É uma URL curta, redirecionar para página de redirect
                return os.path.join(os.getcwd(), 'site', 'redirect.html')
            
            # Servir da pasta site
            if path == '/' or path == '':
                path = '/index.html'
            base_path = os.path.join(os.getcwd(), 'site')
            
            # Construir caminho completo
            full_path = os.path.normpath(os.path.join(base_path, path.lstrip('/')))
            
            return full_path
    
    def end_headers(self):
        # Adicionar headers CORS para desenvolvimento
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

def main():
    print("=" * 60)
    print("🚀 Servidor Local - Ofertas do Rafa")
    print("=" * 60)
    print()
    print(f"📂 Diretório base: {os.getcwd()}")
    print(f"🌐 Site: http://localhost:{PORT}")
    print(f"🔐 Admin: http://localhost:{PORT}/admin/login.html")
    print()
    print("Rotas disponíveis:")
    print("  /              → site/index.html")
    print("  /admin         → admin/login.html")
    print("  /admin/*       → admin/*")
    print()
    print("Pressione Ctrl+C para parar o servidor")
    print("=" * 60)
    print()
    
    try:
        with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n✅ Servidor encerrado")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
