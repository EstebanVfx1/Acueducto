from fastapi import HTTPException, Depends, Cookie, Response
from fastapi import HTTPException
from fastapi import (
    FastAPI,
    Request,
    Form,
    status,
    Depends,
    HTTPException,
    Cookie,
    Query,
)
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session
from funciones import *
from models import Empresa



SUPER_ADMIN = "SuperAdmin"
ADMIN = "Admin"
ESTADO = "Activo"

def updateEmpresa(
    id_empresa: int ,
    nom_empresa: str,
    tel_fijo: str,
    tel_cel: str,
    email: str,
    estado: str, 
    token: str,
    db: Session,
):
    
    if not nom_empresa:
        raise HTTPException(status_code=400, detail="El nombre es requerido")
    
    if not tel_fijo:
        raise HTTPException(status_code=400, detail="El telefono fijo es requerido")
    
    if not tel_cel:
        raise HTTPException(status_code=400, detail="El telefono celular es requerido")
    
    if not email:
        raise HTTPException(status_code=400, detail="El correo es requerido")
    
    if not nom_empresa or not tel_fijo or not tel_cel or not email:
        raise HTTPException(status_code=400, detail="Todos los campos son requeridos")

    
    if token:
        token_valido = verificar_token(token, db)
        if token_valido:
            rol_usuario = get_rol(token_valido, db)

            if rol_usuario in [SUPER_ADMIN, ADMIN]:
                update_empresa = db.query(Empresa).filter_by(
                    id_empresa=id_empresa).first()

                if update_empresa:
                    update_empresa.nom_empresa = nom_empresa
                    update_empresa.tel_fijo = tel_fijo
                    update_empresa.tel_cel = tel_cel
                    update_empresa.email = email
                    update_empresa.estado = estado
                    db.commit()
                    return True
                else:
                    raise HTTPException(
                        status_code=404, detail="Empresa no encontrada")
            else:
                raise HTTPException(
                    status_code=403, detail="No tienes permisos para actualizar empresas")
        else:
            return False
    else:
        return False
    

def insertarEmpresa(
    nom_empresa: str,
    direccion_empresa: str,
    tel_fijo: str,
    tel_cel: str,
    email: str ,
    token: str,
    db: Session,
):
    # Verificar si todos los campos fueron proporcionados
    if not nom_empresa or not direccion_empresa or not tel_fijo or not tel_cel or not email:
        raise HTTPException(status_code=400, detail="Todos los campos son requeridos")

    # Verificar si se proporciona un token válido en las cookies
    if token:
        is_valid = verificar_token(token, db)
        if is_valid:
            usuario = db.query(Usuario).filter(Usuario.id_usuario == is_valid).first()
            print(usuario.rol)
            if usuario.rol in [SUPER_ADMIN, ADMIN]:
                # Verificar si el correo electrónico de la empresa ya está registrado
                existing_correo = db.query(Empresa).filter(Empresa.email == email).first()

                # Verificar si el nombre de la empresa ya está registrado
                existing_nombre = db.query(Empresa).filter(Empresa.nom_empresa == nom_empresa).first()

                if existing_correo:
                    raise HTTPException(status_code=400, detail="Correo de la empresa ya registrado")

                if existing_nombre:
                    raise HTTPException(status_code=400, detail="Nombre de la empresa ya registrado")

                # Crear una instancia de la clase Empresa
                empresa_db = Empresa(
                    nom_empresa=nom_empresa,
                    direccion_empresa=direccion_empresa,
                    tel_fijo=tel_fijo,
                    tel_cel=tel_cel,
                    email=email
                )

                try:
                    db.add(empresa_db)
                    db.commit()
                    db.refresh(empresa_db)
                    return JSONResponse(status_code=201, content={"mensaje": "Empresa creada exitosamente"})
                except Exception as e:
                    db.rollback()
                    raise HTTPException(status_code=500, detail="Error al registrar la empresa")
            else:
                raise HTTPException(status_code=401, detail="No TIENE LOS PERMISOS")
        else:
            raise HTTPException(status_code=401, detail="No autorizado")
    else:
        raise HTTPException(status_code=401, detail="No autorizado")
    



def cambiarEstadoEmpresa(
        id_empresa: int, 
        token: str ,
        db: Session,
    ):
    try:
        # Comprueba si hay un token
        if token:
            # Verifica la validez del token
            token_valido = verificar_token(token, db)
            if not token_valido:
                raise HTTPException(status_code=403, detail="Token inválido")

            # Obtiene el rol del usuario a partir del token
            rol_usuario = get_rol(token_valido, db)

            # Validar que Super admin y admin puedan cambiar el estado
            if rol_usuario not in {SUPER_ADMIN, ADMIN}:
                raise HTTPException(
                    status_code=403, detail="No cuenta con los permisos para cambiar el estado")

            # Cambia el estado del usuario a "Inactivo"
            empresa_a_cambiar = db.query(Empresa).filter_by(
                id_empresa=id_empresa).first()
            if not empresa_a_cambiar:
                raise HTTPException(
                    status_code=404, detail="Empresa no encontrada")

            empresa_a_cambiar.estado = "Inactivo"
            db.commit()

            return {"exitoso": "Estado de la empresa cambiado a 'Inactivo' correctamente"}
        else:
            raise HTTPException(
                status_code=403, detail="Token no proporcionado")
    except Exception as e:
        # Captura cualquier error inesperado
        return JSONResponse(status_code=500, content={"error": f"Error interno: {str(e)}"})
    