# 📚 Evolution API - Referência Completa de Endpoints

## 🔑 Autenticação

Todas as requisições requerem o header `apikey`:

```bash
-H "apikey: B6D711FCDE4D4FD5936544120E713976"
```

**⚠️ IMPORTANTE**: Altere esta chave no arquivo `.env` antes de usar em produção!

---

## 📱 Gerenciamento de Instâncias

### 1. Criar Instância

```bash
curl -X POST http://localhost:8080/instance/create \
  -H "apikey: B6D711FCDE4D4FD5936544120E713976" \
  -H "Content-Type: application/json" \
  -d '{
    "instanceName": "minha_instancia",
    "integration": "WHATSAPP-BAILEYS"
  }'
```

**Integrações disponíveis:**
- `WHATSAPP-BAILEYS` - WhatsApp Web (QR Code)
- `WHATSAPP-BUSINESS` - WhatsApp Business API (Meta)

**Resposta:**
```json
{
  "instance": {
    "instanceName": "minha_instancia",
    "instanceId": "uuid-here",
    "status": "created"
  }
}
```

---

### 2. Listar Todas as Instâncias

```bash
curl -X GET http://localhost:8080/instance/fetchInstances \
  -H "apikey: B6D711FCDE4D4FD5936544120E713976"
```

**Resposta:**
```json
[
  {
    "id": "uuid",
    "name": "minha_instancia",
    "connectionStatus": "open",
    "integration": "WHATSAPP-BAILEYS",
    "number": "5511999999999",
    "profileName": "Meu Nome",
    "createdAt": "2026-05-12T17:33:50.579Z"
  }
]
```

---

### 3. Conectar Instância (Obter QR Code)

```bash
curl -X GET http://localhost:8080/instance/connect/minha_instancia \
  -H "apikey: B6D711FCDE4D4FD5936544120E713976"
```

**Resposta:**
```json
{
  "code": "2@...",
  "base64": "data:image/png;base64,iVBORw0KG...",
  "pairingCode": null
}
```

---

### 4. Verificar Status da Conexão

```bash
curl -X GET http://localhost:8080/instance/connectionState/minha_instancia \
  -H "apikey: B6D711FCDE4D4FD5936544120E713976"
```

**Resposta:**
```json
{
  "instance": {
    "instanceName": "minha_instancia",
    "state": "open"
  }
}
```

**Estados possíveis:**
- `open` - Conectado
- `connecting` - Conectando
- `close` - Desconectado

---

### 5. Deletar Instância

```bash
curl -X DELETE http://localhost:8080/instance/delete/minha_instancia \
  -H "apikey: B6D711FCDE4D4FD5936544120E713976"
```

**Resposta:**
```json
{
  "status": "SUCCESS",
  "error": false,
  "response": {
    "message": "Instance deleted"
  }
}
```

---

### 6. Reiniciar Instância

```bash
curl -X PUT http://localhost:8080/instance/restart/minha_instancia \
  -H "apikey: B6D711FCDE4D4FD5936544120E713976"
```

---

### 7. Desconectar Instância

```bash
curl -X DELETE http://localhost:8080/instance/logout/minha_instancia \
  -H "apikey: B6D711FCDE4D4FD5936544120E713976"
```

---

## 💬 Envio de Mensagens

### 1. Enviar Mensagem de Texto

```bash
curl -X POST http://localhost:8080/message/sendText/minha_instancia \
  -H "apikey: B6D711FCDE4D4FD5936544120E713976" \
  -H "Content-Type: application/json" \
  -d '{
    "number": "5511999999999",
    "text": "Olá! Esta é uma mensagem de teste."
  }'
```

**Parâmetros opcionais:**
```json
{
  "number": "5511999999999",
  "text": "Mensagem",
  "delay": 1200,
  "quoted": {
    "key": {
      "remoteJid": "5511999999999@s.whatsapp.net",
      "fromMe": false,
      "id": "message-id"
    }
  }
}
```

---

### 2. Enviar Imagem

