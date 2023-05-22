# flaskproject

Para ejecutar este proyecto debe:

1 Levantar un contenedor docker con postgres ejecutando los siguientes comandos:
  - docker run --name postgres -e POSTGRES_PASSWORD=contraseña -p 5432:5432 -d postgres
  - docker exec -it #id_contenedor bash
  - cd
  - psql -h localhost -p 5432 -U postgres
  - CREATE DATABASE dbuser;
  - \c dbuser;
  - CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    cedula_identidad VARCHAR(20) NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    primer_apellido VARCHAR(50) NOT NULL,
    segundo_apellido VARCHAR(50),
    fecha_nacimiento DATE NOT NULL
);

2 Se debe ejecutar el ambiente virtual de python dentro de la carpeta del proyecto ejecutando:
  . .venv/bin/activate
  
3 Para ejectuar el proyecto ponemos:
  python3 app.py
  
4 Se abrira el puerto: 5000 en localhost: la ruta es la siguiente: http://127.0.0.1:5000/

5 En la carpeta postman se encuentran las invocaciones para probar las API's
