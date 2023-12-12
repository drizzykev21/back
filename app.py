from flask import Flask
from controlador import auth_controller as auth, home_controller as home, chofer_controller as chofer, viaje_controller as viaje
from servicios.db import init_app
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Hola123@localhost/radic21$app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mLTpnwAy5FTpSte+aPZoOLFVBg7MyKhRDy++kEP5t4A='

CORS(app, resources={r"/*": {"origins": "*"}})
init_app(app)

@app.route('/registro', methods=['POST'])
def registro():
    return auth.registrar_usuario()

@app.route('/login', methods=['POST'])
def login():
    return auth.ingreso_usuario()

@app.route('/validarToken/<token>', methods=['GET'])
def validarToken(token):
    return auth.validar_token(token)
         
@app.route('/user-info', methods=['GET'])
def user_info():
    return auth.user_info()

@app.route('/')
def saludos():
    return home.saludar()

@app.route('/cambiar_rol', methods=['GET'])
def cambiar_rol():
    return auth.cambiar_rol()

@app.route('/registrar_auto', methods=['POST'])
def registrar_auto():
    return chofer.registrar_auto()

@app.route('/check_status', methods=['GET'])
def check_status():
    return chofer.status()

@app.route('/obtener-autos', methods=['GET'])
def get_autos():
    return viaje.get_autos()

@app.route('/crear-viaje', methods=['POST'])
def crear_viaje():
    return viaje.crear_viaje()

@app.route('/check-viaje', methods=['GET'])
def check_viaje():
    return viaje.check_status_viaje()

@app.route('/mis-viajes', methods=['GET'])
def mis_viajes():
    return chofer.mis_viajes()

@app.route('/tomar-viaje/<id>', methods=['POST'])
def tomar_viaje(id):
    return chofer.tomar_viaje(id)

@app.route('/check-pendientes', methods=['GET'])
def pendientes():
    return chofer.pendientes()

@app.route('/finaliza/<id>', methods=['GET'])
def finaliza_viaje(id):
    return chofer.finalizar(id)

@app.route('/get_viaje/<id>', methods=['GET'])
def get_viaje(id):
    return chofer.get_viaje(id)

@app.route('/cambiar_estado', methods=['GET'])
def cambiar_Estado():
    return viaje.cambiar_estado_viaje()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')