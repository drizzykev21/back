# Backend TeLlevoApp

## Estructura de la base de datos: 
![Alt text](docs/image.png)

## Como ejecutar el programa en local
Si es la primera vez, realiza un git clone al repositorio.
crea un nuevo enviroment virtual con los siguientes comandos:

``` bash
python -m venv venv 
# o 
py -m venv venv
# luego activamos el enviroment, en windows usa:
venv/Scripts/activate
# en linux
source venv/bin/activate
```

Una vez tengamos nuestro venv activo instalaremos los paquetes de la aplicacion, para esto ejecutamos los siguientes comandos:

``` bash
# para ejecutar en local:
pip install -r requirements.txt
python app.py

# para docker:
docker build -t nombre_imagen:version .
```

Para ejecutar los test deberemos usar los siguientes comandos:

``` bash
python test.py
```

# Endpoints disponibles

## Authorizacion:

- Login :
    - Metodo: POST
    - URL: /login
    - Encabezado: No Requiere 
    - Rol: No Requiere
    - Cuerpo: 
        ``` json 
        {
        "username":"usuario",
        "password":"password"
        }
        ```  
- Registro :
    - Metodo: POST
    - URL: /registro
    - Encabezado: No Requiere 
    - Rol: No Requiere
    - Cuerpo: 
        ``` json 
        {
        "username":"usuario",
        "correo":"correo",
        "password":"password"
        } 
        ```
    
- Validar Token :
    - Metodo: GET.
    - URL: /validarToken/<token> --> se debe enviar por la url el parametro token ejemplo : /validarToken/soyeltokendevalidacion.
    - Encabezado: No Requiere .
    - Rol: No Requiere
    - Cuerpo: No Requiere.
    
- Info del Usuario :
    - Metodo: GET
    - URL: /user-info
    - Encabezado: Authorization: Bearer token --> token obtenido desde el login
    - Rol: No Requiere
    - Cuerpo: No Requiere

- Cambiar Rol :
    - Metodo: GET
    - URL: /cambiar_rol
    - Encabezado: Authorization: Bearer token --> token obtenido desde el login
    - Rol: usuario
    - Cuerpo: No Requiere
## Servicios Choferes:

- Registrar auto :
    - Metodo: POST
    - URL: /registrar_auto
    - Encabezado: Authorization: Bearer token 
    - Rol: Chofer
    - Cuerpo: 
        ``` json 
        {
            "patente":"",
            "capacidad":4,
            "modelo":"Nissan",
            "marca":"Terraneitor"
        }
        ```#   b a c k  
 