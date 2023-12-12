from modelos.viajes_models import Viaje,Auto 
from servicios.db import db 
from flask import jsonify
from modelos.auth_models import Usuario

def crear_viaje_db(inicio, destino, auto_id, usuario):
    # Crea un nuevo viaje utilizando SQLAlchemy y los modelos definidos
    nuevo_viaje = Viaje(inicio=inicio, destino=destino, auto_id=auto_id, usuario_id=obtenerIdUsuario(usuario))
    # Agrega el nuevo viaje a la sesión y guarda en la base de datos
    print("creando viaje")
    try:
        db.session.add(nuevo_viaje)
        db.session.commit()
        auto = Auto.query.filter_by(id=auto_id).first()
        return jsonify({'mensaje': 'Viaje creado exitosamente', 'chofer':auto.usuario.username}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'mensaje': 'No se ha podido crear el viaje'}), 500

def obtenerIdUsuario(username):
    usuario = Usuario.query.filter_by(username=username).first()
    return usuario.id

def crear_auto(patente, capacidad,marca, modelo, username):
    nuevo_auto = Auto(
        patente=patente,
        capacidad=capacidad,
        marca=marca,
        modelo=modelo,
        usuario_id=obtenerIdUsuario(username)
    )

    try:
        db.session.add(nuevo_auto)
        db.session.commit()
        return {'mensaje': 'Auto creado exitosamente'}, 201
    except Exception as e:
        db.session.rollback()
        return {'mensaje': 'No se ha podido crear el auto'}, 500
    
def obtener_autos():
    autos = (
        Auto.query
        .filter(Auto.capacidad != 0)  # Filtra los autos cuya capacidad no sea igual al valor dado
        .limit(3)  # Limita la consulta a obtener solo 3 autos
        .all()
    )   
    # Prepara la lista de autos para devolver los datos requeridos
    autos_list = [
        {
            'id': auto.id,
            'marca': auto.marca,
            'patente': auto.patente,
            'capacidad': auto.capacidad,
            'modelo': auto.modelo,
            'usuario': auto.usuario.username
        }
        for auto in autos
    ]
    return jsonify({'autos': autos_list}), 200   

def obtener_autos_chofer(username):
    usuario = Usuario.query.filter_by(username=username).first()

    if usuario is None:
        return jsonify({'mensaje': 'Usuario no encontrado'}), 404

    autos_del_usuario = Auto.query.filter_by(usuario_id=usuario.id).all()

    autos_list = [
        {
            'id': auto.id,
            'patente': auto.patente,
            'capacidad': auto.capacidad,
            'modelo': auto.modelo,
            'marca': auto.marca,
            'usuario': auto.usuario.username
        }
        for auto in autos_del_usuario
    ]

    return autos_list

def saluda():
    return {'mensaje': 'Bienvenido a tellevoapp'}, 200