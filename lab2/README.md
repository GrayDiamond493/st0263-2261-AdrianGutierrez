# Redis CRUD

Redis CRUD es una aplicacion minimalista que permita realizar
operaciones CRUD basicas a una base de datos Redis, tal y como
lo haria un cliente Redis.

## Instalación

Para su funcionamiento, deben instalarse las siguientes dependencias:

`$ pip3 install redis`
`$ pip3 install hiredis`

Y puede ejecutarse utilizando:
`$ python3 redisCRUD.py`

## Cómo se usa

Solo necesitas ejecutar el comando
`$ python3 redisCRUD.py`
y la aplicacion ofrece una interfaz basada en terminal de comandos para
realizar sus funciones

Es muy importante cambiar la variable global 'hostname' por la ip publica
que utilice la maquina en la que corre su servidor Redis. Asimismo, es de
suma importancia abrir el puerto 6379 para entrada desde cualquier IP en su
maquina con Redis.

El  comando
`$ python3 redisCRUD.py -h`
Abre un mensaje de ayuda minimo

## Autor
Adrian Alberto Gutierrez Leal