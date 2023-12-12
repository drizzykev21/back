# Usa la imagen base de Python
FROM python:3.9-slim
# Instala curl
RUN apt-get update && apt-get install -y curl
# Establece el directorio de trabajo en /app
WORKDIR /app
# Copia el código de la aplicación en el contenedor
COPY . /app
# Istala las dependencias necesarias
RUN pip install -r requirements.txt
# Expone el puerto 5000
EXPOSE 5000
# Comando para ejecutar la aplicación cuando el contenedor se inicia
CMD ["python", "app.py"]
