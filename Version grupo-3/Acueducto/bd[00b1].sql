DROP DATABASE IF EXISTS acueducto;

CREATE DATABASE acueducto CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE acueducto;

CREATE TABLE empresas(
    id_empresa INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nom_empresa VARCHAR(50),
    direccion_empresa VARCHAR(100),
    tel_fijo CHAR(10),
    tel_cel CHAR(10),
    email VARCHAR(90),
    estado enum('Activo', 'Inactivo') DEFAULT 'Activo',
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE usuarios(
    id_usuario CHAR(30) PRIMARY KEY, 
    rol ENUM ('SuperAdmin', 'Admin', 'Tecnico', 'Suscriptor'),
    empresa INT UNSIGNED,
    nom_usuario VARCHAR(50),
    apellido_usuario VARCHAR(50),
    correo VARCHAR(90),
    tipo_doc ENUM ('CC', 'CE','DNI', 'NIT'),
    num_doc CHAR(12),
    direccion VARCHAR(100),
    municipio VARCHAR (50),
    contrasenia VARCHAR (180),
    estado enum('Activo', 'Inactivo') DEFAULT 'Activo',
    FOREIGN KEY (empresa) REFERENCES empresas (id_empresa),
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE inmuebles_suscritor(
    id_inmueble INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_usuario CHAR(30),
    direccion VARCHAR(100),
    estrato ENUM('1','2','3','4','5','6'),
    uso ENUM('Doméstico','Industrial','Institucional','Comercial','Agropecuario'),
    numero_residentes TINYINT UNSIGNED,
    FOREIGN KEY (id_usuario) REFERENCES usuarios (id_usuario),
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE servicios(
    id_servicio INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nom_servicio VARCHAR(80),
    paso FLOAT(3,1),
    modulo TINYINT UNSIGNED,
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE documentos(
    id_doc CHAR(30),
    id_usuario CHAR(30),
    nom_doc VARCHAR(80),
    id_servicio INT UNSIGNED,
    tipo ENUM('pdf', 'docx', 'xlsx'),
    FOREIGN KEY (id_usuario) REFERENCES usuarios (id_usuario),
    FOREIGN KEY (id_servicio) REFERENCES servicios (id_servicio),
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE trazabilidad(
    id_trazabilidad INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_empresa INT UNSIGNED,
    id_servicio INT UNSIGNED,
    estado ENUM('Pendiente', 'En proceso', 'Finalizado'),
    FOREIGN KEY (id_empresa) REFERENCES empresas (id_empresa),
    FOREIGN KEY (id_servicio) REFERENCES servicios (id_servicio),
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



CREATE TABLE tokens(
    id_token INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    token VARCHAR(255),
    
)
    
