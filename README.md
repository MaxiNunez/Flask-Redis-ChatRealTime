# Flask-Redis-ChatRealTime

Crea el contenedor con la imagen de redis en el puerto 6379:6379
----------------------------------------------------------------
$ docker run --name redistp3 -p 6379:6379 -d redis

Levantar imagen redistp3
---------------------------
$ docker start redistp3

Correr app
----------
$ flask run
