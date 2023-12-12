from flask import jsonify
from modelos.viajes_models import Auto, Viaje
from servicios.db import db


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
    return jsonify({"autos": autos_list}), 200   

def crear_viaje_db(usuario, auto_id, destino, inicio):
    # Crea un nuevo viaje utilizando SQLAlchemy y los modelos definidos
    nuevo_viaje = Viaje(inicio=inicio, destino=destino, auto_id=auto_id, usuario_id=usuario.id)
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
    
def check_viaje(usuario):
    viaje = Viaje.query.filter_by(usuario_id=usuario.id, finalizado=False).first()
    if viaje:
        viajeDTO = {
            "id": viaje.id,
            "inicio": viaje.inicio,
            "destino": viaje.destino,
            "tomando": viaje.tomado,
            "finalizado": viaje.finalizado,
            "notificado": viaje.notificado
        }
        if viaje.auto:
            viajeDTO["auto"] = {
                "patente": viaje.auto.patente,
                "capacidad": viaje.auto.capacidad
            }
            if viaje.auto.usuario:
                viajeDTO["chofer"] = viaje.auto.usuario.username
            else:
                viajeDTO["chofer"] = None
        else:
            viajeDTO["auto"] = None
        
        return jsonify({"viaje": viajeDTO})
    else:
        viaje = Viaje.query.filter_by(usuario_id=usuario.id, finalizado=True, notificado = False).first()
        if viaje:
            viajeDTO = {
            "id": viaje.id,
            "inicio": viaje.inicio,
            "destino": viaje.destino,
            "tomando": viaje.tomado,
            "finalizado": viaje.finalizado,
            "notificado": viaje.notificado
            }
            if viaje.auto:
                viajeDTO["auto"] = {
                    "patente": viaje.auto.patente,
                    "capacidad": viaje.auto.capacidad
                }
                if viaje.auto.usuario:
                    viajeDTO["chofer"] = viaje.auto.usuario.username
                else:
                    viajeDTO["chofer"] = None
                
            return jsonify({"viaje":viajeDTO}),200
        else:
            return jsonify({"mensaje":"No existen viajes para este usuario"}),400
        
def cambiar_estado(usuario):
    viaje = Viaje.query.filter_by(usuario_id=usuario.id, finalizado=True, notificado=False).first()

    if viaje is None:
        return jsonify({'mensaje': 'No se encontró un viaje para finalizar'}), 404

    viaje.notificado = True
    try:
        db.session.add(viaje)
        db.session.commit()
        # Aquí podría ir la lógica para enviar la notificación al usuario
        return jsonify({'mensaje': 'Su viaje ha finalizado con éxito'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'mensaje': 'Error al finalizar el viaje: ' + str(e)}), 500
