FROM python:3.13

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
# copio la carpeta ./app a la app del contenedor
COPY ./app /app/app
# Para instalar uvicorn
#RUN pip install --no-cache-dir --upgrade uvicorn
# Ejecutamos el servidor uvicorn en en el puerto 80 con reload
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]