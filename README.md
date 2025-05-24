## Requisitos do Projeto

### Estrutura da API
- [x] Desenvolver uma API REST utilizando Django e Django REST Framework.
- [x] Criar endpoints para CRUD de notícias, com os seguintes atributos:
  - [x] Título
  - [x] Subtítulo
  - [x] Imagem (upload)
  - [x] Conteúdo
  - [x] Data de publicação
  - [x] Autor
  - [x] Status (rascunho ou publicado)
- [x] Definir status das notícias:
  - [x] Rascunho: Notícia salva por um editor, mas ainda não publicada.
  - [x] Publicada: Notícia disponível para leitura.
- [x] Funcionalidades adicionais:
  - [x] Permitir o agendamento de publicações.
  - [x] Categorizar notícias dentro das verticais: Poder, Tributos, Saúde, Energia e Trabalhista.
  - [x] Definir se uma notícia será acessível a todos os leitores ou restrita a clientes PRO.
  - [x] Definir a relação do cliente com o plano e a vertical.
- [x] Documentar a API utilizando Swagger.

### Autenticação e Perfis de Usuário
- [x] Implementar autenticação baseada em JWT para controle de acesso.
- [x] Criar endpoints para:
  - [x] Geração e renovação de tokens JWT.
  - [x] Gerenciamento de usuários conforme perfis:
    - [ ] Admin: Acesso total (criação, edição, exclusão e gerenciamento de usuários).
    - [ ] Editor: Pode criar, editar e excluir apenas suas próprias notícias.
    - [ ] Leitor: Pode visualizar apenas notícias publicadas, conforme o plano contratado.
- [x] Definir acesso de leitores conforme o plano contratado:
  - [x] JOTA Info: Acesso a notícias abertas para todos os usuários.
  - [x] JOTA PRO: Acesso a conteúdos exclusivos de acordo com as verticais do plano.
- [x] As verticais disponíveis são:
  - [x] Poder
  - [x] Tributos
  - [x] Saúde
  - [x] Energia
  - [x] Trabalhista
- [x] Garantir que um plano pode incluir acesso a uma ou mais verticais.

### Banco de Dados
- [x] Utilizar PostgreSQL ou MySQL.
- [x] Conhecimento básico em bancos NoSQL (diferencial).

### Arquitetura e Processamento Assíncrono
- [ ] Implementar fila de processamento para tarefas demoradas (ex.: envio de e-mails de notificação).
- [ ] Utilizar arquitetura orientada a eventos para escalabilidade e desacoplamento dos serviços.
- [x] Conhecimento em microsserviços (diferencial).

### Testes Automatizados e CI/CD
- [x] Implementar testes unitários e de integração (pytest ou unittest).
- [ ] Configurar pipeline CI/CD com GitHub Actions para testes automáticos e deploy.
- [x] Experiência com metodologias ágeis e integração/entrega contínua (diferencial).

### Infraestrutura e Deploy
- [x] Criar um `Dockerfile` para empacotar a aplicação.
- [x] Criar um `docker-compose.yml` para facilitar a execução local.

## Como executar o projeto

Acesse o repositório aqui: [https://github.com/wendrewdevelop/JOTA](https://github.com/wendrewdevelop/JOTA)

---

### **1. Clonar o repositório**

```bash
git clone https://github.com/wendrewdevelop/JOTA.git
cd JOTA
```

---

### **2. Criar e ativar ambiente virtual**

```bash
python3 -m venv .venv
source .venv/bin/activate

# Se estiver usando yv, não tem necessidade de criar um ambiente virtual manualmente.
```

---

### **3. Instalar as dependências**

```bash
pip install -r requirements.txt

# ou, se estiver usando uv:
uv sync && uv lock
```

---

### **4. Configurar o banco de dados**

Depois, rode:

```bash
python manage.py migrate

# Se estiver usando uv:

uv run ./manage.py migrate
```

---

### **5. Criar superusuário**

```bash
python manage.py createsuperuser

# Se estiver usando uv:

uv run ./manage.py createsuperuser
```

---

### **6. Rodar o servidor Django**

```bash
python manage.py runserver

# Se estiver usando uv:

uv run ./manage.py runserver
```

---

### **7. Rodar Celery Worker**

Em um terminal separado, ative o venv e execute:

```bash
celery -A jota worker --loglevel=info

# Se estiver usando uv:

uv run ./manage.py celery -A jota worker --loglevel=info
```

---

### **8. Rodar Celery Beat**

Em outro terminal separado:

```bash
celery -A jota beat --loglevel=info

# Se estiver usando uv:

uv run ./manage.py celery -A jota beat --loglevel=info
```

---

### **9. Acessar o painel de administração**

Abra no navegador:

```
# URLS da API

# Admin:
http://127.0.0.1:8000/admin/

# API
http://127.0.0.1:8000/api/v1/ -- Browsable API

# Autenticação
http://127.0.0.1/auth/jwt/login/

# Swagger
http://127.0.0.1:8000/api/schema/swagger/

# Redoc
http://127.0.0.1:8000/api/schema/redoc/
```

---

## **10. Testar a execução automática da task**

1. Crie um `News` com status `draft` e `scheduled_post` para uma data próxima.
2. Aguarde a execução automática via `celery beat + worker`.
3. Veja se o status muda para `published`.

## **11. Executar os testes (pytest)**

Execute no terminal (raiz do projeto)

```
pytest

# Se estiver usando uv:

uv run pytest
```

## **12. Autenticação via JWT**

Acesse a URL: [http://127.0.0.1/auth/jwt/login/](http://127.0.0.1/auth/jwt/login/)

```
# Preencha com os valores abaixos os respectivos campos:

Media type: application/json

Content: {
    "email": "<email>",
    "password": "<senha>"
}
```

## **13. Docker**

No terminal

```
# BUILD e UP
docker-compose up --build

# Rodar as migrações dentro do container
docker-compose exec web python manage.py migrate

# Criar um superusuário:
docker-compose exec web python manage.py createsuperuser

```
- API rodando em: http://localhost:8000
- PostgreSQL rodando na porta: 5432

