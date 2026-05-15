# 🚀 Plano Futuro - Interface Multi-Grupos

Planejamento para evolução do sistema com interface de criação de grupos por nicho.

---

## 🎯 Objetivo

Permitir que o usuário crie múltiplos grupos de WhatsApp, cada um monitorando um nicho específico de produtos, com configurações independentes.

---

## 📋 Funcionalidades Planejadas

### 1. Interface de Gerenciamento de Grupos

**Descrição:** Interface (CLI ou Web) para criar e gerenciar grupos de monitoramento.

**Funcionalidades:**
- ✅ Criar novo grupo de monitoramento
- ✅ Listar grupos existentes
- ✅ Editar configurações de grupo
- ✅ Ativar/desativar grupo
- ✅ Excluir grupo
- ✅ Ver estatísticas de grupo

**Exemplo de Uso:**
```bash
# CLI
python manage_groups.py create --name "Fones Bluetooth" --niche electronics

# Web Interface
http://localhost:5000/groups/create
```

---

### 2. Configuração por Nicho

**Descrição:** Cada grupo tem configurações específicas para seu nicho.

**Configurações por Grupo:**

| Campo | Descrição | Exemplo |
|-------|-----------|---------|
| `name` | Nome do grupo | "Ofertas de Fones" |
| `niche` | Nicho de produtos | "fones bluetooth" |
| `whatsapp_group_id` | ID do grupo WhatsApp | "120363...@g.us" |
| `keywords` | Palavras-chave de busca | ["fone bluetooth", "airpods"] |
| `search_index` | Categoria Amazon | "Electronics" |
| `min_discount` | Desconto mínimo (%) | 20 |
| `max_price` | Preço máximo (R$) | 500.00 |
| `min_rating` | Avaliação mínima | 4.0 |
| `check_interval` | Intervalo de verificação (min) | 30 |
| `max_products_per_check` | Produtos por verificação | 5 |
| `active` | Grupo ativo | true |

**Exemplo de Configuração:**
```json
{
  "id": "grupo_001",
  "name": "Ofertas de Fones Premium",
  "niche": "fones_bluetooth",
  "whatsapp_group_id": "120363123456789012@g.us",
  "keywords": [
    "fone bluetooth",
    "airpods",
    "sony wh-1000xm5"
  ],
  "search_index": "Electronics",
  "filters": {
    "min_discount": 25,
    "max_price": 800.00,
    "min_rating": 4.5,
    "brands": ["Sony", "JBL", "Apple", "Bose"],
    "delivery_flags": ["Prime"]
  },
  "schedule": {
    "check_interval": 30,
    "max_products_per_check": 3,
    "active_hours": {
      "start": "08:00",
      "end": "22:00"
    }
  },
  "active": true,
  "created_at": "2026-05-14T10:00:00Z",
  "updated_at": "2026-05-14T10:00:00Z"
}
```

---

### 3. Banco de Dados de Grupos

**Descrição:** Armazenamento persistente de configurações de grupos.

**Opções de Implementação:**

#### Opção A: JSON File (Simples)
```
groups/
  ├── grupo_001.json
  ├── grupo_002.json
  └── grupo_003.json
```

**Prós:**
- Simples de implementar
- Fácil de editar manualmente
- Sem dependências externas

**Contras:**
- Não escala bem
- Sem queries complexas
- Sem controle de concorrência

#### Opção B: SQLite (Recomendado)
```sql
CREATE TABLE groups (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    niche TEXT NOT NULL,
    whatsapp_group_id TEXT NOT NULL,
    keywords JSON NOT NULL,
    search_index TEXT,
    filters JSON,
    schedule JSON,
    active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE group_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_id TEXT NOT NULL,
    products_found INTEGER,
    products_sent INTEGER,
    last_check TIMESTAMP,
    FOREIGN KEY (group_id) REFERENCES groups(id)
);
```

**Prós:**
- Queries SQL
- Relacional
- Sem servidor externo
- Boa performance

**Contras:**
- Mais complexo que JSON
- Requer ORM ou SQL direto

#### Opção C: PostgreSQL (Produção)
- Para escala maior
- Múltiplos processos
- Backup automático

---

### 4. Fluxo de Monitoramento Multi-Grupo

**Arquitetura:**

```
┌─────────────────────────────────────────┐
│         Scheduler Principal             │
│  (Gerencia todos os grupos)             │
└─────────────────┬───────────────────────┘
                  │
                  ├─► Grupo 1: Fones (30min)
                  │   └─► Amazon API → WhatsApp
                  │
                  ├─► Grupo 2: Smartwatches (60min)
                  │   └─► Amazon API → WhatsApp
                  │
                  └─► Grupo 3: Mouses (45min)
                      └─► Amazon API → WhatsApp
```

**Implementação:**

```python
class GroupMonitor:
    """Monitor de um grupo específico"""
    
    def __init__(self, group_config):
        self.config = group_config
        self.amazon = AmazonClient(...)
        self.whatsapp = EvolutionClient(...)
    
    def check_deals(self):
        """Verifica ofertas para este grupo"""
        if not self.config['active']:
            return
        
        # Buscar produtos
        products = self.amazon.search_items(
            keywords=self.config['keywords'],
            search_index=self.config['search_index'],
            min_saving_percent=self.config['filters']['min_discount']
        )
        
        # Filtrar
        filtered = self.filter_products(products)
        
        # Enviar para WhatsApp
        self.whatsapp.send_deals_to_group(
            filtered,
            self.config['whatsapp_group_id']
        )


class MultiGroupScheduler:
    """Scheduler para múltiplos grupos"""
    
    def __init__(self):
        self.groups = self.load_groups()
        self.monitors = {}
    
    def start(self):
        """Inicia monitoramento de todos os grupos"""
        for group in self.groups:
            monitor = GroupMonitor(group)
            interval = group['schedule']['check_interval']
            
            # Agendar verificação periódica
            schedule.every(interval).minutes.do(monitor.check_deals)
        
        # Loop principal
        while True:
            schedule.run_pending()
            time.sleep(60)
```

