from email.message import EmailMessage
import smtplib
import random
import string


url = "http://localhost:5000"
remitente = "registros.tellevoapp@gmail.com"
password = "wabm pwsd rfib wlse"

def generar_token():
    # Generar un token aleatorio de longitud 8
    longitud = 8
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for i in range(longitud))

def enviar_mensaje_validacion(destinatario, token):
    global url, remitente, password  # Accediendo a las variables globales
    asunto = "Validación de correo electrónico - Te Llevo App"

    url = url + "/validarToken/"+token

    # Construir el cuerpo del mensaje
    mensaje = f"""\
    Estimado usuario,

    ¡Bienvenido a Te Llevo App!

    Gracias por registrarte en nuestra plataforma. Para completar el proceso de registro, 
    necesitamos verificar tu dirección de correo electrónico.

    Por favor, utiliza este enlace {url}
    para completar el proceso de validación en nuestra aplicación.

    Si tienes alguna pregunta o necesitas asistencia, no dudes en contactarnos.

    Atentamente,
    El equipo de Te Llevo App
    """

    email = EmailMessage()
    email["From"] = remitente
    email["To"] = destinatario
    email["Subject"] = asunto
    email.set_content(mensaje)

    smtp = smtplib.SMTP_SSL("smtp.gmail.com")
    smtp.login(remitente, password)
    smtp.sendmail(remitente, destinatario, email.as_string())
    smtp.quit()

    return "mensaje enviado con exito"

def enviar_mensaje_validado(destinatario):
    global url, remitente, password  # Accediendo a las variables globales
    asunto = "Su correo ha sido validado con exito - Te Llevo App"

    # Construir el cuerpo del mensaje
    mensaje = f"""\
    Estimado usuario,

    ¡Bienvenido a Te Llevo App!

    Gracias por validar tu correo en nuestra plataforma. 
    
    Si tienes alguna pregunta o necesitas asistencia, no dudes en contactarnos.

    Atentamente,
    El equipo de Te Llevo App
    """

    email = EmailMessage()
    email["From"] = remitente
    email["To"] = destinatario
    email["Subject"] = asunto
    email.set_content(mensaje)

    smtp = smtplib.SMTP_SSL("smtp.gmail.com")
    smtp.login(remitente, password)
    smtp.sendmail(remitente, destinatario, email.as_string())
    smtp.quit()

    return "mensaje enviado con exito"
    
def enviar_mensaje_viaje_finalizado(usuario,correo, viaje):
    print("enviando mensaje finalizacion")
    inicio = viaje.inicio  # Suponiendo que viaje tiene un atributo inicio
    fin = viaje.destino  # Suponiendo que viaje tiene un atributo usuario
    chofer =  viaje.auto.usuario.username
  # Suponiendo que viaje tiene un atributo chofer
    global url, remitente, password  # Accediendo a las variables globales
    asunto = "Su viaje ha finalizado con éxito - Te Llevo App"

    # Construir el cuerpo del mensaje
    mensaje = f"""\
    Estimado {usuario} ,

    ¡Esperamos que haya tenido un excelente viaje con nosotros en Te Llevo App!

    Su viaje desde {inicio} hasta {fin} con nuestro chofer {chofer} ha finalizado exitosamente.

    Si tiene alguna pregunta o necesita asistencia adicional, no dude en contactarnos.

    Atentamente,
    El equipo de Te Llevo App
    """

    email = EmailMessage()
    email["From"] = remitente
    email["To"] = correo
    email["Subject"] = asunto
    email.set_content(mensaje)

    smtp = smtplib.SMTP_SSL("smtp.gmail.com")
    smtp.login(remitente, password)
    smtp.sendmail(remitente, correo, email.as_string())
    smtp.quit()

    return "mensaje enviado con exito"
    