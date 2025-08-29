# Use imagem python oficial
FROM python:3.13-slim

# Variáveis de ambiente para melhorar logs e performance
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependências do sistema necessárias para psycopg2 e outras libs
RUN apt-get update && apt-get install -y gcc libpq-dev

# Copiar requirements e instalar pacotes python
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copiar código fonte
COPY . /app/

# Expõe a porta que Django vai rodar
EXPOSE 8002

# Comando para rodar o servidor
CMD ["python", "manage.py", "runserver", "0.0.0.0:8002"]
