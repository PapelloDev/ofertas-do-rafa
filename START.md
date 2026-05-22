# 🚀 Como Iniciar o Sistema

## ⚡ Início Rápido (1 comando)

```bash
cd "/Volumes/Storage Expansion/Windsurf/CascadeProjects/ofertas-do-rafa" && ./start_interfaces.sh
```

---

## 📋 Passo a Passo

### 1. Abra o Terminal

### 2. Navegue até o projeto
```bash
cd "/Volumes/Storage Expansion/Windsurf/CascadeProjects/ofertas-do-rafa"
```

### 3. Execute o script de inicialização
```bash
./start_interfaces.sh
```

**Isso vai iniciar:**
- ✅ Servidor do site (porta 8000)
- ✅ API Admin (porta 5001)
- ✅ Página admin (porta 8001)

---

## 🌐 URLs para Acessar

Após iniciar, acesse:

### **Site Principal**
```
http://localhost:8000
```

### **Admin - Adicionar Produto**
```
http://localhost:8000/admin/adicionar-produto.html
```

### **Admin - Configurações**
```
http://localhost:8000/admin/configuracoes.html
```

### **Admin - Produtos**
```
http://localhost:8000/admin/produtos.html
```

---

## 🛑 Como Parar

Pressione `Ctrl+C` no terminal onde está rodando

---

## 🐛 Problemas Comuns

### **Erro: "Permission denied"**
```bash
chmod +x start_interfaces.sh
./start_interfaces.sh
```

### **Erro: "Port already in use"**
```bash
# Matar processos nas portas
lsof -ti:8000 | xargs kill -9
lsof -ti:8001 | xargs kill -9
lsof -ti:5001 | xargs kill -9

# Tentar novamente
./start_interfaces.sh
```

### **Erro: "venv not found"**
```bash
# Recriar ambiente virtual
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Iniciar novamente
./start_interfaces.sh
```

---

## 📝 Comandos Úteis

### **Ver processos rodando**
```bash
ps aux | grep python
```

### **Matar todos os processos Python**
```bash
pkill -f python
```

### **Verificar portas em uso**
```bash
lsof -i :8000
lsof -i :8001
lsof -i :5001
```

---

## 🔄 Reiniciar Tudo

```bash
# Parar tudo
pkill -f python

# Iniciar novamente
./start_interfaces.sh
```

---

## ✅ Verificar se Está Funcionando

Após iniciar, você deve ver no terminal:

```
============================================================
🚀 Iniciando Ofertas do Rafa
============================================================

📡 Servidor do Site: http://localhost:8000
🔧 API Admin: http://localhost:5001
⚙️  Admin Interface: http://localhost:8001

Pressione Ctrl+C para parar todos os servidores
============================================================
```

---

## 📚 Mais Informações

- **Guia Completo:** `COMO-USAR.md`
- **Configuração Netlify:** `NETLIFY-CONFIG.md`
- **Variáveis de Ambiente:** `.env.example`
