
from fastapi import HTTPException, Depends, Cookie, Response
import bcrypt
from str_aleatorio import generar_random_id
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

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
from fastapi.responses import JSONResponse, RedirectResponse

from sqlalchemy.orm import Session
from funciones import *
from models import Usuario

SUPER_ADMIN = "SuperAdmin"
ADMIN = "Admin"
ESTADO = "Activo"


app = FastAPI()

# Agregando los archivos estaticos que están en la carpeta dist del proyecto
app.mount("/static", StaticFiles(directory="public/dist"), name="static")

template = Jinja2Templates(directory="public/templates")

def actualizarPerfil(
        nom_usuario: str,
        apellido_usuario: str,
        tipo_doc: str,
        num_doc: str,
        email: str,
        direccion: str ,
        token: str ,
        db: Session
    ):
    
    if not nom_usuario:
        raise HTTPException(status_code=400, detail="El nombre es requerido")
    
    if not apellido_usuario:
        raise HTTPException(status_code=400, detail="El apellido es requerido")
    
    if not tipo_doc:
        raise HTTPException(status_code=400, detail="El tipo de documento es requerido")
    
    if not num_doc:
        raise HTTPException(status_code=400, detail="El número de documento es requerido")
    
    if not email:
        raise HTTPException(status_code=400, detail="El correo electrónico es requerido")
    
    if not direccion:
        raise HTTPException(status_code=400, detail="La dirección es requerida")
    
    if not nom_usuario or not apellido_usuario or not tipo_doc or not num_doc or not email or not direccion:
        raise HTTPException(status_code=400, detail="Todos los campos son requeridos")
    
    if token:
        token_valido = verificar_token(token, db)
        if token_valido:
            usuario = db.query(Usuario).filter(Usuario.id_usuario == token_valido).first()
            if usuario:
                # Validar si alguno de los campos está vacío o lleno de espacios

                usuario.nom_usuario = nom_usuario
                usuario.apellido_usuario = apellido_usuario
                usuario.tipo_doc = tipo_doc
                usuario.num_doc = num_doc
                usuario.correo = email 
                usuario.direccion = direccion
                
                db.commit() 

                # Redireccionar al perfil actualizado
                return RedirectResponse(url="/perfil_usuario", status_code=status.HTTP_303_SEE_OTHER)
            else:
                raise HTTPException(status_code=403, detail="No puede entrar")
        else:
            return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    


def cambiarEstadoUsuario(
        id_usuario: str, 
        token: str , 
        db: Session):
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
            usuario_a_cambiar = db.query(Usuario).filter_by(
                id_usuario=id_usuario).first()
            if not usuario_a_cambiar:
                raise HTTPException(
                    status_code=404, detail="Usuario no encontrado")

            # CAMBIAR ESTADO ACTIVO O INACTIVO
            nuevoEstado = 'Inactivo'
            if usuario_a_cambiar.estado == 'Inactivo':
                nuevoEstado = 'Activo'

            usuario_a_cambiar.estado = nuevoEstado
            db.commit()

            return {"exitoso": "Estado del usuario cambiado a 'Inactivo' correctamente"}
        else:
            raise HTTPException(
                status_code=403, detail="Token no proporcionado")
    except Exception as e:
        # Captura cualquier error inesperado
        return JSONResponse(status_code=500, content={"error": f"Error interno: {str(e)}"})
    

def actualizarUsuario(

    id_usuario: str,
    nom_usuario: str,
    apellido_usuario: str,
    tipo_doc: str,
    num_doc: str,
    correo: str,
    municipio: str,
    direccion: str,
    estado: str,
    token: str,
    db: Session,
):
    
    
    if token:
        token_valido = verificar_token(token, db)

        if token_valido:
            rol_usuario = get_rol(token_valido, db)

            if rol_usuario in [SUPER_ADMIN, ADMIN]:
                usuario_actualizar = db.query(
                    Usuario).filter_by(id_usuario=id_usuario).first()

                if usuario_actualizar:
                    
                    # Actualiza los campos con los nuevos valores
                    usuario_actualizar.nom_usuario = nom_usuario
                    usuario_actualizar.apellido_usuario = apellido_usuario
                    usuario_actualizar.correo = correo
                    usuario_actualizar.direccion = direccion
                    usuario_actualizar.municipio = municipio
                    usuario_actualizar.estado = estado
                    usuario_actualizar.tipo_doc = tipo_doc
                    # Guarda los cambios en la base de datos
                    db.commit()
                    # Compara los valores actuales con los nuevos valores
                    
                    
                    return RedirectResponse(url="/usuarios", status_code=status.HTTP_303_SEE_OTHER)
                    

                else:
                    
                    return RedirectResponse(url="/usuarios", status_code=status.HTTP_303_SEE_OTHER)
        else:

            return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    else:

        return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    



