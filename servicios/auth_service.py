from functools import wraps
from flask import jsonify, request
from passlib.hash import sha256_crypt
import datetime
import jwt
from servicios.db import db 
from modelos.auth_models import Usuario
from servicios import mail_service
import sqlalchemy.exc 
SECRET_KEY = "mLTpnwAy5FTpSte+aPZoOLFVBg7MyKhRDy++kEP5t4A="

# Función para verificar el token JWT
def user_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'mensaje': 'Debes Ingresar Un Token Valido'}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            rol = data['rol']
            if rol == "usuario":
                return f(*args, **kwargs)
            else:
                return jsonify({'mensaje': 'No estas autorizado para ingresar aqui'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'mensaje': 'El Token Ingresado Esta Expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'mensaje': 'El Token Ingresado Es Inválido'}), 401

    return decorated

def chofer_required(f): 
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'mensaje': 'Debes Ingresar Un Token Valido'}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            rol = data['rol']
            if rol == "chofer":
                return f(*args, **kwargs)
            else:
                return jsonify({'mensaje': 'no estas autorizado para ingresar aqui'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'mensaje': 'El Token Ingresado Esta Expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'mensaje': 'El Token Ingresado Es Inválido'}), 401

    return decorated

def encriptar_password(password):
    return sha256_crypt.hash(password)

def verificar_password(password, password_encriptada):
    return sha256_crypt.verify(password, password_encriptada)

def generar_token(usuario,rol):
    expiracion = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    token = jwt.encode({'usuario': usuario,'rol': rol, 'exp': expiracion}, SECRET_KEY)
    return token

def login_usuario(username, password):
    # Busca el usuario en la base de datos por su nombre de usuario
    try:
        usuario = Usuario.query.filter_by(username=username).first()
        if not usuario.habilitado:
            return jsonify({'mensaje': 'El usuario ingresado no está habilitado, porfavor valide su correo'}), 400                   
    except:
        return jsonify({'mensaje': 'El usuario ingresado no es valido'}), 400
    # Verifica si el usuario existe y la contraseña coincide
    if usuario and verificar_password(password, usuario.password):
        # Genera un token JWT si las credenciales son válidas
        token = generar_token(username, usuario.rol)
        return jsonify({'token':token,'usuario':usuario.username,'rol':usuario.rol}), 200
    
    return jsonify({'mensaje': 'Porfavor verifique sus credenciales'}), 400

def cambiar_role(usuario):
    if not usuario:
        return jsonify({'mensaje': 'Usuario no encontrado'}), 404

    # Actualiza el rol del usuario a "chofer"
    usuario.rol = 'chofer'

    try:
        # Guarda los cambios en la base de datos
        db.session.commit()
        return jsonify({"token":generar_token(usuario.username, usuario.rol),"rol":usuario.rol, "mensaje":"Gracias por registrarte como chofer, porfavor registra tu vehiculo"})
    except Exception as e:
        db.session.rollback()
        return jsonify({'mensaje': 'No se pudo cambiar el rol'}), 500
    
def registrar_usuario(username,correo,password):
    try:
        # Verificar si el usuario ya existe en la base de datos
        if Usuario.query.filter_by(username=username).first():
            return jsonify({'mensaje': 'El usuario ya existe'}), 400

        if Usuario.query.filter_by(correo=correo).first():
            return jsonify({'mensaje': 'El correo ya existe'}), 400
        token = mail_service.generar_token()
        # Crear nuevo usuario
        nueva_password = encriptar_password(password)
        nuevo_usuario = Usuario(username=username, password=nueva_password, correo=correo, rol="usuario", token_validacion=token)
        mail_service.enviar_mensaje_validacion(correo, token)
        db.session.add(nuevo_usuario)
        db.session.commit()
        return jsonify({'mensaje': 'Usuario creado exitosamente, por favor verifique su cuenta de correo electronico'}), 201

    except sqlalchemy.exc.SQLAlchemyError as db_error:
        # Registrar el error de la base de datos
        print(f"Error de base de datos: {str(db_error)}")
        return jsonify({'mensaje': 'Error en la base de datos'}), 500
    
    except Exception as e:
        # Registrar cualquier otra excepción no manejada
        print(f"Error inesperado: {str(e)}")
        return jsonify({'mensaje': f'Error inesperado: {str(e)}'}), 500
    
def validar_usuario(token):
    try:
        usuario = Usuario.query.filter_by(token_validacion=token).first()

        if not usuario:
            return'Token de validación no válido', 404

        # Realiza la validación del usuario
        usuario.token_validacion = ""
        usuario.habilitado = True

        # Guarda los cambios en la base de datos utilizando una transacción
        db.session.add(usuario)
        db.session.commit()
        mail_service.enviar_mensaje_validado(usuario.correo)
        return 'Usuario validado correctamente', 200
            
    except Exception as e:
        # Manejo seguro de excepciones
        db.session.rollback()
        return 'Error al validar el usuario', 500

def user_info(usuario):
    try:
        return jsonify({
            'username': usuario.username,
            'correo': usuario.correo,
            'rol':usuario.rol
            }), 200

    except jwt.ExpiredSignatureError:
        return jsonify({'mensaje': 'El Token Ingresado Esta Expirado'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'mensaje': 'El Token Ingresado Es Inválido'}), 401
    
def extraerUsuarioToken():
    token = None

    if 'Authorization' in request.headers:
        token = request.headers['Authorization'].split(" ")[1]

    if not token:
        return jsonify({'mensaje': 'Debes Ingresar Un Token Valido'}), 401
    
    data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    username = data['usuario']
    usuario = Usuario.query.filter_by(username=username).first()
    return usuario