```bash
curl -X POST http://localhost:8080/message/sendMedia/minha_instancia \
  -H "apikey: B6D711FCDE4D4FD5936544120E713976" \
  -H "Content-Type: application/json" \
  -d '{
    "number": "5511999999999",
    "mediatype": "image",
    "media": "https://example.com/image.jpg",
    "caption": "Confira esta imagem!"
  }'
```

**Ou com base64:**
```json
{
  "number": "5511999999999",
  "mediatype": "image",
  "media": "data:image/png;base64,iVBORw0KGgoAAAA...",
  "caption": "Imagem em base64"
}
```

---

### 3. Enviar Vídeo

```bash
curl -X POST http://localhost:8080/message/sendMedia/minha_instancia \
  -H "apikey: B6D711FCDE4D4FD5936544120E713976" \
  -H "Content-Type: application/json" \
  -d '{
    "number": "5511999999999",
    "mediatype": "video",
    "media": "https://example.com/video.mp4",
    "caption": "Veja este vídeo!"
  }'
```

---

### 4. Enviar Áudio

```bash
curl -X POST http://localhost:8080/message/sendMedia/minha_instancia \
  -H "apikey: B6D711FCDE4D4FD5936544120E713976" \
  -H "Content-Type: application/json" \
  -d '{
    "number": "5511999999999",
    "mediatype": "audio",
    "media": "https://example.com/audio.mp3"
  }'
```

**Para áudio PTT (Push-to-Talk):**
```json
{
  "number": "5511999999999",
  "mediatype": "audio",
  "media": "https://example.com/audio.mp3",
  "ptt": true
}
```

---

### 5. Enviar Documento/PDF

```bash
curl -X POST http://localhost:8080/message/sendMedia/minha_instancia \
  -H "apikey: B6D711FCDE4D4FD5936544120E713976" \
  -H "Content-Type: application/json" \
  -d '{
    "number": "5511999999999",
    "mediatype": "document",
    "media": "https://example.com/documento.pdf",
    "fileName": "Relatório.pdf"
  }'
```

---

### 6. Enviar Localização

```bash
curl -X POST http://localhost:8080/message/sendLocation/minha_instancia \
  -H "apikey: B6D711FCDE4D4FD5936544120E713976" \
  -H "Content-Type: application/json" \
  -d '{
    "number": "5511999999999",
    "latitude": -23.550520,
    "longitude": -46.633308,
    "name": "Avenida Paulista",
    "address": "São Paulo, SP, Brasil"
  }'
```

---

### 7. Enviar Contato

```bash
curl -X POST http://localhost:8080/message/sendContact/minha_instancia \
  -H "apikey: B6D711FCDE4D4FD5936544120E713976" \
  -H "Content-Type: application/json" \
  -d '{
    "number": "5511999999999",
    "contact": {
      "fullName": "João Silva",
      "wuid": "5511888888888",
      "phoneNumber": "5511888888888"
    }
  }'
```

**Múltiplos contatos:**
```json
{
  "number": "5511999999999",
  "contact": [
    {
      "fullName": "João Silva",
      "wuid": "5511888888888",
      "phoneNumber": "5511888888888"
    },
    {
      "fullName": "Maria Santos",
      "wuid": "5511777777777",
      "phoneNumber": "5511777777777"
    }
  ]
}
```

---

### 8. Enviar Lista (List Message)

```bash
curl -X POST http://localhost:8080/message/sendList/minha_instancia \
  -H "apikey: B6D711FCDE4D4FD5936544120E713976" \
  -H "Content-Type: application/json" \
  -d '{
    "number": "5511999999999",
    "title": "Menu de Opções",
    "description": "Escolha uma opção:",
    "buttonText": "Ver Opções",
    "footerText": "Powered by Evolution API",
    "sections": [
      {
        "title": "Seção 1",
        "rows": [
          {
            "title": "Opção 1",
            "description": "Descrição da opção 1",
            "rowId": "option1"
          },
          {
            "title": "Opção 2",
            "description": "Descrição da opção 2",
            "rowId": "option2"
          }
        ]
      }
    ]
  }'
```

---

### 9. Enviar Botões (Button Message)

