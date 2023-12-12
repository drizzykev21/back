
from flask import jsonify
from modelos.auth_models import Usuario
from modelos.viajes_models import Auto, Viaje
from servicios import mail_service
from servicios.db import db 

def check_status(usuario):
    try:
        auto = Auto.query.filter_by(usuario_id=usuario.id).first()
        auto_json ={
        'id': auto.id,
        'marca': auto.marca,
        'patente': auto.patente,
        'capacidad': auto.capacidad,
        'modelo': auto.modelo,
        'usuario': auto.usuario.username
        }
        
        return jsonify({"auto": auto_json})
    except:
        return jsonify({'mensaje': 'No has registrado un auto aun'}), 400

def registrar_auto(usuario,patente,capacidad,marca,modelo):
    try:
        auto_existente = Auto.query.filter_by(usuario_id=usuario.id).first()

        if auto_existente:
            return jsonify({"mensaje": "Ya cuentas con un auto registrado"})

        nuevo_auto = Auto(
        patente=patente,
        capacidad=capacidad,
        marca=marca,
        modelo=modelo,
        usuario_id=usuario.id
        )

        try:
            db.session.add(nuevo_auto)
            db.session.commit()
            return jsonify({'mensaje': 'Auto creado exitosamente'}, 201)
        except Exception as e:
            db.session.rollback()
            return jsonify({'mensaje': 'No se ha podido crear el auto'}, 500)
    
    except Exception as e:
        return jsonify({"mensaje": f"No se pudo registrar el auto: {str(e)}"}), 400

def get_viajes(usuario):
    try:
        viajes = Viaje.query.join(Auto).filter(Auto.usuario_id == usuario.id, Viaje.finalizado == False).all()

        if viajes:
            viajes_list = []
            for viaje in viajes:
                viaje_json = {
                    'id': viaje.id,
                    'inicio': viaje.inicio,
                    'destino': viaje.destino,
                    'usuario': viaje.usuario.username
                }
                viajes_list.append(viaje_json)

            return jsonify({"viajes": viajes_list})
        else:
            return jsonify({'mensaje': 'No tienes viajes pendientes'}), 400

    except Exception as e:
        print(e)  # Manejo básico de la excepción para identificar errores
        return jsonify({'mensaje': 'Ha ocurrido un error'}), 500
    
def seleccionar_viaje(usuario,id):
    try:
        viaje = Viaje.query.filter_by(id=id).first()
        viaje.tomado = True
           
        try:
            db.session.add(viaje)
            db.session.commit()
            return {'mensaje': 'Viaje seleccionado con exito'}, 201
        except Exception as e:
            db.session.rollback()
            return {'mensaje': 'No se ha podido seleccionado el Viaje'}, 500       

    except Exception as e:
        print(e)  # Manejo básico de la excepción para identificar errores
        return jsonify({'mensaje': 'Ha ocurrido un error'}), 500
    
def pendientes(usuario):
    try:
        viaje = Viaje.query.join(Auto).join(Usuario, Usuario.id == Auto.usuario_id).filter(Viaje.tomado == True, Viaje.finalizado == False, Viaje.notificado== False,Usuario.id == usuario.id).first()
        if viaje:
            viaje_data = {
                'id': viaje.id,
                'inicio': viaje.inicio,
                'destino': viaje.destino,
                'usuario': viaje.usuario.username
            }
            return jsonify({'viaje': viaje_data})
        else:
            return jsonify({'mensaje': 'No se encontró el viaje para el usuario o no está tomado'}), 404

    except Exception as e:
        print(e)  # Manejo básico de la excepción para identificar errores
        return jsonify({'mensaje': 'Ha ocurrido un error'}), 500

def finalizar_viaje(id,usuario):
    try:
        viaje = Viaje.query.filter_by(id=id).first()
        chofer = viaje.auto.usuario.username
        if viaje:
            viaje.finalizado = True
            viaje.tomado = False
            db.session.add(viaje)
            db.session.commit()
            correo = viaje.usuario.correo
            usuario = viaje.usuario.username
            viaje_data = {
                'id': viaje.id,
                'inicio': viaje.inicio,
                'destino': viaje.destino,
                'usuario': viaje.usuario.username,
                'finalizado': viaje.finalizado,
                'chofer': chofer
            }
            mensaje = mail_service.enviar_mensaje_viaje_finalizado(usuario, correo, viaje)
            print(mensaje)
            return jsonify({'viaje': viaje_data, "mensaje":"viaje finalizado con exito"})
        else:
            return jsonify({'mensaje': 'No se encontró el viaje para el usuario o no está tomado'}), 404

    except Exception as e:
        print(e)  # Manejo básico de la excepción para identificar errores
        return jsonify({'mensaje': 'Ha ocurrido un error'}), 500
    
def get_viaje(id):
    try:
        viaje = Viaje.query.filter_by(id=id).first()
        chofer = viaje.auto.usuario.username
        viaje_data = {
            'id': viaje.id,
            'inicio': viaje.inicio,
            'destino': viaje.destino,
            'usuario': viaje.usuario.username,
            'finalizado': viaje.finalizado,
            'chofer': chofer
        }
        return jsonify({'viaje': viaje_data})

    except Exception as e:
        print(e)  # Manejo básico de la excepción para identificar errores
        return jsonify({'mensaje': 'Ha ocurrido un error'}), 500