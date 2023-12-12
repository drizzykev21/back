create database radic21$app;
use radic21$app;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL,
    habilitado BOOLEAN NOT NULL DEFAULT false,
    token_validacion VARCHAR(100),
    password VARCHAR(100) NOT NULL,
    rol VARCHAR(20) NOT NULL
);
CREATE TABLE autos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patente VARCHAR(50) UNIQUE NOT NULL,
    capacidad VARCHAR(100) NOT NULL,
    modelo VARCHAR(100) NOT NULL,
    marca VARCHAR(100) NOT NULL,
    usuario_id INT NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);
CREATE TABLE viajes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    inicio VARCHAR(100) NOT NULL,
    destino VARCHAR(100) NOT NULL,
    auto_id INT,
    usuario_id INT NOT NULL,
    tomado BOOLEAN NOT NULL DEFAULT false,
    finalizado BOOLEAN NOT NULL DEFAULT false,
    notificado BOOLEAN NOT NULL DEFAULT false,
    FOREIGN KEY (auto_id) REFERENCES autos(id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);
