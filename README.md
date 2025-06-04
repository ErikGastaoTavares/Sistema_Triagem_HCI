# Sistema de Triagem HCI

<div align="center">
  <img src="https://hci.org.br/wp-content/uploads/2024/09/logo-300x67.png" alt="Logo HCI" width="300"/>
  <h3>Sistema Inteligente de Triagem Clínica</h3>
  <p>Baseado no Protocolo de Manchester com Inteligência Artificial</p>
</div>

## 📋 Sobre o Projeto

O Sistema de Triagem HCI é uma aplicação completa para triagem clínica hospitalar, desenvolvida especificamente para o Hospital de Clínicas de Ijuí (HCI). O sistema utiliza inteligência artificial através do modelo Mistral via Ollama para classificar pacientes de acordo com o Protocolo de Manchester, priorizando o atendimento conforme a gravidade dos casos.

### Principais Funcionalidades

- **Triagem Inteligente**: Classificação automática de pacientes baseada em sintomas
- **Validação Clínica**: Interface para validação das triagens por profissionais de saúde
- **Gestão de Usuários**: Sistema completo de cadastro e gerenciamento de usuários
- **Dashboard Administrativo**: Visualização de estatísticas e métricas de desempenho
- **Aprendizado Contínuo**: Melhoria progressiva da precisão através de feedback

## 🚀 Tecnologias

### Frontend
- **Next.js**: Framework React para renderização de páginas
- **CSS Moderno**: Design responsivo e adaptável a qualquer dispositivo
- **Componentes Reutilizáveis**: Arquitetura modular e escalável

### Backend
- **FastAPI**: Framework Python de alta performance
- **SQLite**: Banco de dados relacional para armazenamento de dados
- **ChromaDB**: Banco de dados vetorial para busca semântica
- **Ollama/Mistral**: Modelo de linguagem para processamento de triagem

## 🔧 Instalação

### Pré-requisitos
- Node.js 16.x ou superior
- Python 3.9 ou superior
- Ollama instalado com o modelo Mistral

### Backend

```bash
# Navegar para o diretório do backend
cd backend

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Iniciar servidor
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend

```bash
# Navegar para o diretório do frontend
cd frontend

# Instalar dependências
npm install

# Iniciar servidor de desenvolvimento
npm run dev

# Para build de produção
npm run build
npm start
```

Para instruções detalhadas, consulte o [Manual de Instalação](docs/MANUAL_INSTALACAO.md).

## 🖥️ Uso do Sistema

### Triagem de Pacientes

1. Acesse a página inicial
2. Preencha o formulário com os sintomas do paciente
3. Clique em "Realizar Triagem"
4. Visualize a classificação, justificativa e condutas recomendadas

### Área Administrativa

1. Acesse a área administrativa através do botão no canto superior direito
2. Faça login com suas credenciais
3. Navegue pelo dashboard para visualizar estatísticas
4. Gerencie usuários e valide triagens pendentes

Para instruções detalhadas, consulte o [Guia de Administradores](docs/GUIA_ADMINISTRADORES.md).

## 🔍 Estrutura do Projeto

```
projeto_melhorado/
├── backend/               # API e lógica de negócio
│   ├── main.py            # Ponto de entrada da API
│   ├── embedding_service.py # Serviço de embeddings
│   ├── ollama_service.py  # Serviço de comunicação com Ollama
│   ├── usuarios.py        # Módulo de gestão de usuários
│   └── requirements.txt   # Dependências Python
│
├── frontend/              # Interface de usuário
│   ├── components/        # Componentes reutilizáveis
│   ├── pages/             # Páginas da aplicação
│   ├── styles/            # Estilos CSS
│   └── package.json       # Dependências JavaScript
│
└── docs/                  # Documentação
    ├── MANUAL_INSTALACAO.md      # Guia de instalação
    ├── GUIA_ADMINISTRADORES.md   # Manual para administradores
    ├── NOVAS_FUNCIONALIDADES.md  # Detalhes das funcionalidades
    └── RELATORIO_TESTES.md       # Resultados dos testes
```

## 🔐 Segurança

O sistema implementa diversas medidas de segurança:

- Armazenamento seguro de senhas com hash e salt
- Proteção de rotas por nível de acesso
- Validação de dados em frontend e backend
- Proteção contra ataques comuns (SQL Injection, XSS)

## 📊 Classificação de Manchester

O sistema utiliza o Protocolo de Manchester para classificação de pacientes:

| Cor       | Prioridade     | Tempo Máximo |
|-----------|----------------|--------------|
| Vermelho  | Emergência     | Imediato     |
| Laranja   | Muito Urgente  | 10 minutos   |
| Amarelo   | Urgente        | 60 minutos   |
| Verde     | Pouco Urgente  | 120 minutos  |
| Azul      | Não Urgente    | 240 minutos  |

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Faça commit das alterações (`git commit -m 'Adiciona nova funcionalidade'`)
4. Faça push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.

## 📞 Contato

Hospital de Clínicas de Ijuí - [https://hci.org.br/](https://hci.org.br/)

---

<div align="center">
  <p>Desenvolvido com ❤️ para o Hospital de Clínicas de Ijuí</p>
</div>
