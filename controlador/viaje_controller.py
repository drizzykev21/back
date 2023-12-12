from flask import jsonify, request
from servicios import auth_service,viajes_service as viaje

@auth_service.user_required
def get_autos():
    return viaje.obtener_autos()

@auth_service.chofer_required
def registrar_auto():
    usuario = auth_service.extraerUsuarioToken()
    data = request.get_json()
    if not all(key in data for key in ('patente', 'capacidad', 'modelo','marca')):
        return jsonify({'mensaje': 'Faltan datos para crear el auto'}), 400
    patente = data['patente']
    capacidad = data['capacidad']
    modelo = data['modelo']
    marca = data['marca']
    return viaje.crear_viaje_db(usuario,patente,capacidad,marca,modelo)

@auth_service.user_required
def crear_viaje():
    usuario = auth_service.extraerUsuarioToken()
    data = request.get_json()
    if not all(key in data for key in ('auto_id', 'destino', 'inicio')):
        return jsonify({'mensaje': 'Faltan datos para crear el auto'}), 400
    auto_id = data['auto_id']
    destino = data['destino']
    inicio = data['inicio']
    return viaje.crear_viaje_db(usuario,auto_id,destino,inicio)

@auth_service.user_required
def check_status_viaje():
    usuario = auth_service.extraerUsuarioToken()
    return viaje.check_viaje(usuario)
  
@auth_service.user_required  
def cambiar_estado_viaje():
    usuario = auth_service.extraerUsuarioToken()
    return viaje.cambiar_estado(usuario)
    