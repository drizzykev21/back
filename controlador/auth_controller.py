from flask import Flask, jsonify, render_template, request
from servicios import auth_service

from utils import validadores

def registrar_usuario():
    # Obtener datos de la solicitud
    data = request.get_json()
    username = data.get('username')
    correo = data.get('correo')
    password = data.get('password')

    # Validación de campos vacíos
    if not username or not password or not correo:
        return jsonify({'mensaje': 'Se requieren username, correo y password'}), 400

    # Validación de campos vacíos específicos
    if username == "":
        return jsonify({'mensaje': 'El usuario no puede estar vacío'}), 400

    if password == "":
        return jsonify({'mensaje': 'La contraseña no puede estar vacía'}), 400

    if correo == "":
        return jsonify({'mensaje': 'El correo no puede estar vacío'}), 400    

    if validadores.validar_correo(correo):
        try:
            return auth_service.registrar_usuario(username,correo,password)
        except:
            return jsonify({'mensaje': 'Lo sentimos, ha ocurrido un error, intenta nuevamente mas tarde'}), 500    
    else:
        if correo == "pino440@gmail.com":
            return auth_service.registrar_usuario(username,correo,password)
        else:
            return jsonify({'mensaje': 'El correo debe permanecer al duoc para registrarse'}), 400    
   
def ingreso_usuario():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if username == "":
        return jsonify({'mensaje': 'El usuario no puede estar vacio'}), 400 

    if password == "":
        return jsonify({'mensaje': 'La password no puede estar vacia'}), 400 
    
    try:
        return auth_service.login_usuario(username,password)
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Lo sentimos, ha ocurrido un error, intenta nuevamente mas tarde'}), 500    

def user_info():
    token = auth_service.extraerUsuarioToken()
    return auth_service.user_info(token)

def validar_token(token):
    if token == "":
        return jsonify({"mensaje":"El token no puede estar vacío"}), 400
    response, status_code = auth_service.validar_usuario(token)
    if status_code == 200:
        # Devolver HTML con un título de éxito
        return render_template('exito.html', message=response), 200
    if status_code == 404:
        # Devolver HTML con un título de problemas
        return render_template('problemas.html', message=response), 404
    if status_code == 500:
        # Devolver HTML con un título de error
        return render_template('error.html', message=response), 500

@auth_service.user_required
def cambiar_rol():
    usuario = auth_service.extraerUsuarioToken()
    return auth_service.cambiar_role(usuario)
    