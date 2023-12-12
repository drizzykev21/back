import sqlalchemy
from modelos.auth_models import Usuario
from modelos.viajes_models import Auto, Viaje
from servicios.db import db
from servicios import chofer_service as chofer, viajes_service as viajes
from test.auth_test import get_usuario
SECRET_KEY = "mLTpnwAy5FTpSte+aPZoOLFVBg7MyKhRDy++kEP5t4A="

def get_auto(usuario):
    return Auto.query.filter_by(usuario_id=usuario.id).first()

def registrar_auto():
    try:
        usuario = get_usuario("test23")
        auto_existente = get_auto(usuario)
        if auto_existente:
            print("Auto existente")
            return False
        else:
            chofer.registrar_auto(usuario, "dd-25-56", 3, "Nissan", "Terrananeitor")
            return True
    except:
        return False
    
def crear_viaje():
    try:
        conductor = get_usuario("test23")
        auto = Auto.query.filter_by(usuario_id=conductor.id).first()
        pasajero = get_usuario("test22")
        viajes.crear_viaje_db(pasajero,auto.id,"Centro Diagonal 23 #22", "Santa Pepita #225")
        return True
    except:
        return False
    
def get_viaje():
    try:
        usuario = get_usuario("test22")
        Viaje.query.filter_by(usuario_id=usuario.id).first()
        return True
    except:
        return False

def delete_viaje(usuario):
    viaje = Viaje.query.filter_by(usuario_id=usuario.id).first()
    db.session.delete(viaje)
    db.session.commit()
