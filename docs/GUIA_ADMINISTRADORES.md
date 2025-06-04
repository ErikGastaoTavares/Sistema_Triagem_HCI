# Guia de Uso para Administradores - Sistema de Triagem HCI

Este guia detalha as funcionalidades administrativas do Sistema de Triagem HCI e como utilizá-las efetivamente.

## Visão Geral

Como administrador do sistema, você tem acesso a funcionalidades exclusivas para gerenciar usuários, visualizar estatísticas e validar triagens realizadas. Este guia aborda todas essas funcionalidades em detalhes.

## Acesso ao Painel Administrativo

1. Acesse a página inicial do sistema: http://localhost:3000
2. Clique no botão "Área Administrativa" no canto superior direito
3. Faça login com suas credenciais de administrador:
   - Usuário: `admin`
   - Senha: `admin` (recomendamos alterar após o primeiro acesso)

## Dashboard Administrativo

O dashboard apresenta uma visão geral do sistema, incluindo:

- Total de triagens realizadas
- Triagens pendentes de validação
- Triagens validadas
- Gráficos de distribuição por classificação
- Atividade recente

### Navegação

O menu lateral permite acesso a todas as seções administrativas:

- **Dashboard**: Visão geral do sistema
- **Triagens**: Lista de todas as triagens realizadas
- **Usuários**: Gerenciamento de usuários do sistema
- **Configurações**: Configurações gerais do sistema
- **Sair**: Encerra a sessão administrativa

## Gerenciamento de Usuários

### Visualizar Usuários

1. No menu lateral, clique em "Usuários"
2. A tabela exibe todos os usuários cadastrados com informações básicas
3. Utilize a barra de pesquisa para filtrar usuários por nome ou função

### Adicionar Novo Usuário

1. Na página de usuários, clique no botão "+ Novo Usuário"
2. Preencha o formulário com os dados do novo usuário:
   - **Nome Completo**: Nome completo do usuário
   - **Nome de Usuário**: Login único para acesso ao sistema
   - **Senha**: Senha inicial (o usuário poderá alterar posteriormente)
   - **Confirmar Senha**: Repetição da senha para confirmação
   - **Email**: Email do usuário para notificações
   - **Função**: Nível de acesso do usuário (Administrador, Médico, Enfermeiro, Recepcionista)
3. Clique em "Cadastrar Usuário" para finalizar

### Editar Usuário

1. Na lista de usuários, clique no botão "Editar" ao lado do usuário desejado
2. Atualize os campos necessários
3. Para alterar a senha, preencha os campos de senha (caso contrário, deixe em branco)
4. Clique em "Salvar Alterações" para confirmar

### Excluir Usuário

1. Na lista de usuários, clique no botão "Excluir" ao lado do usuário desejado
2. Confirme a exclusão na caixa de diálogo
3. **Atenção**: Esta ação não pode ser desfeita

## Validação de Triagens

### Visualizar Triagens Pendentes

1. No menu lateral, clique em "Triagens"
2. Por padrão, a visualização mostra todas as triagens
3. Utilize o filtro "Pendentes" para ver apenas triagens não validadas

### Validar uma Triagem

1. Na lista de triagens, clique no botão "Visualizar" ao lado da triagem desejada
2. Revise os detalhes da triagem:
   - Sintomas relatados
   - Classificação sugerida pelo sistema
   - Justificativa e condutas recomendadas
3. Escolha uma das opções:
   - **Validar**: Confirma que a triagem está correta
   - **Ajustar**: Permite modificar a classificação, justificativa ou condutas
   - **Rejeitar**: Marca a triagem como incorreta

4. Adicione um comentário explicando sua decisão
5. Clique em "Salvar Validação"

### Estatísticas de Validação

1. No dashboard, a seção "Precisão do Sistema" mostra estatísticas sobre as validações
2. O gráfico indica a porcentagem de triagens validadas sem ajustes
3. A tabela de distribuição mostra a precisão por categoria de classificação

## Configurações do Sistema

### Configurações Gerais

1. No menu lateral, clique em "Configurações"
2. Na aba "Geral", você pode ajustar:
   - Nome da instituição
   - Logo (upload de nova imagem)
   - Informações de contato
   - Mensagem de boas-vindas

### Configurações de Triagem

1. Na aba "Triagem", você pode ajustar:
   - Tempo máximo para validação de triagens
   - Notificações automáticas
   - Parâmetros do modelo de IA (temperatura, top_p)

### Backup e Restauração

1. Na aba "Backup", você pode:
   - Gerar backup completo do sistema
   - Restaurar a partir de backup anterior
   - Configurar backups automáticos

## Boas Práticas

1. **Segurança**:
   - Altere a senha padrão do administrador
   - Crie contas individuais para cada usuário
   - Revise periodicamente a lista de usuários ativos

2. **Validação de Triagens**:
   - Valide triagens regularmente para melhorar a precisão do sistema
   - Forneça feedback detalhado ao ajustar classificações
   - Monitore as estatísticas de precisão para identificar padrões de erro

3. **Manutenção**:
   - Realize backups semanais do sistema
   - Verifique regularmente o espaço em disco
   - Monitore os logs do sistema para identificar problemas

## Solução de Problemas Comuns

### Usuário não consegue fazer login

1. Verifique se o usuário está digitando as credenciais corretamente
2. Confirme se a conta está ativa na lista de usuários
3. Redefina a senha do usuário se necessário

### Triagem não está sendo processada

1. Verifique se o serviço Ollama está em execução
2. Consulte os logs do backend para identificar erros
3. Reinicie o serviço backend se necessário

### Lentidão no sistema

1. Verifique a utilização de recursos do servidor
2. Considere limpar o banco de dados de triagens antigas
3. Verifique se há muitas requisições simultâneas
