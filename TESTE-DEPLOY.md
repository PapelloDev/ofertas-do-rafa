# 🧪 Teste de Deploy Automático - Ofertas do Rafa

## ✅ Sistema Pronto para Testar!

Tudo está funcionando! Vamos testar o fluxo completo de adicionar um produto e ver ele aparecer no site público.

---

## 📋 Pré-requisitos

- ✅ Servidores rodando (`./start_interfaces.sh`)
- ✅ Evolution API conectada (WhatsApp)
- ✅ GitHub configurado
- ✅ Netlify configurado

---

## 🚀 Passo a Passo do Teste

### **1. Acesse o Admin**

URL: http://localhost:8000/admin/adicionar-produto.html

---

### **2. Preencha um Produto de Teste**

Use estes dados de exemplo:

```
Link de Afiliado:
https://amzn.to/3exemplo

Título:
Fone de Ouvido JBL Tune 510BT Bluetooth

Categoria:
Eletrônicos

Preço Atual:
179.90

Preço Original:
299.90

URL da Imagem:
https://m.media-amazon.com/images/I/61EXAMPLE.jpg

Marca:
JBL

Características (uma por linha):
Bluetooth 5.0
Bateria de 40 horas
Design dobrável
Controles integrados
Som JBL Pure Bass

Prazo de Validade:
24 horas (padrão)
```

---

### **3. Visualizar Produto**

1. Clique em **"Visualizar Produto"**
2. Verifique se o preview aparece corretamente
3. Confira:
   - ✅ Imagem
   - ✅ Título
   - ✅ Preços
   - ✅ Desconto calculado
   - ✅ Características
   - ✅ Prazo de validade

---

### **4. Publicar Produto**

1. Clique em **"Publicar Produto"**

2. **Aguarde a mensagem**:
   ```
   ✅ Produto publicado com sucesso!
   
   📱 WhatsApp: Enviado
   🚀 Deploy: Iniciado
   ⏱️ Site será atualizado em ~2 minutos
   
   Acesse: https://ofertasdorafa.app.br
   ```

---

### **5. Verificar WhatsApp**

1. Abra o grupo WhatsApp configurado
2. Deve ter chegado uma mensagem com:
   - ✅ Imagem do produto
   - ✅ Título e descrição
   - ✅ Preço com desconto
   - ✅ Link: `https://ofertasdorafa.netlify.app/produto/{asin}.html`

---

### **6. Verificar GitHub**

1. Acesse: https://github.com/PapelloDev/ofertas-do-rafa/commits/main

2. Deve aparecer um novo commit:
   - ✅ Mensagem: "Novo produto: Fone de Ouvido JBL..."
   - ✅ Timestamp: há alguns segundos
   - ✅ Arquivos alterados:
     - `site/data/produtos.json`
     - `site/produto/{asin}.html`

---

### **7. Verificar Netlify**

1. Acesse: https://app.netlify.com

2. Vá no seu site: **ofertas-do-rafa**

3. Verifique:
   - ✅ Deploy em andamento (amarelo)
   - ✅ Ou deploy concluído (verde)
   - ✅ Tempo: ~1-2 minutos

---

### **8. Verificar Site Público**

**Aguarde ~2 minutos** após publicar, depois:

1. **Acesse**: https://ofertasdorafa.netlify.app

2. **Verifique na home**:
   - ✅ Produto aparece na lista
   - ✅ Imagem carrega
   - ✅ Preço e desconto corretos
   - ✅ Badge de desconto (ex: "29% OFF")

3. **Clique no produto**:
   - ✅ Abre página individual
   - ✅ URL: `https://ofertasdorafa.netlify.app/produto/{asin}.html`
   - ✅ Todas as informações aparecem
   - ✅ Botão "Ver Oferta na Amazon" funciona

4. **Clique em "Ver Oferta na Amazon"**:
   - ✅ Redireciona para Amazon
   - ✅ Link contém seu tag de afiliado: `rahsinc-20`

---

## ✅ Checklist de Sucesso

Marque conforme for testando:

