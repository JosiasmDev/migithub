# Usa una imagen base de Python
FROM python:3.9

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY . .

# Actualiza pip
RUN pip install --upgrade pip

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Ejecuta collectstatic para los archivos estáticos
RUN python manage.py collectstatic --noinput

# Expon el puerto
EXPOSE 8080

# Comando para iniciar Django con el servidor de producción
CMD ["gunicorn", "mi_proyecto.wsgi", "--bind", "0.0.0.0:8080"]
