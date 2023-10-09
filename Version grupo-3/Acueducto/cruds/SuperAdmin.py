
from fastapi import HTTPException
import bcrypt
from str_aleatorio import generar_random_id
from sqlalchemy.orm import Session
from funciones import *
from models import Usuario


def createSuper_admin(
    id_usuario: str,
    rol: str,
    empresa: int,
    nom_usuario: str,
    apellido_usuario: str,
    correo: str,
    tipo_doc: str,
    num_doc: str,
    direccion: str,
    municipio: str,
    contrasenia: str,
    db: Session,
):
    # Verificar si el correo electrónico ya está registrado
    existing_user = db.query(Usuario).filter(Usuario.correo == correo).first()
    if existing_user:
        raise HTTPException(
            status_code=400, detail="Correo electrónico ya registrado")

    # Genera un ID de usuario aleatorio
    id_usuario = generar_random_id()

    # Encriptar la contraseña antes de almacenarla
    hashed_password = bcrypt.hashpw(
        contrasenia.encode("utf-8"), bcrypt.gensalt())

    usuario_db = Usuario(
        id_usuario=id_usuario,
        rol=rol,
        empresa=empresa,
        nom_usuario=nom_usuario,
        apellido_usuario=apellido_usuario,
        correo=correo,
        tipo_doc=tipo_doc,
        num_doc=num_doc,
        direccion=direccion,
        municipio=municipio,
        contrasenia=hashed_password.decode(
            "utf-8"
        ),  # Almacena la contraseña encriptada
    )
    db.add(usuario_db)
    db.commit()
    db.refresh(usuario_db)
    return {"mensaje": "Super Admin creado exitosamente"}