```bash
curl -X POST http://localhost:8080/message/sendButtons/minha_instancia \
  -H "apikey: B6D711FCDE4D4FD5936544120E713976" \
  -H "Content-Type: application/json" \
  -d '{
    "number": "5511999999999",
    "title": "Título da Mensagem",
    "description": "Escolha uma opção abaixo:",
    "footerText": "Rodapé",
    "buttons": [
      {
        "type": "replyButton",
        "displayText": "Sim"
      },
      {
        "type": "replyButton",
        "displayText": "Não"
      }
    ]
  }'
```

---

### 10. Reagir a Mensagem

```bash
curl -X POST http://localhost:8080/message/sendReaction/minha_instancia \
  -H "apikey: B6D711FCDE4D4FD5936544120E713976" \
  -H "Content-Type: application/json" \
  -d '{
    "key": {
      "remoteJid": "5511999999999@s.whatsapp.net",
      "fromMe": false,
      "id": "message-id-here"
    },
    "reaction": "👍"
  }'
```

**Para remover reação:**
```json
{
  "key": {...},
  "reaction": ""
}
```

---

## 👥 Mensagens para Grupos

### 1. Listar Todos os Chats (Incluindo Grupos)

```bash
curl -X POST http://localhost:8080/chat/findChats/minha_instancia \
  -H "apikey: B6D711FCDE4D4FD5936544120E713976" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Resposta:**
```json
[
  {
    "id": null,
    "remoteJid": "120363123456789012@g.us",
    "pushName": "Nome do Grupo",
    "profilePicUrl": "https://...",
    "updatedAt": "2026-05-12T18:17:38.000Z"
  }
]
```

**Identificar grupos:** IDs terminam com `@g.us`

---

### 2. Enviar Mensagem para Grupo

```bash
curl -X POST http://localhost:8080/message/sendText/minha_instancia \
  -H "apikey: B6D711FCDE4D4FD5936544120E713976" \
  -H "Content-Type: application/json" \
  -d '{
    "number": "120363123456789012@g.us",
    "text": "Olá grupo! Mensagem automática."
  }'
```

**Nota:** Use o mesmo endpoint de mensagens, apenas mude o `number` para o ID do grupo.

---

### 3. Obter Metadados do Grupo

```bash
curl -X GET "http://localhost:8080/group/metadata/minha_instancia?groupJid=120363123456789012@g.us" \
  -H "apikey: B6D711FCDE4D4FD5936544120E713976"
```

---

### 4. Listar Participantes do Grupo

```bash
curl -X GET "http://localhost:8080/group/participants/minha_instancia?groupJid=120363123456789012@g.us" \
  -H "apikey: B6D711FCDE4D4FD5936544120E713976"
```

---

### 5. Criar Grupo

```bash
curl -X POST http://localhost:8080/group/create/minha_instancia \
  -H "apikey: B6D711FCDE4D4FD5936544120E713976" \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Meu Novo Grupo",
    "description": "Descrição do grupo",
    "participants": [
      "5511999999999@s.whatsapp.net",
      "5511888888888@s.whatsapp.net"
    ]
  }'
```

---

### 6. Atualizar Foto do Grupo

```bash
curl -X PUT http://localhost:8080/group/updateGroupPicture/minha_instancia \
  -H "apikey: B6D711FCDE4D4FD5936544120E713976" \
  -H "Content-Type: application/json" \
  -d '{
    "groupJid": "120363123456789012@g.us",
    "image": "https://example.com/image.jpg"
  }'
```

---

### 7. Atualizar Nome do Grupo

```bash
curl -X PUT http://localhost:8080/group/updateGroupSubject/minha_instancia \
  -H "apikey: B6D711FCDE4D4FD5936544120E713976" \
  -H "Content-Type: application/json" \
  -d '{
    "groupJid": "120363123456789012@g.us",
    "subject": "Novo Nome do Grupo"
  }'
```

---

### 8. Atualizar Descrição do Grupo

```bash
curl -X PUT http://localhost:8080/group/updateGroupDescription/minha_instancia \
  -H "apikey: B6D711FCDE4D4FD5936544120E713976" \
  -H "Content-Type: application/json" \
  -d '{
    "groupJid": "120363123456789012@g.us",
    "description": "Nova descrição do grupo"
  }'
