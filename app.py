from flask import Flask
from flask import render_template, request,redirect, url_for, Response
import redis

#---> PUBSUB channels  /Lista los canales que esten activos.
#---> SUSCRIBE nombredelcanal1 nombredelcanal2  /Suscribirse a un canal o mas de uno.
#---> UNSUSCRIBE      /Cancelar suscripcion a todos los canales.
#---> UNSUSCRIBE nombredecanal1 nombredCanal de ecanal2 /Cancelar suscripcion a canales. 
#---> PUBSUB NUMSUB nombredelcanal1 nombredelcanal2  /Retorna la cantidad de subcriptores en cada canal.
#---> PUBLISH nombredecanal "mensaje" /Para publicar un mensaje en un canal.

#export FLASK_DEBUG=1
#FLASK run

app = Flask(__name__)
r = redis.StrictRedis(host='127.0.0.1', port= 6379, decode_responses=True, charset='utf-8',db=0)

def connect_db():
    """Crear conexion a base de datos."""
    conexion = redis.StrictRedis(host='127.0.0.1', port= 6379, decode_responses=True, charset='utf-8',db=0)
    if (conexion.ping()):
        print ("conectado al servidor de redis")
    else:
        print("error...")
    return conexion

def event_stream():
    pubsub = r.pubsub(ignore_subscribe_messages=True)
    misCanales = connect_db().lrange('misCanales',0,-1)
    pubsub.subscribe(misCanales)
    
    for message in pubsub.listen():
        yield 'data: %s\n\n'% message['data'] 

@app.route('/stream')
def stream():
    return Response(event_stream(), mimetype="text/event-stream")

@app.route('/imagenes')
def imagenes():
    """Cargar carpeta imagenes"""
    return render_template('imagenes.html',img_path = url_for('static'))

@app.route('/')
def index():
    """Index(Principal-inicio)."""
    misCanales = connect_db().lrange('misCanales',0,-1)
    return render_template('index.html', misCanales = misCanales)
    
@app.route('/canales')
def canales():
    """Pestaña canales(Canales Activos)."""
    lista = [] 
    canalesActivos = connect_db().lrange('canales',0,-1)
    if canalesActivos == []:
        connect_db().lpush("canales","Mesas de Examen","Becas","Extension","Deportes","Carreras Tics","Profesorados")
    else:
        connect_db().pubsub().subscribe(canalesActivos)
        for subs in canalesActivos:
            lista.append(connect_db().pubsub_numsub(subs))

    return render_template('canales.html', lista = lista)

@app.route('/subscribe', methods=['POST'])
def subscribe():
    """Subscribir a un canal."""
    canal = request.args.get('can')
    misCanales = connect_db().lrange('misCanales',0,-1)
    if not canal in misCanales:
        connect_db().lpush("misCanales",canal)

    return redirect(url_for('index'))
    
@app.route('/cansubscribe', methods=['POST'])
def cansubscribe():
    """Cancelar subscripcion de un canal."""
    canal = request.args.get('can')
    connect_db().lrem("misCanales",1,canal)
    connect_db().pubsub().unsubscribe(canal)
    misCanales = connect_db().lrange('misCanales',0,-1)
    
    return render_template('index.html', misCanales = misCanales)

@app.route('/publicarMsj', methods=['GET','POST'])
def publicarMsj():
    """Publica el mensaje en Chat-en-vivo."""
    msj = request.args.get('texto')
    misCanales = connect_db().lrange('misCanales',0,-1)
    
    for canal in misCanales:
        connect_db().publish(canal,('Publicaste en '+canal+': '+msj))

    return Response(status=204)

@app.route('/publicar')
def Pespublicar():
    """Pestaña publicar(Cliente)."""
    canales = connect_db().lrange('canales',0,-1)
    return render_template('publicar.html',canales = canales)

@app.route('/clienteMsj', methods=['GET','POST'])
def clienteMsj():
    """Publica un mensaje en un canal determinado."""
    msj = request.args.get('texto')
    can = request.args.get('canal')
    
    connect_db().publish(can,(can+' dice: '+msj))
    canales = connect_db().lrange('canales',0,-1)
    
    return render_template('publicar.html', canales = canales)
        
@app.route('/about')
def about():        
    """Retorna la pagina about."""
    return 'about Python Flask'    

if __name__ == '__main__':
    app.run(host ='localhost', port='5000', debug=True)