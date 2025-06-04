# Plano de Testes - Sistema de Triagem HCI

## 1. Testes de Funcionalidade

### 1.1 Frontend - Página Principal
- [ ] Verificar carregamento correto da página inicial
- [ ] Testar formulário de triagem com diferentes sintomas
- [ ] Validar exibição correta dos resultados de classificação
- [ ] Verificar navegação para área administrativa

### 1.2 Frontend - Autenticação
- [ ] Testar login com credenciais válidas (admin, médico, enfermeiro)
- [ ] Testar login com credenciais inválidas
- [ ] Verificar redirecionamento após login bem-sucedido
- [ ] Testar logout

### 1.3 Frontend - Cadastro de Usuários
- [ ] Verificar acesso à página de cadastro apenas para administradores
- [ ] Testar cadastro de novo usuário com dados válidos
- [ ] Testar validações de formulário (campos obrigatórios, formato de email, senhas)
- [ ] Verificar listagem de usuários cadastrados
- [ ] Testar edição de usuário existente
- [ ] Testar exclusão de usuário

### 1.4 Backend - API de Triagem
- [ ] Testar endpoint `/api/triagem` com sintomas válidos
- [ ] Verificar processamento correto da classificação
- [ ] Testar tratamento de erros (sintomas vazios, serviço Ollama indisponível)
- [ ] Verificar armazenamento da triagem no banco de dados

### 1.5 Backend - API de Usuários
- [ ] Testar criação de usuário via API
- [ ] Testar listagem de usuários
- [ ] Testar atualização de usuário
- [ ] Testar exclusão de usuário
- [ ] Verificar validações e tratamento de erros

### 1.6 Integração com Ollama/Mistral
- [ ] Testar comunicação com o serviço Ollama
- [ ] Verificar processamento de respostas
- [ ] Testar mecanismo de retry em caso de falhas
- [ ] Verificar funcionamento do cache de respostas

## 2. Testes de Responsividade

### 2.1 Dispositivos Desktop
- [ ] Testar em resolução 1920x1080 (Full HD)
- [ ] Testar em resolução 1366x768 (Laptop comum)
- [ ] Testar em resolução 2560x1440 (QHD)

### 2.2 Dispositivos Móveis
- [ ] Testar em resolução 375x667 (iPhone 8)
- [ ] Testar em resolução 414x896 (iPhone 11 Pro Max)
- [ ] Testar em resolução 360x740 (Android médio)

### 2.3 Tablets
- [ ] Testar em resolução 768x1024 (iPad)
- [ ] Testar em resolução 1024x1366 (iPad Pro)

## 3. Testes de Compatibilidade

### 3.1 Navegadores
- [ ] Google Chrome (última versão)
- [ ] Mozilla Firefox (última versão)
- [ ] Microsoft Edge (última versão)
- [ ] Safari (última versão)

### 3.2 Sistemas Operacionais
- [ ] Windows 10/11
- [ ] macOS
- [ ] Android
- [ ] iOS

## 4. Testes de Desempenho

### 4.1 Tempo de Resposta
- [ ] Medir tempo de carregamento da página inicial
- [ ] Medir tempo de processamento da triagem
- [ ] Medir tempo de resposta das operações de usuário

### 4.2 Carga
- [ ] Testar múltiplas requisições simultâneas
- [ ] Verificar comportamento sob carga moderada

## 5. Testes de Segurança

### 5.1 Autenticação
- [ ] Verificar proteção de rotas administrativas
- [ ] Testar expiração de sessão
- [ ] Verificar armazenamento seguro de senhas

### 5.2 Validação de Entrada
- [ ] Testar injeção de SQL
- [ ] Testar XSS (Cross-Site Scripting)
- [ ] Verificar validação de todos os campos de formulário

## Resultados e Correções

| ID | Descrição do Teste | Resultado | Correção Necessária |
|----|-------------------|-----------|---------------------|
|    |                   |           |                     |
