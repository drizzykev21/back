from servicios.db import db

class Auto(db.Model):
    __tablename__ = 'autos'
    id = db.Column(db.Integer, primary_key=True)
    patente = db.Column(db.String(50), unique=True, nullable=False)
    capacidad = db.Column(db.String(100), nullable=False)
    modelo = db.Column(db.String(100), nullable=False)
    marca = db.Column(db.String(100), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    usuario = db.relationship('Usuario', backref='autos')

class Viaje(db.Model):
    __tablename__ = 'viajes'
    id = db.Column(db.Integer, primary_key=True)
    inicio = db.Column(db.String(100), nullable=False)
    destino = db.Column(db.String(100), nullable=False)
    auto_id = db.Column(db.Integer, db.ForeignKey('autos.id'))
    auto = db.relationship('Auto', backref='viajes')
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    usuario = db.relationship('Usuario', backref='viajes')
    tomado = db.Column(db.Boolean, nullable=False, default=False)
    finalizado = db.Column(db.Boolean, nullable=False, default=False)
    notificado = db.Column(db.Boolean, nullable=False, default=False)