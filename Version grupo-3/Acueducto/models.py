from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Float
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
from enum import Enum as PyEnum

Base = declarative_base()


class Empresa(Base):
    __tablename__ = 'empresas'
    id_empresa = Column(Integer, primary_key=True, autoincrement=True)
    nom_empresa = Column(String(50))
    direccion_empresa = Column(String(100))
    tel_fijo = Column(String(10))
    tel_cel = Column(String(10))
    email = Column(String(90))
    estado = Column(Enum('Activo', 'Inactivo'), default='Activo')
    create_at = Column(String, server_default=func.now(), nullable=False)
    update_at = Column(String, server_default=func.now(),
                       onupdate=func.now(), nullable=False)


class Servicio(Base):
    __tablename__ = 'servicios'
    id_servicio = Column(Integer, primary_key=True, autoincrement=True)
    nom_servicio = Column(String(80))
    paso = Column(Float(3, 1))
    modulo = Column(Integer, nullable=False)
    create_at = Column(String, server_default=func.now(), nullable=False)
    update_at = Column(String, server_default=func.now(),
                       onupdate=func.now(), nullable=False)


class Usuario(Base):
    __tablename__ = "usuarios"
    id_usuario = Column(String(30), primary_key=True)
    rol = Column(Enum('SuperAdmin', 'Admin', 'Tecnico', 'Suscriptor'))
    empresa = Column(Integer, nullable=True)
    nom_usuario = Column(String(50))
    apellido_usuario = Column(String(50))
    correo = Column(String(90))
    tipo_doc = Column(Enum('CC', 'CE', 'DNI', 'NIT'))
    num_doc = Column(String(12))
    direccion = Column(String(100))
    municipio = Column(String(50))
    contrasenia = Column(String(180))
    estado = Column(Enum('Activo', 'Inactivo'), default='Activo')


class Token(Base):
    __tablename__ = "tokens"

    id_token = Column(Integer, primary_key=True,
                      autoincrement=True, nullable=False)
    token = Column(String(255), nullable=False)
