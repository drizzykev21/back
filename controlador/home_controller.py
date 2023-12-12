from flask import jsonify


def saludar():
    return jsonify({'mensaje':'Bienvenido a tellevoApp'})