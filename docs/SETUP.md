# Guia de Configuração do Ambiente de Desenvolvimento

Este documento contém instruções detalhadas para configurar o ambiente de desenvolvimento do Sistema de Triagem HCI com as melhorias implementadas.

## Requisitos do Sistema

- Node.js (v16 ou superior)
- Python (v3.8 ou superior)
- Ollama (com modelo Mistral instalado)
- Git (opcional, para controle de versão)

## Estrutura do Projeto

```
projeto_melhorado/
├── frontend/         # Aplicação Next.js (interface do usuário)
├── backend/          # API FastAPI (servidor)
└── docs/             # Documentação
```

## Configuração do Backend

1. **Criar ambiente virtual Python**:

```bash
cd backend
python -m venv venv

# Ativar o ambiente virtual
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate
```

2. **Instalar dependências**:

```bash
pip install -r requirements.txt
```

3. **Configurar banco de dados**:

O sistema utiliza SQLite por padrão, que não requer configuração adicional.

4. **Iniciar o servidor de desenvolvimento**:

```bash
python main.py
```

O servidor estará disponível em `http://localhost:8000`.

## Configuração do Frontend

1. **Instalar dependências**:

```bash
cd frontend
npm install
```

2. **Iniciar o servidor de desenvolvimento**:

```bash
npm run dev
```

O frontend estará disponível em `http://localhost:3000`.

## Configuração do Ollama

1. **Instalar Ollama**:

Siga as instruções em [ollama.ai](https://ollama.ai) para instalar o Ollama em seu sistema operacional.

2. **Baixar o modelo Mistral**:

```bash
ollama pull mistral
```

3. **Verificar a instalação**:

```bash
ollama list
```

Certifique-se de que o modelo "mistral" aparece na lista.

## Testando a Integração

1. Certifique-se de que o Ollama está em execução
2. Inicie o backend (servidor FastAPI)
3. Inicie o frontend (aplicação Next.js)
4. Acesse `http://localhost:3000` no navegador
5. Teste o sistema de triagem com alguns exemplos de sintomas

## Solução de Problemas

### Erro de conexão com Ollama

Se o sistema exibir um erro indicando que o Ollama não está disponível, verifique:

1. Se o serviço Ollama está em execução
2. Se o modelo Mistral foi baixado corretamente
3. Se o backend está configurado para acessar o Ollama na porta correta (padrão: 11434)

### Erro no frontend

Se o frontend não carregar corretamente:

1. Verifique se todas as dependências foram instaladas
2. Certifique-se de que o backend está em execução
3. Verifique os logs do console do navegador para identificar erros específicos

## Desenvolvimento

Para implementar novas funcionalidades ou fazer modificações:

- **Frontend**: Edite os arquivos em `frontend/pages` e `frontend/components`
- **Backend**: Modifique os endpoints em `backend/main.py`
- **Estilos**: Atualize o CSS em `frontend/styles/globals.css`

Após cada modificação, reinicie os servidores de desenvolvimento para aplicar as alterações.