```

---

### 9. Adicionar/Remover Participantes

**Adicionar:**
```bash
curl -X PUT http://localhost:8080/group/updateParticipant/minha_instancia \
  -H "apikey: B6D711FCDE4D4FD5936544120E713976" \
  -H "Content-Type: application/json" \
  -d '{
    "groupJid": "120363123456789012@g.us",
    "action": "add",
    "participants": ["5511999999999@s.whatsapp.net"]
  }'
```

**Remover:**
```json
{
  "groupJid": "120363123456789012@g.us",
  "action": "remove",
  "participants": ["5511999999999@s.whatsapp.net"]
}
```

**Promover a Admin:**
```json
{
  "groupJid": "120363123456789012@g.us",
  "action": "promote",
  "participants": ["5511999999999@s.whatsapp.net"]
}
```

**Rebaixar de Admin:**
```json
{
  "groupJid": "120363123456789012@g.us",
  "action": "demote",
  "participants": ["5511999999999@s.whatsapp.net"]
}
```

---

### 10. Sair do Grupo

```bash
curl -X DELETE http://localhost:8080/group/leaveGroup/minha_instancia \
  -H "apikey: B6D711FCDE4D4FD5936544120E713976" \
  -H "Content-Type: application/json" \
  -d '{
    "groupJid": "120363123456789012@g.us"
  }'
```

---

### 11. Obter Link de Convite do Grupo

```bash
curl -X GET "http://localhost:8080/group/inviteCode/minha_instancia?groupJid=120363123456789012@g.us" \
  -H "apikey: B6D711FCDE4D4FD5936544120E713976"
```

---

### 12. Revogar Link de Convite

```bash
curl -X PUT http://localhost:8080/group/revokeInviteCode/minha_instancia \
  -H "apikey: B6D711FCDE4D4FD5936544120E713976" \
  -H "Content-Type: application/json" \
  -d '{
    "groupJid": "120363123456789012@g.us"
  }'
```

---

## 📞 Contatos

### 1. Verificar se Número Existe no WhatsApp

```bash
curl -X POST http://localhost:8080/chat/whatsappNumbers/minha_instancia \
  -H "apikey: B6D711FCDE4D4FD5936544120E713976" \
  -H "Content-Type: application/json" \
  -d '{
    "numbers": ["5511999999999", "5511888888888"]
  }'
```

**Resposta:**
```json
[
  {
    "jid": "5511999999999@s.whatsapp.net",
    "exists": true,
    "number": "5511999999999"
  }
]
```

---

### 2. Obter Foto de Perfil

```bash
curl -X POST http://localhost:8080/chat/fetchProfilePicture/minha_instancia \
  -H "apikey: B6D711FCDE4D4FD5936544120E713976" \
  -H "Content-Type: application/json" \
  -d '{
    "number": "5511999999999@s.whatsapp.net"
  }'
```

---

### 3. Obter Status/Bio do Contato

```bash
curl -X POST http://localhost:8080/chat/fetchProfile/minha_instancia \
  -H "apikey: B6D711FCDE4D4FD5936544120E713976" \
  -H "Content-Type: application/json" \
  -d '{
    "number": "5511999999999@s.whatsapp.net"
  }'
```

---

### 4. Bloquear/Desbloquear Contato

**Bloquear:**
```bash
curl -X PUT http://localhost:8080/chat/blockUser/minha_instancia \
  -H "apikey: B6D711FCDE4D4FD5936544120E713976" \
  -H "Content-Type: application/json" \
  -d '{
    "number": "5511999999999@s.whatsapp.net",
    "status": "block"
  }'
```

**Desbloquear:**
```json
{
  "number": "5511999999999@s.whatsapp.net",
  "status": "unblock"
}
```

---

## 📨 Gerenciamento de Mensagens

### 1. Marcar como Lida

```bash
curl -X PUT http://localhost:8080/chat/markMessageAsRead/minha_instancia \
  -H "apikey: B6D711FCDE4D4FD5936544120E713976" \
  -H "Content-Type: application/json" \
  -d '{
    "readMessages": [
      {
        "remoteJid": "5511999999999@s.whatsapp.net",
        "fromMe": false,
        "id": "message-id-here"
      }
    ]
  }'
