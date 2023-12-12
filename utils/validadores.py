import re

def validar_correo(correo):
    dominios_permitidos = ['duoc.cl', 'duocuc.cl', 'algo.duoc.cl']
    patron = r'@({})$'.format('|'.join(map(re.escape, dominios_permitidos)))
    match = re.search(patron, correo)
    return bool(match)
