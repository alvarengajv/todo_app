# To-Do App

Este é um aplicativo de tarefas (To-Do App) construído usando **Flask (Python)**. O aplicativo permite que os usuários criem listas de tarefas, adicionem, editem, concluam e excluam tarefas facilmente.

## Funcionalidades

- Criar várias listas e várias tarefas dentro dessas listas.
- Adicionar, editar e excluir listas e tarefas.
- Marcar tarefas como concluídas.

## Tecnologias Usadas

- **Python** (Flask)
- **HTML/CSS** para as interfaces.
- **SQLite** como banco de dados.
- **Jinja2** para renderização de templates.
- **jQuery** para manipulação de DOM e requisições AJAX.


---

## Estrutura do Projeto

```plaintext
TODO_APP/
│
├── database/              # Banco de dados SQLite
│   └── todo_app.db        # Arquivo de banco de dados SQLite
├── static/                # Arquivos estáticos (CSS)
│   └── css/
│       ├── add_lista.css  # Arquivo CSS para estilizar a adição e edição de listas
│       ├── add_tarefa.css # Arquivo CSS para estilizar a adição e edição de tarefas
│       ├── home.css       # Arquivo CSS para estilizar a home
│       ├── index.css      # Arquivo CSS para estilizar a index
│       └── lista.css      # Arquivo CSS para estilizar a página que exibe as tarefas de uma lista
├── templates/             # Arquivos HTML renderizados com Jinja2
│   ├── add_lista.html     # Formulário para adicionar uma nova lista
│   ├── add_tarefa.html    # Formulário para adicionar uma nova tarefa
│   ├── edit_lista.html    # Formulário para editar uma lista
│   ├── edit_tarefa.html   # Formulário para editar uma tarefa
│   ├── home.html          # Página home que exibe as listas
│   ├── index.html         # Página inicial
│   ├── lista.html         # Página para exibir tarefas de uma lista
├── api_routes.py          # Rotas da API (RESTful)
├── app.py                 # Arquivo principal que inicia a aplicação Flask
├── config.py              # Arquivo de configuração da aplicação
├── database.py            # Conexão com o banco de dados SQLite
├── forms.py               # Formulários
├── models.py              # Definição dos modelos/tabelas do banco de dados
├── requirements.txt       # Arquivo de dependências Python
├── runtime.txt            # Versão do Python (se configurado)
├── web_routes.py          # Rotas principais da aplicação (web)
```

---

## Como Rodar o Projeto Localmente

### 1. Pré-requisitos

Certifique-se de ter o Python instalado na sua máquina. Este projeto foi desenvolvido usando Python 3.9.9, conforme especificado no arquivo `runtime.txt`.

### 2. Clonar o Repositório

Primeiro, clone o repositório GitHub localmente:

```bash
git clone https://github.com/alvarengajv/todo_app.git
cd todo_app
```

### 3. Criar e Ativar um Ambiente Virtual

Crie e ative um ambiente virtual Python para isolar as dependências:

```bash
# No Windows
python -m venv venv
venv\Scripts\activate

# No macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Instalar Dependências

Instale todas as dependências listadas no arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 5. Inicializar o Banco de Dados

Se o banco de dados ainda não estiver criado, você pode iniciá-lo rodando o seguinte comando Python:

```bash
python
>>> from database import init_db
>>> init_db()
>>> exit()
```

Isso criará o banco de dados SQLite (`todo_app.db`) no diretório `database/`.

### 6. Rodar o Servidor

Inicie o servidor Flask localmente:

```bash
# No Windows
set FLASK_APP=app.py
flask run

# No macOS/Linux
export FLASK_APP=app.py
flask run
```

O aplicativo estará disponível em `http://127.0.0.1:5000/`.

---

## Backend

### Rotas API

#### Rotas para Listas

- **GET /listas**: Retorna todas as listas no formato JSON.
- **POST /listas**: Cria uma nova lista com base nos dados fornecidos (necessário informar o título).
- **PUT /listas/<int:id>**: Atualiza o título de uma lista com base no Id.
- **DELETE /listas/<int:id>**: Exclui uma lista com base no Id.

#### Rotas para Tarefas

- **GET /listas/<int:id_lista>/tarefas**: Retorna todas as tarefas associadas a uma lista.
- **POST /listas/<int:id_lista>/tarefas**: Adiciona uma nova tarefa a uma lista.
- **PUT /listas/<int:id_lista>/tarefas/<int:id_tarefa>**: Edita uma tarefa.
- **PUT /listas/<int:id_lista>/tarefas/<int:id_tarefa>/concluir**: Marca uma tarefa como concluída (ou não).
- **DELETE /listas/<int:id_lista>/tarefas/<int:id_tarefa>**: Exclui uma tarefa.

---
## Frontend

### Rotas Web

#### Página Inicial
- **GET /**: Carrega a página principal que descreve o aplicativo

#### Página de Listas

- **GET /home**: Carrega a página inicial com todas as listas.
- **GET /lista/<int:id>**: Exibe as tarefas associadas a uma lista.
- **POST /lista/add**: Adiciona uma nova lista.
- **PUT /lista/<int:id>/edit**: Edita uma lista.
- **DELETE /lista/<int:id>/delete**: Exclui uma lista.

#### Página de Tarefas

- **POST /lista/<int:lista_id>/tarefa/add**: Adiciona uma nova tarefa à lista.
- **PUT /lista/<int:lista_id>/tarefa/<int:tarefa_id>/edit**: Edita uma tarefa.
- **DELETE /lista/<int:lista_id>/tarefa/<int:tarefa_id>/delete**: Exclui uma tarefa.

