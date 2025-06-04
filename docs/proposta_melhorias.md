# Proposta de Melhorias para o Sistema de Triagem HCI

## Resumo Executivo

Após análise detalhada do código-fonte do sistema de triagem atual, propomos um conjunto de melhorias que atendem aos requisitos solicitados:

1. **Atualização da Interface Gráfica**: Redesenho completo seguindo a identidade visual do Hospital HCI
2. **Cadastro de Usuários**: Nova página para gerenciamento de usuários do sistema
3. **Melhorias na Triagem com IA**: Otimização da integração com Ollama/Mistral para maior precisão
4. **Otimização de Desempenho**: Refinamentos técnicos para melhor experiência do usuário

## 1. Atualização da Interface Gráfica

### Análise da Identidade Visual do HCI

Após análise do site institucional (https://hci.org.br/), identificamos os seguintes elementos-chave:

- **Paleta de Cores**: 
  - Azul principal: #003B71 (já presente no CSS atual)
  - Azul claro: #0072C6 (já presente no CSS atual)
  - Verde: #009B3A (já presente no CSS atual)
  - Turquesa: #41B9B3 (novo elemento a ser adicionado)
  - Laranja: #F26522 (novo elemento a ser adicionado para destaque)

- **Tipografia**: 
  - Fonte Montserrat (já implementada no sistema atual)
  - Pesos variados para hierarquia visual

- **Elementos Visuais**:
  - Gradientes suaves nos cards e botões
  - Cantos arredondados nos elementos interativos
  - Sombras sutis para profundidade

### Melhorias Propostas para Interface

1. **Header Redesenhado**:
   - Barra superior com gradiente azul-turquesa
   - Logo HCI em destaque com tamanho adequado
   - Menu de navegação mais intuitivo

2. **Página Principal**:
   - Cards com gradientes e ícones para diferentes seções
   - Formulário de triagem com visual mais profissional
   - Feedback visual aprimorado durante o processo de triagem

3. **Responsividade**:
   - Melhorias no layout para dispositivos móveis
   - Ajustes de tamanho de fonte e espaçamento
   - Adaptação de menus para telas pequenas

## 2. Página de Cadastro de Usuários

### Funcionalidades Propostas

1. **Formulário de Cadastro**:
   - Campos para nome, usuário, senha, email e função
   - Validação em tempo real dos dados inseridos
   - Feedback visual sobre requisitos de senha

2. **Gerenciamento de Usuários**:
   - Lista de usuários cadastrados (apenas para administradores)
   - Opções para editar, desativar ou excluir usuários
   - Filtros e busca para facilitar a gestão

3. **Níveis de Acesso**:
   - Administrador: acesso completo ao sistema
   - Médico: validação de triagens e acesso a estatísticas
   - Enfermeiro: validação de triagens básicas
   - Recepcionista: apenas registro de pacientes

### Integração com Sistema Existente

- Adição de endpoint `/api/usuarios` no backend
- Implementação de autenticação mais robusta
- Armazenamento seguro de senhas com hash e salt

## 3. Melhorias na Triagem com IA (Ollama/Mistral)

### Otimização da Precisão

1. **Refinamento do Prompt**:
   - Estruturação mais clara das instruções para o modelo
   - Inclusão de exemplos específicos para cada classificação
   - Diretrizes mais detalhadas para justificativas e condutas

2. **Processamento de Resposta**:
   - Algoritmo aprimorado para extração de classificação
   - Tratamento mais robusto de casos ambíguos
   - Validação adicional das respostas geradas

3. **Feedback Loop**:
   - Incorporação de feedback dos profissionais nas futuras triagens
   - Armazenamento de casos validados para referência
   - Atualização periódica da base de conhecimento

### Otimização de Desempenho

1. **Gerenciamento de Conexão**:
   - Tratamento mais robusto de falhas na comunicação com Ollama
   - Sistema de retry com backoff exponencial
   - Feedback em tempo real sobre o status do processamento

2. **Caching Inteligente**:
   - Armazenamento temporário de embeddings frequentes
   - Reutilização de cálculos para consultas similares
   - Limpeza periódica do cache para otimizar memória

## 4. Implementação Técnica

### Frontend (Next.js)

1. **Novos Componentes**:
   - `UserForm.js`: Formulário de cadastro de usuários
   - `UserList.js`: Lista de usuários com opções de gerenciamento
   - `Header.js`: Componente de cabeçalho redesenhado
   - `Footer.js`: Rodapé padronizado com informações do HCI

2. **Estilos Atualizados**:
   - Adição de novas variáveis CSS para cores do HCI
   - Implementação de gradientes e efeitos visuais
   - Classes responsivas aprimoradas

3. **Novas Páginas**:
   - `/admin/users`: Gerenciamento de usuários
   - `/admin/users/new`: Cadastro de novo usuário
   - `/admin/users/[id]/edit`: Edição de usuário existente

### Backend (FastAPI)

1. **Novos Endpoints**:
   - `POST /api/usuarios`: Criar novo usuário
   - `GET /api/usuarios`: Listar usuários
   - `PUT /api/usuarios/{id}`: Atualizar usuário
   - `DELETE /api/usuarios/{id}`: Remover usuário

2. **Melhorias em Endpoints Existentes**:
   - Otimização do `/api/triagem` para melhor tratamento de erros
   - Refinamento do processamento de respostas do Ollama
   - Adição de logs detalhados para monitoramento

3. **Segurança**:
   - Implementação de JWT para autenticação
   - Proteção contra ataques comuns (CSRF, XSS)
   - Validação robusta de inputs

## 5. Cronograma de Implementação

1. **Fase 1: Preparação** (1-2 dias)
   - Configuração do ambiente de desenvolvimento
   - Backup do sistema atual
   - Definição de branches Git para cada feature

2. **Fase 2: Desenvolvimento Frontend** (3-5 dias)
   - Implementação da nova identidade visual
   - Criação das páginas de cadastro de usuários
   - Testes de responsividade

3. **Fase 3: Desenvolvimento Backend** (3-5 dias)
   - Implementação dos novos endpoints
   - Otimização da integração com Ollama/Mistral
   - Testes de segurança e performance

4. **Fase 4: Integração e Testes** (2-3 dias)
   - Testes de integração entre frontend e backend
   - Validação de fluxos completos
   - Correção de bugs identificados

5. **Fase 5: Implantação** (1 dia)
   - Migração de dados necessários
   - Implantação em ambiente de produção
   - Monitoramento inicial

## 6. Conclusão

As melhorias propostas trarão benefícios significativos ao Sistema de Triagem do HCI:

- **Experiência do Usuário**: Interface mais intuitiva e alinhada à identidade do hospital
- **Segurança**: Gerenciamento adequado de usuários e permissões
- **Precisão**: Triagens mais acuradas com a otimização da IA
- **Desempenho**: Sistema mais rápido e confiável

Estamos à disposição para discutir detalhes adicionais e ajustar a proposta conforme necessário.
