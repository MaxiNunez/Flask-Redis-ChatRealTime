# Flask-Redis-ChatRealTime

Crea el contenedor con la imagen de redis en el puerto 6379:6379
----------------------------------------------------------------
$ docker run --name redistp3 -p 6379:6379 -d redis

Levantar imagen o detenerla
---------------------------
$ docker start redistp3
$ docker stop redistp3

Correr app
----------
$ export FLASK_DEBUG=1
$ flask run