def createUsuario(
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
    token: str ,
    db: Session,
    
):

    empresa_existente = db.query(Empresa).filter(
        Empresa.id_empresa == empresa).first()
    if not empresa_existente:
        """         alerta = {
            "mensaje": "La empresa seleccionada, no existe.",
            "color": "danger",
        }
        return RedirectResponse(url="/form_registro_usuario", status_code=status.HTTP_303_SEE_OTHER, alerta=alerta) """
        return
    campos = ['correo', 'num_doc']
    valores = [correo, num_doc]
    if verificar_existencia(campos, valores, db):
        return

    if token:
        is_valid = verificar_token(token, db)
        if is_valid:
            usuario = db.query(Usuario).filter(
                Usuario.id_usuario == is_valid).first()
            if usuario.rol in [SUPER_ADMIN, ADMIN]:
                # Verificar si el correo electronico ya está registrado
                existing_user = db.query(Usuario).filter(
                    Usuario.correo == correo).first()
                if existing_user:
                    return {"error": "Usuario ya existe"}

                verificar_documento = db.query(Usuario).filter(
                    Usuario.num_doc == num_doc).first()
                if verificar_documento:
                    return {"no exitoso": "documento ya existente"}

                # Genera un ID de usuario aleatorio
                id_usuario = generar_random_id()
                user = (
                    db.query(Usuario).filter(
                        Usuario.id_usuario == id_usuario).first()
                )
                if user:
                    raise HTTPException(
                        status_code=400, detail="Id de usuario ya Existe"
                    )
                # Encriptar la contraseña antes de almacenarla
                hashed_password = bcrypt.hashpw(
                    contrasenia.encode("utf-8"), bcrypt.gensalt()
                )
                # Validar y crear el usuario en la base de datos con la contrasena encriptada
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
                try:
                    db.add(usuario_db)
                    db.commit()
                    db.refresh(usuario_db)
                    
                    #falta mostra el mensaje para cuando se almacene correctamnete el usuario
                    """ alerta = {
                        "mensaje": "creado correctamente",
                        "color": "success",
                    } """
                   
                    return RedirectResponse(url="/form_registro_usuario", status_code=status.HTTP_303_SEE_OTHER)
                except Exception as e:
                    db.rollback()  # Realiza un rollback en caso de error para deshacer cambios
                    return {"mensaje": e}
            return {"mensaje": "Usuario creado exitosamente"}
        else:
            raise HTTPException(status_code=401, detail="No autorizado")
    else:
        raise HTTPException(status_code=401, detail="No autorizado")
    

def verificar_existencia(campos, valores, db):
    query = db.query(Usuario)
    for campo, valor in zip(campos, valores):
        query = query.filter(getattr(Usuario, campo) == valor)
    return db.query(query.exists()).scalar()


def consultarUsuarios(
    request: Request, token: str , db: Session
):
    if token:
        token_valido = verificar_token(token, db)
        if token_valido:
            rol_usuario = get_rol(token_valido, db)
            usuario = (
                db.query(Usuario).filter(Usuario.id_usuario == token_valido).first()
            )
            headers = elimimar_cache()
            if rol_usuario in [SUPER_ADMIN, ADMIN]:
                if rol_usuario == SUPER_ADMIN:
                    query_usuarios = db.query(Usuario, Empresa.nom_empresa).join(
                        Empresa, Usuario.empresa == Empresa.id_empresa
                    ).filter(Usuario.id_usuario != token_valido)
                if rol_usuario == ADMIN:
                    query_usuarios = (
                        db.query(Usuario, Empresa.nom_empresa)
                        .join(Empresa, Usuario.empresa == Empresa.id_empresa)
                        .filter(
                            (Usuario.id_usuario != token_valido)
                            & (Usuario.rol != SUPER_ADMIN )
                            & (Usuario.empresa == usuario.empresa)
                        )
                    )
                if query_usuarios.all():
                    print(query_usuarios)

                    response = template.TemplateResponse(
                        "crud-usuarios/consultar_usuario.html",
                        {
                            "request": request,
                            "usuarios": query_usuarios,
                            "usuario": usuario,
                        },
                    )
                    response.headers.update(headers)
                    return response
                else:
                    raise HTTPException(
                        status_code=403, detail="No hay usuarios para consultar"
                    )
            else:
                raise HTTPException(
                    status_code=403, detail="No cuenta con los permisos"
                )
        else:
            return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