```

---

### 2. Deletar Mensagem

```bash
curl -X DELETE http://localhost:8080/message/delete/minha_instancia \
  -H "apikey: B6D711FCDE4D4FD5936544120E713976" \
  -H "Content-Type: application/json" \
  -d '{
    "key": {
      "remoteJid": "5511999999999@s.whatsapp.net",
      "fromMe": true,
      "id": "message-id-here"
    }
  }'
```

---

### 3. Arquivar/Desarquivar Chat

```bash
curl -X PUT http://localhost:8080/chat/archiveChat/minha_instancia \
  -H "apikey: B6D711FCDE4D4FD5936544120E713976" \
  -H "Content-Type: application/json" \
  -d '{
    "lastMessage": {
      "key": {
        "remoteJid": "5511999999999@s.whatsapp.net",
        "fromMe": false,
        "id": "message-id"
      }
    },
    "archive": true
  }'
```

**Desarquivar:** `"archive": false`

---

### 4. Marcar Chat como Não Lido

```bash
curl -X PUT http://localhost:8080/chat/markChatUnread/minha_instancia \
  -H "apikey: B6D711FCDE4D4FD5936544120E713976" \
  -H "Content-Type: application/json" \
  -d '{
    "lastMessage": {
      "key": {
        "remoteJid": "5511999999999@s.whatsapp.net",
        "fromMe": false,
        "id": "message-id"
      }
    }
  }'
```

---

## 👤 Perfil

### 1. Atualizar Nome do Perfil

```bash
curl -X PUT http://localhost:8080/chat/updateProfileName/minha_instancia \
  -H "apikey: B6D711FCDE4D4FD5936544120E713976" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Meu Novo Nome"
  }'
```

---

### 2. Atualizar Status/Bio

```bash
curl -X PUT http://localhost:8080/chat/updateProfileStatus/minha_instancia \
  -H "apikey: B6D711FCDE4D4FD5936544120E713976" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "Disponível 24/7"
  }'
```

---

### 3. Atualizar Foto de Perfil

```bash
curl -X PUT http://localhost:8080/chat/updateProfilePicture/minha_instancia \
  -H "apikey: B6D711FCDE4D4FD5936544120E713976" \
  -H "Content-Type: application/json" \
  -d '{
    "picture": "https://example.com/profile.jpg"
  }'
```

---

### 4. Remover Foto de Perfil

```bash
curl -X DELETE http://localhost:8080/chat/removeProfilePicture/minha_instancia \
  -H "apikey: B6D711FCDE4D4FD5936544120E713976"
```

---

### 5. Obter Configurações de Privacidade

```bash
curl -X GET http://localhost:8080/chat/fetchPrivacySettings/minha_instancia \
  -H "apikey: B6D711FCDE4D4FD5936544120E713976"
```

---

### 6. Atualizar Configurações de Privacidade

```bash
curl -X PUT http://localhost:8080/chat/updatePrivacySettings/minha_instancia \
  -H "apikey: B6D711FCDE4D4FD5936544120E713976" \
  -H "Content-Type: application/json" \
  -d '{
    "privacySettings": {
      "readreceipts": "all",
      "profile": "all",
      "status": "all",
      "online": "all",
      "last": "all",
      "groupadd": "all"
    }
  }'
```

**Valores possíveis:** `all`, `contacts`, `contact_blacklist`, `none`

---

## 📊 Presença e Status

### 1. Enviar Presença (Digitando/Gravando)

```bash
curl -X PUT http://localhost:8080/chat/sendPresence/minha_instancia \
  -H "apikey: B6D711FCDE4D4FD5936544120E713976" \
  -H "Content-Type: application/json" \
  -d '{
    "number": "5511999999999@s.whatsapp.net",
    "presence": "composing",
    "delay": 1200
  }'
