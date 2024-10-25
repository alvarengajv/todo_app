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
- **SQLAlchemy** como ORM (Object-Relational Mapper) para abstrair as interações com o banco de dados
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

## Banco de dados

O projeto utiliza **SQLite** como banco de dados e **SQLAlchemy** como ORM (Object-Relational Mapper) para abstrair as interações com o banco de dados. A escolha do SQLite é ideal para desenvolvimento local e aplicações simples, pois é um banco de dados leve que armazena os dados em um único arquivo (`todo_app.db`) no diretório `database/`. 

O **SQLAlchemy** permite que a interação com o banco de dados seja feita de forma mais intuitiva, usando classes Python para representar as tabelas e abstraindo a necessidade de escrever SQL diretamente.

### Modelos

Foram definidos dois modelos principais: `Lista` e `Tarefa`. Esses modelos representam, respectivamente, uma lista de tarefas e uma tarefa específica dentro de uma lista.

#### **Lista**

O modelo `Lista` representa uma lista de tarefas e contém um título para identificá-la.

##### Campos

- **id**: Identificador único da lista (chave primária).
- **titulo**: Nome da lista.
- **tarefas**: Relacionamento um-para-muitos com o modelo `Tarefa`, permitindo que uma lista tenha várias tarefas. O parâmetro `cascade="all, delete-orphan"` garante que ao excluir uma lista, todas as tarefas associadas a ela também sejam removidas.

#### **Tarefa**

O modelo `Tarefa` representa uma tarefa específica dentro de uma lista. Contém informações como título, descrição, data e hora de execução, status de conclusão e a associação com uma lista.

##### Campos

- **id**: Identificador único da tarefa (chave primária).
- **titulo**: Nome ou título da tarefa.
- **data**: Data de conclusão da tarefa.
- **hora**: Horário de conclusão da tarefa.
- **descricao**: Detalhes adicionais sobre a tarefa.
- **concluida**: Indicador booleano que define se a tarefa foi concluída.
- **lista_id**: Chave estrangeira que associa a tarefa a uma lista específica, utilizando o `id` da tabela `listas`.

### Relacionamento entre `Lista` e `Tarefa`

- Uma `Lista` possui várias `Tarefas`, enquanto cada `Tarefa` pertence a uma única `Lista`.
- Esse relacionamento um-para-muitos é configurado no SQLAlchemy através do `db.relationship` no modelo `Lista` e da `db.ForeignKey` no modelo `Tarefa`.

### Criação e Inicialização do Banco de Dados

O banco de dados é criado e inicializado chamando `db.create_all()` no contexto da aplicação Flask. Isso cria as tabelas `listas` e `tarefas` no banco de dados SQLite (`todo_app.db`), conforme as definições nos modelos.

---

## Backend

O **backend** é desenvolvido em **Flask**, que serve as rotas principais da aplicação e processa as requisições de dados. A aplicação está dividida em rotas **web** e **API RESTful** para facilitar a organização e permitir que o frontend e o backend funcionem de maneira independente.

#### Rotas API 

As rotas de API focadas em manipulações de dados e fornecimento de respostas JSON para as operações de criação, leitura, atualização e exclusão (CRUD) além de, fornecerem uma interface JSON para o frontend e permiterem uma interação dinâmica.

#### **Listas**

- **GET /listas**: Retorna todas as listas no formato JSON.
- **POST /listas**: Cria uma nova lista com base nos dados fornecidos (necessário informar o título).
- **PUT /listas/<int:id>**: Atualiza o título de uma lista com base no Id.
- **DELETE /listas/<int:id>**: Exclui uma lista com base no Id.

#### **Tarefas**

- **GET /listas/<int:id_lista>/tarefas**: Retorna todas as tarefas associadas a uma lista.
- **POST /listas/<int:id_lista>/tarefas**: Adiciona uma nova tarefa a uma lista.
- **PUT /listas/<int:id_lista>/tarefas/<int:id_tarefa>**: Edita uma tarefa.
- **PUT /listas/<int:id_lista>/tarefas/<int:id_tarefa>/concluir**: Marca uma tarefa como concluída.
- **DELETE /listas/<int:id_lista>/tarefas/<int:id_tarefa>**: Exclui uma tarefa.

---

## Frontend

### Uso de jQuery e AJAX

No frontend, o **jQuery** é utilizado para simplificar a manipulação do DOM (Document Object Model) e facilitar as requisições **AJAX** ao backend, que são essenciais para tornar o aplicativo mais interativo e responsivo. As requisições AJAX permitem que o conteúdo seja atualizado dinamicamente, sem a necessidade de recarregar a página, melhorando a experiência do usuário.

As funcionalidades implementadas com jQuery e AJAX no aplicativo incluem:

- **Marcar Tarefas como Concluídas**:
   - Um checkbox permite que o usuário marque uma tarefa como concluída. Essa ação aciona uma requisição AJAX `PUT` para o backend, atualizando o status de conclusão da tarefa no banco de dados.

- **Edição e Exclusão de Tarefas e Listas**:
   - Botões de ação (ícones de lápis e lixeira) permitem que o usuário edite ou exclua listas e tarefas diretamente. A exclusão de itens é feita através de uma requisição AJAX `DELETE`, enquanto a edição utiliza uma combinação de AJAX e redirecionamentos para a interface de edição.

- **Criação de Novas Tarefas e Listas**:
   - Os formulários para adicionar listas e tarefas também utilizam jQuery para validações e envio de dados via AJAX, quando aplicável.

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
