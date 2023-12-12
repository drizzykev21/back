import unittest
from flask import Flask
from servicios.db import db
from test import auth_test as auth, chofer_test as chofer

token = ""
class TestAuth(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Pinolabs@localhost/radic21$app'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['SECRET_KEY'] = 'mLTpnwAy5FTpSte+aPZoOLFVBg7MyKhRDy++kEP5t4A='
        self.token = token  # Accede a la variable global 'token'
        db.init_app(self.app)
        
    #TODO: Registra usuario
    def test_01_registro(self):
        print("------------------------------------------")
        print("Testeando: Registro de usuarios")
        with self.app.app_context():
            print("registro usuario test23")
            resultado = auth.registrar_usuario("test23", "test22@gmail.com", "test")
            auth.validar_usuario()
            print("registro usuario test22")
            resultado = auth.registrar_usuario("test22", "test23@gmail.com", "test")
            print("Resultado: " + str(resultado))
            self.assertTrue(resultado)

    #TODO: Validacion de correo del usuario
    def test_02_validar_registro(self):
        print("------------------------------------------")
        print("Testeando: Validacion de usuarios (correo)")
        with self.app.app_context():
            resultado = auth.validar_usuario()
            print("Resultado: " + str(resultado))
            self.assertTrue(resultado)

    #TODO: Ingreso de usuarios
    def test_03_login(self):
        global token
        print("------------------------------------------")
        print("Testeando: Login de usuarios")
        with self.app.app_context():
            resultado = auth.login_test("test22", "test")
            token = resultado[1]  # Almacena el token en el atributo de clase
            self.assertTrue(resultado[0])
            print("Resultado: " + str(resultado[0]))

    #TODO: Validacion de token
    def test_04_validacion_token(self):
        resultado = False
        print("------------------------------------------")
        print("Testeando: Validacion de token")
        with self.app.app_context():
            if self.token:
                resultado = auth.extraer_usuario(self.token)
            else:
                resultado = False
                print("sin token")
                
            print("Resultado: " + str(resultado))
            self.assertTrue(resultado)    
        
    #TODO: Registra un chofer cambiando su rol
    def test_05_cambio_rol(self):
        resultado = False
        print("------------------------------------------")
        print("Testeando: Cambio rol, creacion de chofer ")
        with self.app.app_context():
            resultado = auth.cambiar_rol("test23")
                
            print("Resultado: " + str(resultado))
            self.assertTrue(resultado)   
            
    #TODO: Registra un auto para el chofer
    def test_06_registro_auto(self):
        resultado = False
        print("------------------------------------------")
        print("Testando: Registro de autos")
        with self.app.app_context():
            resultado = chofer.registrar_auto()
            print("Resultado: " + str(resultado))
            self.assertTrue(resultado)   
    #TODO: guarda un viaje en la base de datos
    def test_07_registrar_viaje(self):
        resultado = False
        print("------------------------------------------")
        print("Testando: Creacion de viaje")
        with self.app.app_context():
            resultado = chofer.crear_viaje()
            print("Resultado: " + str(resultado))
            self.assertTrue(resultado) 
    #TODO: Trae de la base de datos el viaje creado
    def test_08_consultar_viaje(self):
        resultado = False
        print("------------------------------------------")
        print("Testando: Consulta de viajes")
        with self.app.app_context():
            resultado = chofer.get_viaje()
            print("Resultado: " + str(resultado))
            self.assertTrue(resultado) 
        
    #TODO: borra todos los datos creados de la bd
    def test_10_borrar_datos(self):
        print("------------------------------------------")
        print("Limpiando Datos")
        with self.app.app_context():
            usuario = auth.get_usuario("test22")
            chofer.delete_viaje(usuario)
            if usuario:
                db.session.delete(usuario)
                db.session.commit()
            usuario = auth.get_usuario("test23")
            auto = chofer.get_auto(usuario)
            if usuario:
                db.session.delete(auto)
                db.session.commit()
                db.session.delete(usuario)
                db.session.commit()

if __name__ == '__main__':
    unittest.main()