def EditarUsuarios(
    request: Request,
    id_usuario: str,
    token: str,
    db: Session,
):
    if token:
        token_valido = verificar_token(token, db)
        if token_valido:
            rol_usuario = get_rol(token_valido, db)
            usuario = (
                db.query(Usuario).filter(Usuario.id_usuario == token_valido).first()
            )
            headers = elimimar_cache()
            if rol_usuario in [SUPER_ADMIN, ADMIN]:
                user = get_datos_usuario(id_usuario, db)
                response = template.TemplateResponse(
                    "crud-usuarios/EditarUsuario.html",
                    {"request": request, "user": user, "usuario": usuario},
                )
                response.headers.update(headers)
                return response
    raise HTTPException(status_code=403, detail="No tiene los permisos necesarios")


def getPerfilUsuario(
    request: Request, token: str, db: Session
):
    if token:
        is_token_valid = verificar_token(token, db)  # retorna el id_usuario
        datos_usuario = get_datos_usuario(is_token_valid, db)
        headers = elimimar_cache()
        if is_token_valid:
            rol_usuario = get_rol(is_token_valid, db)

            if rol_usuario:
                response = template.TemplateResponse(
                    "crud-usuarios/perfil_usuario.html",
                    {"request": request, "usuario": datos_usuario},
                )
                response.headers.update(headers)
                return response
            else:
                alerta = {
                    "mensaje": "No tiene los permisos para esta acción",
                    "color": "warning",
                }

                response = template.TemplateResponse(
                    "index.html",
                    {"request": request, "alerta": alerta, "usuario": datos_usuario},
                )
                response.headers.update(headers)
                return response
        else:
            return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    

def EditarUsuarioPerfil(
    request: Request,
    id_usuario: str,
    token: str,
    db: Session,
):
    usuario = get_datos_usuario(id_usuario, db)
    headers = elimimar_cache()
    if token:
        token_valido = verificar_token(token, db)
        if token_valido:
            response = template.TemplateResponse(
                "crud-usuarios/perfil_usuario.html",
                {"request": request, "usuario": usuario},
            )
            response.headers.update(headers)
            return response
    raise HTTPException(status_code=403, detail="Ha ocurrido un error.")

def get_formUsuario(
    request: Request, token: str, db: Session
):
    if token:
        is_token_valid = verificar_token(token, db)  # retorna el id_usuario

        if is_token_valid:
            rol_usuario = get_rol(is_token_valid, db)
            print(rol_usuario)
            headers = elimimar_cache()
            datos_usuario = get_datos_usuario(is_token_valid, db)
            if rol_usuario == SUPER_ADMIN:
                empresas = db.query(Empresa).filter(Empresa.estado == 'Activo').all()
                response = template.TemplateResponse(
                    "crud-usuarios/registro_usuario.html",
                    {
                        "request": request,
                        "usuario": datos_usuario,
                        "empresas": empresas,
                    },
                )
                response.headers.update(headers)
                return response
            elif rol_usuario == ADMIN:
                id_empresa_user = get_empresa(is_token_valid,db)
                empresa = db.query(Empresa).filter_by(id_empresa=id_empresa_user).scalar()
                response = template.TemplateResponse(
                    "crud-usuarios/registro_usuario.html",
                    {
                        "request": request,
                        "usuario": datos_usuario,
                        "empresa": empresa,
                    },
                )
                response.headers.update(headers)
                return response
            else:
                alerta = {
                    "mensaje": "No tiene los permisos para esta accion",
                    "color": "warning",
                }
                response = template.TemplateResponse(
                    "index.html",
                    {"request": request, "alerta": alerta, "usuario": datos_usuario},
                )
                response.headers.update(headers)
                return response

        else:
            return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)