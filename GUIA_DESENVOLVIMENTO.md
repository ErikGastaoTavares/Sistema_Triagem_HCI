# Guia de Desenvolvimento - Sistema de Triagem HCI

Este documento fornece informações detalhadas para desenvolvedores que desejam contribuir ou estender o Sistema de Triagem HCI.

## Arquitetura do Sistema

O Sistema de Triagem HCI segue uma arquitetura cliente-servidor com as seguintes camadas:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Frontend  │────▶│   Backend   │────▶│    Ollama   │
│  (Next.js)  │◀────│  (FastAPI)  │◀────│   (Mistral) │
└─────────────┘     └─────────────┘     └─────────────┘
                          │
                          ▼
                    ┌─────────────┐
                    │  ChromaDB   │
                    │(Embeddings) │
                    └─────────────┘
```

### Componentes Principais

1. **Frontend (Next.js)**
   - Interface de usuário responsiva
   - Gerenciamento de estado com React Hooks
   - Comunicação com API via Axios

2. **Backend (FastAPI)**
   - API RESTful para processamento de triagens
   - Autenticação e autorização de usuários
   - Integração com serviços de IA

3. **Serviços de IA**
   - Embedding Service: Geração de embeddings para busca semântica
   - Ollama Service: Integração com modelo de linguagem local (Mistral)
   - ChromaDB: Banco de dados vetorial para armazenamento de casos similares

## Estrutura de Código

### Backend

```
backend/
├── main.py                # Ponto de entrada da aplicação
├── embedding_service.py   # Serviço de embeddings
├── ollama_service.py      # Serviço de integração com Ollama
├── auth.py                # Autenticação e autorização
├── database.py            # Configuração do banco de dados
├── models.py              # Modelos de dados
├── rotas_usuarios.py      # Rotas para gerenciamento de usuários
└── requirements.txt       # Dependências do projeto
```

#### Fluxo de Processamento de Triagem

1. O cliente envia uma requisição com os sintomas do paciente
2. O backend gera embeddings para os sintomas
3. O ChromaDB busca casos similares baseados nos embeddings
4. O Ollama Service formata um prompt com os sintomas e casos similares
5. O modelo Mistral gera uma resposta com classificação, análise e condutas
6. A resposta é processada e retornada ao cliente
7. A triagem é salva no banco de dados para validação posterior

### Frontend

```
frontend/
├── components/            # Componentes reutilizáveis
├── pages/                 # Páginas da aplicação
│   ├── index.js           # Página principal (triagem)
│   ├── admin/             # Área administrativa
│   └── _app.js            # Configuração global
├── public/                # Arquivos estáticos
└── styles/                # Estilos CSS
```

## Guia de Desenvolvimento

### Configuração do Ambiente de Desenvolvimento

1. **Requisitos**
   - Node.js (v16+)
   - Python (v3.9+)
   - Ollama com modelo Mistral
   - Git (opcional)

2. **Configuração do Backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configuração do Frontend**
   ```bash
   cd frontend
   npm install
   ```

### Executando em Modo de Desenvolvimento

1. **Backend**
   ```bash
   cd backend
   python main.py
   # Ou
   uvicorn main:app --reload
   ```

2. **Frontend**
   ```bash
   cd frontend
   npm run dev
   ```

### Padrões de Código

#### Backend (Python)

- Siga a PEP 8 para estilo de código
- Use tipagem estática quando possível
- Documente funções e classes com docstrings
- Utilize logging para registrar eventos importantes
- Trate exceções adequadamente

#### Frontend (JavaScript/React)

- Use componentes funcionais com hooks
- Mantenha componentes pequenos e focados
- Utilize prop-types para validação de propriedades
- Siga o padrão de design atômico para componentes
- Evite manipulação direta do DOM

### Adicionando Novas Funcionalidades

#### Novos Endpoints na API

1. Defina o modelo de dados em `models.py`
2. Implemente a lógica de negócio
3. Adicione o endpoint em `main.py` ou em um router específico
4. Documente o endpoint com comentários OpenAPI
5. Atualize os testes

#### Novos Componentes Frontend

1. Crie o componente em `components/`
2. Implemente a lógica de renderização e interação
3. Adicione estilos em `styles/`
4. Integre o componente nas páginas relevantes

### Integração com Modelos de IA

O sistema utiliza o Ollama com o modelo Mistral para processamento de linguagem natural. Para integrar outros modelos:

1. Crie um novo serviço similar ao `ollama_service.py`
2. Implemente os métodos de geração e processamento de respostas
3. Atualize a configuração para utilizar o novo serviço

### Banco de Dados

O sistema utiliza SQLite para armazenamento de dados relacionais e ChromaDB para armazenamento de embeddings. Para modificar o esquema:

1. Atualize as funções de inicialização em `main.py` ou `database.py`
2. Implemente migrações se necessário
3. Atualize os modelos de dados em `models.py`

## Testes

### Testes de Backend

Execute os testes com pytest:

```bash
cd backend
pytest
```

### Testes de Frontend

Execute os testes com Jest:

```bash
cd frontend
npm test
```

### Testes de Integração

Os scripts de teste de integração estão disponíveis em `docs/`:

```bash
cd docs
python api_tests.py
python frontend_tests.py
```

## Deployment

### Backend

1. Construa uma imagem Docker ou prepare o ambiente de produção
2. Configure variáveis de ambiente para produção
3. Execute o servidor com Gunicorn ou Uvicorn

### Frontend

1. Construa a versão de produção:
   ```bash
   npm run build
   ```
2. Sirva os arquivos estáticos com Nginx ou similar

## Recursos Adicionais

- [Documentação do FastAPI](https://fastapi.tiangolo.com/)
- [Documentação do Next.js](https://nextjs.org/docs)
- [Documentação do Ollama](https://ollama.ai/docs)
- [Documentação do ChromaDB](https://docs.trychroma.com/)