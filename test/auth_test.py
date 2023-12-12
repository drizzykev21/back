import jwt
import sqlalchemy
from modelos.auth_models import Usuario
from servicios import auth_service as auth
from servicios.db import db
SECRET_KEY = "mLTpnwAy5FTpSte+aPZoOLFVBg7MyKhRDy++kEP5t4A="

def get_usuario(username):
        usuario = Usuario.query.filter_by(username=username).first()
        return usuario
    
def login_test(username, password):
    try:
        usuario = get_usuario(username)
        if usuario.habilitado == False:
            print("no habilitado")
            return False, None           
        else:
            if usuario and auth.verificar_password(password, usuario.password):
                token = auth.generar_token(username, usuario.rol)
                return True, token 
    except:
        print("no habilitado")
        return False, None
   
def registrar_usuario(username,correo,password):
    try:
        if get_usuario(username):
            print("existe usuario")
            return False
        if Usuario.query.filter_by(correo=correo).first():
            print("existe correo")
            return False
        nueva_password = auth.encriptar_password(password)
        nuevo_usuario = Usuario(username=username, password=nueva_password, correo=correo, rol="usuario", token_validacion="jksidjsidjsopaisjdpaisdpijasd")
        db.session.add(nuevo_usuario)
        db.session.commit()
        return True

    except sqlalchemy.exc.SQLAlchemyError as db_error:
        return False
    
    except Exception as e:
        return False
    
def validar_usuario():
    try:
        usuario = Usuario.query.filter_by(token_validacion="jksidjsidjsopaisjdpaisdpijasd").first()
        if not usuario:
            print("no existe usuario")
            return False
        # Realiza la validación del usuario
        usuario.token_validacion = ""
        usuario.habilitado = True
        # Guarda los cambios en la base de datos utilizando una transacción
        db.session.add(usuario)
        db.session.commit()
        return True
            
    except Exception as e:
        print(e)
        print("error al validar usuario")
        # Manejo seguro de excepciones
        db.session.rollback()
        return False
    
def extraer_usuario(token):
    data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    username = data['usuario']
    return True

def cambiar_rol(username):
    usuario = get_usuario(username)
    usuario.rol = 'chofer'
    try:
        # Guarda los cambios en la base de datos
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False