---

### 5. Interface de Usuário

#### Opção A: CLI (Fase 1)

```bash
# Criar grupo
python manage_groups.py create

# Listar grupos
python manage_groups.py list

# Editar grupo
python manage_groups.py edit grupo_001

# Ativar/Desativar
python manage_groups.py toggle grupo_001

# Ver estatísticas
python manage_groups.py stats grupo_001
```

#### Opção B: Web Interface (Fase 2)

**Stack Sugerida:**
- Backend: Flask ou FastAPI
- Frontend: React ou Vue.js
- Estilo: TailwindCSS

**Telas:**

1. **Dashboard**
   - Lista de grupos
   - Status (ativo/inativo)
   - Última verificação
   - Produtos enviados hoje

2. **Criar/Editar Grupo**
   - Formulário com todos os campos
   - Preview de configuração
   - Teste de busca

3. **Estatísticas**
   - Gráficos de produtos encontrados
   - Taxa de envio
   - Horários de pico

4. **Logs**
   - Histórico de envios
   - Erros
   - Performance

---

### 6. Nichos Pré-Configurados

**Templates de Nicho:**

```python
NICHE_TEMPLATES = {
    'fones_bluetooth': {
        'name': 'Fones Bluetooth',
        'keywords': ['fone bluetooth', 'headphone', 'earbuds'],
        'search_index': 'Electronics',
        'filters': {
            'min_discount': 20,
            'max_price': 800,
            'min_rating': 4.0
        }
    },
    'smartwatches': {
        'name': 'Smartwatches',
        'keywords': ['smartwatch', 'relógio inteligente'],
        'search_index': 'Electronics',
        'filters': {
            'min_discount': 15,
            'max_price': 1500,
            'min_rating': 4.0
        }
    },
    'perifericos_gamer': {
        'name': 'Periféricos Gamer',
        'keywords': ['mouse gamer', 'teclado mecânico', 'headset gamer'],
        'search_index': 'VideoGames',
        'filters': {
            'min_discount': 25,
            'max_price': 600,
            'min_rating': 4.5
        }
    }
}
```

**Uso:**
```python
# Criar grupo a partir de template
group = create_group_from_template('fones_bluetooth')
group['whatsapp_group_id'] = '120363...'
save_group(group)
```

---

## 📊 Estrutura de Arquivos Futura

```
windsurf-project/
├── amazon_auth.py              # ✅ Já implementado
├── amazon_client.py            # A implementar
├── evolution_client.py         # ✅ Já existe
├── group_manager.py            # Gerenciamento de grupos
├── group_monitor.py            # Monitor individual
├── multi_group_scheduler.py   # Scheduler multi-grupo
├── manage_groups.py            # CLI de gerenciamento
├── config/
│   └── niche_templates.json   # Templates de nichos
├── groups/                     # Configurações de grupos
│   ├── groups.db              # SQLite (recomendado)
│   └── *.json                 # Ou arquivos JSON
├── web/                        # Interface web (fase 2)
│   ├── app.py                 # Flask/FastAPI
│   ├── static/
│   └── templates/
└── tests/
    ├── test_group_manager.py
    ├── test_group_monitor.py
    └── test_multi_scheduler.py
```

---

## 🔄 Fases de Implementação

### Fase 1: Fundação (Atual)
- ✅ Autenticação Amazon
- ✅ Cliente Evolution
- ✅ Testes unitários
- ⏳ Cliente Amazon (SearchItems)
- ⏳ Monitor básico (1 grupo)

### Fase 2: Multi-Grupo CLI
- ⏳ Banco de dados (SQLite)
- ⏳ Group Manager
- ⏳ Multi-Group Scheduler
- ⏳ CLI de gerenciamento
- ⏳ Templates de nichos

### Fase 3: Interface Web
- ⏳ Backend API (Flask/FastAPI)
- ⏳ Frontend (React/Vue)
- ⏳ Dashboard
- ⏳ CRUD de grupos
- ⏳ Estatísticas e logs

### Fase 4: Otimizações
- ⏳ Cache distribuído (Redis)
- ⏳ Fila de mensagens (RabbitMQ/Celery)
- ⏳ Métricas e alertas
- ⏳ Backup automático
- ⏳ Deploy em produção

---

## 💡 Considerações Técnicas

### Rate Limiting
- Distribuir requests entre grupos
- Respeitar TPS global da API
- Priorizar grupos mais ativos

### Performance
- Cache de produtos já enviados
- Deduplicação entre grupos
- Batch de mensagens WhatsApp

### Confiabilidade
- Retry automático em falhas
- Logs detalhados
- Alertas de erro
- Health checks

### Segurança
- Autenticação na interface web
- Validação de inputs
- Sanitização de dados
- Rate limiting da interface

---

## 📝 Notas de Implementação

1. **Começar simples:** JSON files → SQLite → PostgreSQL
2. **Testar cada fase:** Testes automatizados em cada etapa
3. **Documentar:** Manter docs atualizadas
4. **Feedback do usuário:** Ajustar baseado no uso real

---

**Última atualização:** 14 de Maio de 2026
