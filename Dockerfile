# 1. Imagem Base: Usa uma versão leve do Python
FROM python:3.9-slim

# 2. Diretório de Trabalho: Cria uma pasta dentro do container
WORKDIR /app

# 3. Copia os arquivos de requisitos primeiro (para cachear a instalação)
COPY requirements.txt .

# 4. Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copia o resto do código para dentro do container
COPY . .

# 6. Expõe a porta que o Streamlit usa
EXPOSE 8501

# 7. Verifica se o container está saudável (Healthcheck)
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# 8. Comando para rodar o app quando o container iniciar
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]