```

**Tipos de presença:**
- `composing` - Digitando
- `recording` - Gravando áudio
- `paused` - Parou de digitar

---

### 2. Atualizar Presença (Online/Offline)

```bash
curl -X PUT http://localhost:8080/chat/updatePresence/minha_instancia \
  -H "apikey: B6D711FCDE4D4FD5936544120E713976" \
  -H "Content-Type: application/json" \
  -d '{
    "presence": "available"
  }'
```

**Valores:**
- `available` - Online
- `unavailable` - Offline

---

## 🔔 Webhooks

### 1. Configurar Webhook

```bash
curl -X POST http://localhost:8080/webhook/set/minha_instancia \
  -H "apikey: B6D711FCDE4D4FD5936544120E713976" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://seu-servidor.com/webhook",
    "webhookByEvents": false,
    "events": [
      "QRCODE_UPDATED",
      "MESSAGES_UPSERT",
      "MESSAGES_UPDATE",
      "SEND_MESSAGE",
      "CONNECTION_UPDATE"
    ]
  }'
```

**Eventos disponíveis:**
- `QRCODE_UPDATED` - QR Code atualizado
- `CONNECTION_UPDATE` - Status de conexão mudou
- `MESSAGES_UPSERT` - Nova mensagem recebida
- `MESSAGES_UPDATE` - Mensagem atualizada
- `MESSAGES_DELETE` - Mensagem deletada
- `SEND_MESSAGE` - Mensagem enviada
- `CONTACTS_UPDATE` - Contatos atualizados
- `CONTACTS_UPSERT` - Novos contatos
- `PRESENCE_UPDATE` - Presença atualizada
- `CHATS_UPDATE` - Chats atualizados
- `CHATS_UPSERT` - Novos chats
- `CHATS_DELETE` - Chats deletados
- `GROUPS_UPSERT` - Novos grupos
- `GROUPS_UPDATE` - Grupos atualizados
- `GROUP_PARTICIPANTS_UPDATE` - Participantes do grupo atualizados
- `NEW_TOKEN` - Novo token gerado

---

### 2. Obter Webhook Configurado

```bash
curl -X GET http://localhost:8080/webhook/find/minha_instancia \
  -H "apikey: B6D711FCDE4D4FD5936544120E713976"
```

---

## 🔍 Consultas e Busca

### 1. Buscar Mensagens

```bash
curl -X POST http://localhost:8080/chat/findMessages/minha_instancia \
  -H "apikey: B6D711FCDE4D4FD5936544120E713976" \
  -H "Content-Type: application/json" \
  -d '{
    "remoteJid": "5511999999999@s.whatsapp.net",
    "limit": 50
  }'
```

---

### 2. Buscar Contatos

```bash
curl -X POST http://localhost:8080/chat/findContacts/minha_instancia \
  -H "apikey: B6D711FCDE4D4FD5936544120E713976" \
  -H "Content-Type: application/json" \
  -d '{}'
```

---

## 📝 Formatos de Número

### Números Individuais
```
5511999999999@s.whatsapp.net
```

### Grupos
```
120363123456789012@g.us
```

### Canais/Newsletter
```
120363123456789012@newsletter
```

---

## ⚠️ Códigos de Erro Comuns

| Código | Erro | Solução |
|--------|------|---------|
| 400 | Bad Request | Verifique o formato do JSON |
| 401 | Unauthorized | API Key inválida |
| 404 | Not Found | Instância não existe ou endpoint incorreto |
| 500 | Internal Server Error | Erro no servidor, verifique logs |

---

## 🔗 Links Úteis

- **Interface Web**: http://localhost:3000
- **API Base URL**: http://localhost:8080
- **Documentação Oficial**: https://doc.evolution-api.com
- **GitHub**: https://github.com/evolution-foundation/evolution-api

---

## 📚 Documentação Adicional

- **`SETUP.md`** - Configuração inicial e instalação
- **`INICIO-RAPIDO.md`** - Guia de início rápido
- **`GRUPOS-WHATSAPP.md`** - Guia completo de grupos
- **`SOLUCAO-ERRO-WHATSAPP.md`** - Solução de problemas comuns

---

**Última atualização:** 12 de Maio de 2026