- [ ] Admin carregou corretamente
- [ ] Preview do produto funcionou
- [ ] Mensagem de sucesso apareceu
- [ ] WhatsApp recebeu a mensagem
- [ ] Commit apareceu no GitHub
- [ ] Netlify iniciou rebuild
- [ ] Produto apareceu na home do site
- [ ] Página individual do produto funciona
- [ ] Link de afiliado redireciona corretamente

---

## 🐛 Troubleshooting

### **Problema: Deploy não iniciou**

**Sintomas**: Produto salvo mas não apareceu no GitHub

**Soluções**:
1. Verificar console do navegador (F12)
2. Verificar logs do backend
3. Verificar se GitHub token está correto no `.env`
4. Fazer push manual: `git push origin main`

### **Problema: WhatsApp não enviou**

**Sintomas**: Produto publicado mas WhatsApp não recebeu

**Soluções**:
1. Verificar se Evolution API está rodando
2. Verificar conexão WhatsApp
3. Verificar `WHATSAPP_GROUP_ID` no `.env`
4. Produto foi salvo, só WhatsApp falhou (não é crítico)

### **Problema: Site não atualizou**

**Sintomas**: Produto no GitHub mas não aparece no site

**Soluções**:
1. Aguardar mais 1-2 minutos (Netlify pode demorar)
2. Verificar deploy no Netlify (pode ter falhado)
3. Limpar cache do navegador (Ctrl+Shift+R)
4. Verificar se arquivo `produtos.json` foi atualizado no GitHub

### **Problema: Página do produto não abre**

**Sintomas**: Home funciona mas página individual dá 404

**Soluções**:
1. Verificar se arquivo `.html` foi criado em `site/produto/`
2. Verificar se arquivo foi commitado no GitHub
3. Aguardar rebuild do Netlify completar
4. Verificar URL está correta (com `.html` no final)

---

## 📊 Logs para Monitorar

### **Backend API** (Terminal 1)
```bash
# Deve mostrar:
📤 Iniciando deploy para GitHub...
   Repositório: PapelloDev/ofertas-do-rafa
   Branch: main
   ✅ produtos.json atualizado
   ✅ Página do produto atualizada
✅ Deploy realizado com sucesso!
   Netlify vai fazer rebuild em ~2 minutos
```

### **Console do Navegador** (F12)
```javascript
// Deve mostrar:
📤 Iniciando deploy para GitHub...
✅ Deploy iniciado! Deploy iniciado! Site será atualizado em ~2 minutos.
```

---

## 🎯 Próximos Passos Após Teste

### **Se tudo funcionou** ✅

1. **Adicionar produtos reais**:
   - Busque ofertas em: https://www.amazon.com.br/gp/goldbox
   - Filtre por desconto > 20%
   - Adicione 1-3 produtos por dia

2. **Monitorar resultados**:
   - Acompanhe cliques no WhatsApp
   - Verifique vendas no painel Amazon Associates
   - Ajuste estratégia conforme necessário

3. **Aguardar DNS**:
   - Domínio `ofertasdorafa.app.br` vai funcionar em até 24h
   - Por enquanto use: `ofertasdorafa.netlify.app`

### **Se algo não funcionou** ❌

1. **Anote o erro exato**
2. **Verifique logs** (backend + console)
3. **Tente novamente** com outro produto
4. **Reporte o problema** com detalhes

---

## 📝 Workflow Diário

Após validar que tudo funciona:

```
1. Ligar máquina
   ↓
2. ./start_interfaces.sh
   ↓
3. Buscar ofertas na Amazon
   ↓
4. Adicionar no admin
   ↓
5. Publicar (automático!)
   ↓
6. Aguardar 2 min
   ↓
7. ✅ Produto no ar!
```

**Tempo por produto**: ~3 minutos

---

## 🎉 Parabéns!

Se todos os checkboxes estão marcados, seu sistema está **100% funcional**!

Você agora tem:
- ✅ Site público profissional
- ✅ Deploy automático
- ✅ WhatsApp integrado
- ✅ Custo: ~R$ 40/ano (só domínio)

**Comece a adicionar produtos reais e ganhar comissões!** 💰
