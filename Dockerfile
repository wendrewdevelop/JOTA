# Escolha uma imagem base
FROM python:3.11-slim

# Define diretório de trabalho
WORKDIR /code

# Instala dependências de sistema (opcional, se precisar)
RUN apt-get update && apt-get install -y \
    netcat \
    && rm -rf /var/lib/apt/lists/*

# Copia dependências
COPY requirements.txt .

# Instala dependências Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copia código do projeto
COPY . .

# Comando padrão
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
