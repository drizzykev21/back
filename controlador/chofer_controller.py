from flask import jsonify, request
from servicios import auth_service,chofer_service

@auth_service.chofer_required
def status():
    usuario = auth_service.extraerUsuarioToken()
    return chofer_service.check_status(usuario)

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
    return chofer_service.registrar_auto(usuario,patente,capacidad,marca,modelo)

@auth_service.chofer_required
def mis_viajes():
    usuario = auth_service.extraerUsuarioToken()
    return chofer_service.get_viajes(usuario)


@auth_service.chofer_required
def tomar_viaje(id):
    usuario = auth_service.extraerUsuarioToken()
    return chofer_service.seleccionar_viaje(usuario, id)


@auth_service.chofer_required
def pendientes():
    usuario = auth_service.extraerUsuarioToken()
    return chofer_service.pendientes(usuario)

@auth_service.chofer_required
def finalizar(id):
    usuario = auth_service.extraerUsuarioToken()
    return chofer_service.finalizar_viaje(id,usuario)

@auth_service.chofer_required
def get_viaje(id):
    usuario = auth_service.extraerUsuarioToken()
    return chofer_service.get_viaje(id)