from servicios.db import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    habilitado = db.Column(db.Boolean, nullable=False, default=False)
    token_validacion = db.Column(db.String(100))
    password = db.Column(db.String(100), nullable=False)
    rol = db.Column(db.String(20), nullable=False)
    
    # Constructor
    def __init__(self, username, correo, password, rol, token_validacion=None):
        self.username = username
        self.correo = correo
        self.password = password
        self.rol = rol
        self.token_validacion = token_validacion
