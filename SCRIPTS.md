# 🚀 Scripts de Inicialização

Scripts prontos para facilitar o uso do sistema.

## 📋 Scripts Disponíveis

### **1. `./setup.sh` - Configuração Inicial**
Execute **uma vez** na primeira configuração:

```bash
./setup.sh
```

Este script irá:
- ✅ Criar arquivo `.env` (se não existir)
- ✅ Conectar WhatsApp (QR Code)
- ✅ Listar grupos disponíveis
- ✅ Executar testes do sistema

---

### **2. `./start.sh` - Iniciar Sistema**
Execute para **rodar o sistema** de monitoramento:

```bash
./start.sh
```

Este script irá:
- ✅ Ativar ambiente virtual automaticamente
- ✅ Verificar se `.env` existe
- ✅ Iniciar monitoramento de ofertas

---

### **3. `./connect.sh` - Conectar WhatsApp**
Execute para **conectar ou reconectar** o WhatsApp:

```bash
./connect.sh
```

Use quando:
- WhatsApp desconectar
- Precisar gerar novo QR Code
- Trocar de número

---

### **4. `./get-groups.sh` - Listar Grupos**
Execute para **ver todos os grupos** do WhatsApp:

```bash
./get-groups.sh
```

Mostra:
- Nome de cada grupo
- ID do grupo (para usar no `.env`)

---

### **5. `./test.sh` - Testar Sistema**
Execute para **testar** se tudo está funcionando:

```bash
./test.sh
```

Testa:
- Conexão com Evolution API
- Banco de dados
- Envio de mensagens (opcional)

---

## 🎯 Fluxo de Uso

### **Primeira vez:**

```bash
# 1. Configurar tudo
./setup.sh

# 2. Editar .env com suas credenciais
nano .env

# 3. Iniciar sistema
./start.sh
```

### **Uso diário:**

```bash
# Apenas iniciar
./start.sh
```

### **Se WhatsApp desconectar:**

```bash
./connect.sh
```

### **Para testar:**

```bash
./test.sh
```

---

## ⚙️ Executar em Background

Para rodar o sistema em background:

```bash
nohup ./start.sh > output.log 2>&1 &
```

Para parar:

```bash
ps aux | grep main.py
kill [PID]
```

---

## 🔧 Troubleshooting

### Erro: "Permission denied"

```bash
chmod +x *.sh
```

### Erro: "venv not found"

```bash
python3 -m venv venv
pip install -r requirements.txt
```

### Ver logs em tempo real

```bash
tail -f deal_monitor.log
```

---

## 📝 Notas

- Todos os scripts **ativam automaticamente** o ambiente virtual
- Não precisa executar `source venv/bin/activate` manualmente
- Os scripts verificam se o `.env` existe antes de executar

---

**Desenvolvido para facilitar o uso do sistema de ofertas Amazon** 🛒🤖
