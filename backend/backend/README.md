# ✅ Checklist de Desenvolvimento - Sistema de Controle de Suprimentos

Organize o desenvolvimento de cada tela com base em funcionalidades, componentes e integrações.

---

## 1. Login
- [ ] Criar página de login responsiva
- [ ] Integrar com API de autenticação (OAuth2/JWT)
- [ ] Exibir mensagens de erro
- [ ] Redirecionar usuário autenticado para dashboard

## 2. Dashboard
- [ ] Criar layout principal com cards (KPIs)
- [ ] Integrar dados do backend (solicitações pendentes, estoque atual)
- [ ] Criar menu lateral com links funcionais
- [ ] Adicionar botão de nova solicitação

## 3. Nova Solicitação
- [ ] Criar formulário com dropdowns e validações
- [ ] Integrar com endpoint de criação de solicitação
- [ ] Exibir mensagens de sucesso/erro
- [ ] Redirecionar para "Minhas Solicitações" após envio

## 4. Minhas Solicitações
- [ ] Listar todas as solicitações do usuário logado
- [ ] Adicionar filtros por status e data
- [ ] Exibir status colorido
- [ ] Link para detalhe da solicitação

## 5. Detalhe da Solicitação
- [ ] Mostrar todas as informações (produto, justificativa, status, data)
- [ ] Exibir histórico da solicitação (log, atualizações)

## 6. Estoque
- [ ] Criar tabela de produtos com nível de estoque
- [ ] Destacar itens abaixo do mínimo
- [ ] Adicionar botão de edição rápida
- [ ] Exibir detalhes do produto selecionado

## 7. Configurações
- [ ] Criar tela de configurações gerais
- [ ] Opções para e-mails, limites de estoque e preferências
- [ ] Campos para configurar integração com ERP

## 8. Layout Geral
- [ ] Criar menu lateral com React Router
- [ ] Criar cabeçalho com nome do usuário
- [ ] Adicionar botão de logout
- [ ] Responsividade para mobile e tablets

## Integração com Backend
- [ ] Criar serviço Axios para comunicação com API
- [ ] Armazenar token JWT no localStorage
- [ ] Adicionar headers nas requisições autenticadas

## Validação e UX
- [ ] Feedback visual (loading/spinner)
- [ ] Validação de formulários e mensagens claras
- [ ] Testar fluxos completos de usuário


## USe flow

# 🧭 User Flow - Sistema de Controle de Suprimentos

Representação profissional do fluxo de navegação e experiência do usuário no sistema web.

```plaintext
[Login]
   |
   v
[Dashboard Principal]
   |
   |--> [Nova Solicitação] --> [Enviar Solicitação] --> [Volta ao Dashboard]
   |
   |--> [Minhas Solicitações]
   |       |
   |       --> [Detalhe da Solicitação]
   |
   |--> [Estoque]
   |       |
   |       --> [Editar Produto]
   |       --> [Visualizar Detalhes]
   |
   |--> [Configurações]
   |
   |--> [Sair]
```

---

## 🗺️ Descrição por Tela

### 1. Login
- Campo usuário/senha
- Autenticação via OAuth2/JWT
- Redireciona para dashboard

### 2. Dashboard Principal
- KPIs de resumo
- Acesso rápido às principais funções

### 3. Nova Solicitação
- Formulário completo com validação
- Gatilho para tarefas Celery (e-mail, integração)

### 4. Minhas Solicitações
- Listagem de solicitações feitas
- Filtros por data/status
- Acesso ao detalhe da solicitação

### 5. Detalhe da Solicitação
- Exibe justificativa, data, status, histórico

### 6. Estoque
- Tabela com produtos e níveis
- Destaque para baixo estoque
- Botão editar e visualizar

### 7. Configurações
- E-mails de notificação
- Integração com ERP
- Limites, alertas e preferências

---

## 🚀 Acesso e Fluxo
- A navegação é feita por um **menu lateral fixo**
- Usuário tem acesso imediato às ações principais
- Telas seguem layout responsivo e baseado em componentes reutilizáveis



# ✅ Requisitos Funcionais e Não Funcionais

Documentação oficial dos requisitos para o Sistema de Controle de Suprimentos.


| ID     | Descrição do Requisito                                                                 | Prioridade |
|--------|-----------------------------------------------------------------------------------------|------------|
| RF-001 | O sistema deve permitir login com usuário e senha. Login com autenticação via OAuth2 e geração de token JWT                               | ALTA       |
| RF-002 | O sistema deve gerar e validar tokens JWT para autenticação,cadastro de solicitação de compra com validações.                                     | ALTA       |
| RF-003 | O sistema deve permitir logout e bloqueio de acesso não autenticado.                              | MÉDIA      |
| RF-004 | Listagem do estoque com destaque para níveis críticos                                  | ALTA       |
| RF-005 | Edição rápida de produtos no estoque                                                   | MÉDIA      |
| RF-006 | O sistema deve controlar permissões por tipo de usuário (comprador, solicitante, gestor, etc.).Aprovação/reprovação de solicitações (usuário com permissão)                           | MÉDIA      |
| RF-007 | O usuário deve poder cadastrar uma nova solicitação de compra.
| RF-008 | Envio automático de e-mails para mudanças de status                                    | MÉDIA      |
| RF-009 | Integração com ERP via Firebird e pyodbc                                               | ALTA       |
| RF-010 | Logs de atividades do sistema e rastreio de ações por usuário                          | ALTA       |
| RF-011 | Configurações de alertas, e-mails e níveis mínimos de estoque                          | MÉDIA      |
| RF-012 | O sistema deve permitir visualizar a lista de solicitações por status (pendente, aprovado, negado).
| RF-09  | O sistema deve registrar data, hora e usuário responsável por cada ação.
---

# Requisitos Não Funcionais

| ID      | Descrição do Requisito                                                                                  | Prioridade |
|---------|----------------------------------------------------------------------------------------------------------|------------|
| RNF-001 | O sistema deve ser responsivo para diferentes tamanhos de tela                                           | MÉDIA      |
| RNF-002 | O frontend deve ser intuitivo, com navegação clara e fluida                                              | MÉDIA      |
| RNF-003 | O sistema deve utilizar autenticação baseada em OAuth2 com tokens JWT                                    | ALTA       |
| RNF-004 | O backend deve executar tarefas assíncronas com Celery + Redis                                           | ALTA       |
| RNF-005 | A estrutura deve ser containerizada com Docker e suportar CI/CD com GitHub Actions                      | ALTA       |
| RNF-006 | A API deve ser documentada automaticamente com Swagger e seguir padrão REST                             | MÉDIA      |
| RNF-007 | O sistema deve ser monitorado por métricas exportadas para o Grafana                                     | MÉDIA      |
| RNF-008 | Os dados devem ser persistidos de forma segura no PostgreSQL com criptografia de informações sensíveis   | ALTA       |


