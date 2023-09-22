from typing import Optional
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
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from funciones import *
from models import Empresa, Servicio, Usuario, Token
import bcrypt
from str_aleatorio import generar_random_id
from database import get_database
import urllib.parse

SUPER_ADMIN = "SuperAdmin"
ADMIN = "Admin"
datos_usuario = None


app = FastAPI()

# Agregando los archivos estaticos que están en la carpeta dist del proyecto
app.mount("/static", StaticFiles(directory="public/dist"), name="static")

template = Jinja2Templates(directory="public/templates")


@app.get("/", response_class=HTMLResponse)
def login(
    request: Request,
):
    return template.TemplateResponse("login.html", {"request": request})


@app.get("/index", response_class=RedirectResponse)
def inicio(
    request: Request, token: str = Cookie(None), db: Session = Depends(get_database)
):
    if token:
        is_valid = verificar_token(token, db)
        if is_valid:
            usuario = db.query(Usuario).filter(Usuario.id_usuario == is_valid).first()
            return template.TemplateResponse(
                "index.html", {"request": request, "usuario": usuario}
            )
        else:
            return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


# -- 1.1 --
# CENSO


@app.get("/censo", response_class=HTMLResponse)
def pagCenso(
    request: Request, token: str = Cookie(None), db: Session = Depends(get_database)
):
    if token:
        is_token_valid = verificar_token(token, db)  # retorna el id_usuario

        if is_token_valid:
            rol_usuario = get_rol(is_token_valid, db)
            print(rol_usuario)
            if rol_usuario == SUPER_ADMIN or rol_usuario == ADMIN:
                datos_usuario = get_datos_usuario(is_token_valid, db)
                return template.TemplateResponse(
                    "censo.html", {"request": request, "usuario": datos_usuario}
                )
            else:
                alerta = {
                    "mensaje": "No tiene los permisos para esta acción",
                    "color": "warning",
                }
                return template.TemplateResponse(
                    "index.html", {"request": request, "alerta": alerta}
                )
        else:
            return RedirectResponse(url="/", status_code=status.HTTP_403_FORBIDDEN)
    else:
        return RedirectResponse(url="/", status_code=status.HTTP_403_FORBIDDEN)



# CONCEPTOS BASICO


@app.get("/conceptos_basicos", response_class=HTMLResponse)
def pagConceptosBasicos(
    request: Request, token: str = Cookie(None), db: Session = Depends(get_database)
):
    if token:
        is_token_valid = verificar_token(token, db)  # retorna el id_usuario

        if is_token_valid:
            rol_usuario = get_rol(is_token_valid, db)
            print(rol_usuario)
            if rol_usuario == SUPER_ADMIN or rol_usuario == ADMIN:
                datos_usuario = get_datos_usuario(is_token_valid, db)
                return template.TemplateResponse(
                    "conceptos_basicos.html", {"request": request, "usuario": datos_usuario}
                )
            else:
                alerta = {
                    "mensaje": "No tiene los permisos para esta acción",
                    "color": "warning",
                }
                return template.TemplateResponse(
                    "index.html", {"request": request, "alerta": alerta}
                )
        else:
            return RedirectResponse(url="/", status_code=status.HTTP_403_FORBIDDEN)
    else:
        return RedirectResponse(url="/", status_code=status.HTTP_403_FORBIDDEN)


# ESTATUTOS


@app.get("/estatutos", response_class=HTMLResponse)
def pagEstatutos(
    request: Request, token: str = Cookie(None), db: Session = Depends(get_database)
):
    if token:
        is_token_valid = verificar_token(token, db)  # retorna el id_usuario

        if is_token_valid:
            rol_usuario = get_rol(is_token_valid, db)
            print(rol_usuario)
            if rol_usuario == SUPER_ADMIN or rol_usuario == ADMIN:
                datos_usuario = get_datos_usuario(is_token_valid, db)
                return template.TemplateResponse(
                    "estatutos.html", {"request": request, "usuario": datos_usuario}
                )
            else:
                alerta = {
                    "mensaje": "No tiene los permisos para esta acción",
                    "color": "warning",
                }
                return template.TemplateResponse(
                    "index.html", {"request": request, "alerta": alerta}
                )
        else:
            return RedirectResponse(url="/", status_code=status.HTTP_403_FORBIDDEN)
    else:
        return RedirectResponse(url="/", status_code=status.HTTP_403_FORBIDDEN)


# CONTRATO DE CONDICIONES UNIFORME


@app.get("/contrato_condiciones", response_class=HTMLResponse)
def pagContrato_de_condiciones_uniformes(
    request: Request, token: str = Cookie(None), db: Session = Depends(get_database)
):
    if token:
        is_token_valid = verificar_token(token, db)  # retorna el id_usuario

        if is_token_valid:
            rol_usuario = get_rol(is_token_valid, db)
            print(rol_usuario)
            if rol_usuario == SUPER_ADMIN or rol_usuario == ADMIN:
                datos_usuario = get_datos_usuario(is_token_valid, db)
                return template.TemplateResponse(
                    "contrato_condiciones.html", {"request": request, "usuario": datos_usuario}
                )
            else:
                alerta = {
                    "mensaje": "No tiene los permisos para esta acción",
                    "color": "warning",
                }
                return template.TemplateResponse(
                    "index.html", {"request": request, "alerta": alerta}
                )
        else:
            return RedirectResponse(url="/", status_code=status.HTTP_403_FORBIDDEN)
    else:
        return RedirectResponse(url="/", status_code=status.HTTP_403_FORBIDDEN)


# INVITACION A LA ASAMBLEA


@app.get("/invitacion_asamblea", response_class=HTMLResponse)
def pagInvitacion_a_la_asamblea(
    request: Request, token: str = Cookie(None), db: Session = Depends(get_database)
):
    if token:
        is_token_valid = verificar_token(token, db)  # retorna el id_usuario

        if is_token_valid:
            rol_usuario = get_rol(is_token_valid, db)
            print(rol_usuario)
            if rol_usuario == SUPER_ADMIN or rol_usuario == ADMIN:
                datos_usuario = get_datos_usuario(is_token_valid, db)
                return template.TemplateResponse(
                    "invitacion_asamblea.html", {"request": request, "usuario": datos_usuario}
                )
            else:
                alerta = {
                    "mensaje": "No tiene los permisos para esta acción",
                    "color": "warning",
                }
                return template.TemplateResponse(
                    "index.html", {"request": request, "alerta": alerta}
                )
        else:
            return RedirectResponse(url="/", status_code=status.HTTP_403_FORBIDDEN)
    else:
        return RedirectResponse(url="/", status_code=status.HTTP_403_FORBIDDEN)


# FIN 1.1


# -- 1.2 --


# LLAMADO A LISTA
@app.get("/llamado_lista", response_class=HTMLResponse)
def pagLlamado(
    request: Request, token: str = Cookie(None), db: Session = Depends(get_database)
):
    if token:
        is_token_valid = verificar_token(token, db)  # retorna el id_usuario

        if is_token_valid:
            rol_usuario = get_rol(is_token_valid, db)
            print(rol_usuario)
            if rol_usuario == SUPER_ADMIN or rol_usuario == ADMIN:
                datos_usuario = get_datos_usuario(is_token_valid, db)
                return template.TemplateResponse(
                    "llamado_lista.html", {"request": request, "usuario": datos_usuario}
                )
            else:
                alerta = {
                    "mensaje": "No tiene los permisos para esta acción",
                    "color": "warning",
                }
                return template.TemplateResponse(
                    "index.html", {"request": request, "alerta": alerta}
                )
        else:
            return RedirectResponse(url="/", status_code=status.HTTP_403_FORBIDDEN)
    else:
        return RedirectResponse(url="/", status_code=status.HTTP_403_FORBIDDEN)


# VERIFICACION DEL CUORUM


@app.get("/cuorum", response_class=HTMLResponse)
def pagCuorum(
    request: Request, token: str = Cookie(None), db: Session = Depends(get_database)
):
    if token:
        is_token_valid = verificar_token(token, db)  # retorna el id_usuario

        if is_token_valid:
            rol_usuario = get_rol(is_token_valid, db)
            print(rol_usuario)
            if rol_usuario == SUPER_ADMIN or rol_usuario == ADMIN:
                datos_usuario = get_datos_usuario(is_token_valid, db)
                return template.TemplateResponse(
                    "cuorum.html", {"request": request, "usuario": datos_usuario}
                )
            else:
                alerta = {
                    "mensaje": "No tiene los permisos para esta acción",
                    "color": "warning",
                }
                return template.TemplateResponse(
                    "index.html", {"request": request, "alerta": alerta}
                )
        else:
            return RedirectResponse(url="/", status_code=status.HTTP_403_FORBIDDEN)
    else:
        return RedirectResponse(url="/", status_code=status.HTTP_403_FORBIDDEN)


# ORDEN DEL DIA


@app.get("/orden_dia", response_class=HTMLResponse)
def pagOrdenDia(
    request: Request, token: str = Cookie(None), db: Session = Depends(get_database)
):
    if token:
        is_token_valid = verificar_token(token, db)  # retorna el id_usuario

        if is_token_valid:
            rol_usuario = get_rol(is_token_valid, db)
            print(rol_usuario)
            if rol_usuario == SUPER_ADMIN or rol_usuario == ADMIN:
                datos_usuario = get_datos_usuario(is_token_valid, db)
                return template.TemplateResponse(
                    "orden_dia.html", {"request": request, "usuario": datos_usuario}
                )
            else:
                alerta = {
                    "mensaje": "No tiene los permisos para esta acción",
                    "color": "warning",
                }
                return template.TemplateResponse(
                    "index.html", {"request": request, "alerta": alerta}
                )
        else:
            return RedirectResponse(url="/", status_code=status.HTTP_403_FORBIDDEN)
    else:
        return RedirectResponse(url="/", status_code=status.HTTP_403_FORBIDDEN)


# ELECCION A LA COMISION


@app.get("/eleccion_comision", response_class=HTMLResponse)
def pagEleccion(
    request: Request, token: str = Cookie(None), db: Session = Depends(get_database)
):
    if token:
        is_token_valid = verificar_token(token, db)  # retorna el id_usuario

        if is_token_valid:
            rol_usuario = get_rol(is_token_valid, db)
            print(rol_usuario)
            if rol_usuario == SUPER_ADMIN or rol_usuario == ADMIN:
                datos_usuario = get_datos_usuario(is_token_valid, db)
                return template.TemplateResponse(
                    "eleccion_comision.html", {"request": request, "usuario": datos_usuario}
                )
            else:
                alerta = {
                    "mensaje": "No tiene los permisos para esta acción",
                    "color": "warning",
                }
                return template.TemplateResponse(
                    "index.html", {"request": request, "alerta": alerta}
                )
        else:
            return RedirectResponse(url="/", status_code=status.HTTP_403_FORBIDDEN)
    else:
        return RedirectResponse(url="/", status_code=status.HTTP_403_FORBIDDEN)


# APROBACION ESTATUTOS


@app.get("/aprobacion_estatutos", response_class=HTMLResponse)
def pagAprobacion_estatutos(
    request: Request, token: str = Cookie(None), db: Session = Depends(get_database)
):
    if token:
        is_token_valid = verificar_token(token, db)  # retorna el id_usuario

        if is_token_valid:
            rol_usuario = get_rol(is_token_valid, db)
            print(rol_usuario)
            if rol_usuario == SUPER_ADMIN or rol_usuario == ADMIN:
                datos_usuario = get_datos_usuario(is_token_valid, db)
                return template.TemplateResponse(
                    "aprobacion_estatutos.html", {"request": request, "usuario": datos_usuario}
                )
            else:
                alerta = {
                    "mensaje": "No tiene los permisos para esta acción",
                    "color": "warning",
                }
                return template.TemplateResponse(
                    "index.html", {"request": request, "alerta": alerta}
                )
        else:
            return RedirectResponse(url="/", status_code=status.HTTP_403_FORBIDDEN)
    else:
        return RedirectResponse(url="/", status_code=status.HTTP_403_FORBIDDEN)


# ELECCION DE LA JUNTA


@app.get("/eleccion_junta_administradora", response_class=HTMLResponse)
def pagEleccion_junta_administradora(
    request: Request, token: str = Cookie(None), db: Session = Depends(get_database)
):
    if token:
        is_token_valid = verificar_token(token, db)  # retorna el id_usuario

        if is_token_valid:
            rol_usuario = get_rol(is_token_valid, db)
            print(rol_usuario)
            if rol_usuario == SUPER_ADMIN or rol_usuario == ADMIN:
                datos_usuario = get_datos_usuario(is_token_valid, db)
                return template.TemplateResponse(
                    "eleccion_junta_administradora.html", {"request": request, "usuario": datos_usuario}
                )
            else:
                alerta = {
                    "mensaje": "No tiene los permisos para esta acción",
                    "color": "warning",
                }
                return template.TemplateResponse(
                    "index.html", {"request": request, "alerta": alerta}
                )
        else:
            return RedirectResponse(url="/", status_code=status.HTTP_403_FORBIDDEN)
    else:
        return RedirectResponse(url="/", status_code=status.HTTP_403_FORBIDDEN)


# APROBACION DE LA ACTA


@app.get("/aprobacion_acta_constitucion", response_class=HTMLResponse)
def PagAprobacion_acta_constitucion(
    request: Request, token: str = Cookie(None), db: Session = Depends(get_database)
):
    if token:
        is_token_valid = verificar_token(token, db)  # retorna el id_usuario

        if is_token_valid:
            rol_usuario = get_rol(is_token_valid, db)
            print(rol_usuario)
            if rol_usuario == SUPER_ADMIN or rol_usuario == ADMIN:
                datos_usuario = get_datos_usuario(is_token_valid, db)
                return template.TemplateResponse(
                    "aprobacion_acta_constitucion.html", {"request": request, "usuario": datos_usuario}
                )
            else:
                alerta = {
                    "mensaje": "No tiene los permisos para esta acción",
                    "color": "warning",
                }
                return template.TemplateResponse(
                    "index.html", {"request": request, "alerta": alerta}
                )
        else:
            return RedirectResponse(url="/", status_code=status.HTTP_403_FORBIDDEN)
    else:
        return RedirectResponse(url="/", status_code=status.HTTP_403_FORBIDDEN)


# FIN 1.2

@app.get("/archivo_control_documental", response_class=HTMLResponse)
def PagArchivo_control_documental(
    request: Request, token: str = Cookie(None), db: Session = Depends(get_database)
):
    if token:
        is_token_valid = verificar_token(token, db)  # retorna el id_usuario

        if is_token_valid:
            rol_usuario = get_rol(is_token_valid, db)
            print(rol_usuario)
            if rol_usuario == SUPER_ADMIN or rol_usuario == ADMIN:
                datos_usuario = get_datos_usuario(is_token_valid, db)
                return template.TemplateResponse(
                    "archivo_control_documental.html", {"request": request, "usuario": datos_usuario}
                )
            else:
                alerta = {
                    "mensaje": "No tiene los permisos para esta acción",
                    "color": "warning",
                }
                return template.TemplateResponse(
                    "index.html", {"request": request, "alerta": alerta}
                )
        else:
            return RedirectResponse(url="/", status_code=status.HTTP_403_FORBIDDEN)
    else:
        return RedirectResponse(url="/", status_code=status.HTTP_403_FORBIDDEN)


@app.get("/registro_suscriptor", response_class=HTMLResponse)
def PagRegistro_suscriptor(request: Request):
    return template.TemplateResponse("registro_suscriptor.html", {"request": request})


@app.get("/registro_comision", response_class=HTMLResponse)
def PagRegistro_comiSion(request: Request):
    return template.TemplateResponse("registro_comision.html", {"request": request})


# FUNCIONES PARA LA TAREA DE DIEGO
# CREAR USUARIO
@app.get("/form_super_admin", response_class=HTMLResponse)
def PagRegistro_comiSion(request: Request):
    return template.TemplateResponse("addUsuario.html", {"request": request})


# PARA CREAR SUPER ADMIN
@app.post("/crear_super_admin/")
def create_usuario(
    id_usuario: str = Form(...),
    rol: str = Form(...),
    empresa: int = Form(None),
    nom_usuario: str = Form(...),
    apellido_usuario: str = Form(...),
    correo: str = Form(...),
    tipo_doc: str = Form(...),
    num_doc: str = Form(...),
    direccion: str = Form(...),
    municipio: str = Form(...),
    contrasenia: str = Form(...),
    db: Session = Depends(get_database),
):
    # Verificar si el correo electrónico ya está registrado
    existing_user = db.query(Usuario).filter(Usuario.correo == correo).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Correo electrónico ya registrado")

    # Genera un ID de usuario aleatorio
    id_usuario = generar_random_id()

    # Encriptar la contraseña antes de almacenarla
    hashed_password = bcrypt.hashpw(contrasenia.encode("utf-8"), bcrypt.gensalt())

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


# CREAR USUARIOS
# @app.post("/crearUsuario")
# def create_usuario(
#     rol: str = Form(...),
#     empresa: int = Form(None),
#     nom_usuario: str = Form(...),
#     apellido_usuario: str = Form(...),
#     correo: str = Form(...),
#     tipo_doc: str = Form(...),
#     num_doc: str = Form(...),
#     direccion: str = Form(...),
#     municipio: str = Form(...),
#     contrasenia: str = Form(...),
#     token: str = Cookie(None),
#     db: Session = Depends(get_database),
# ):
#     if token:
#         is_valid = verificar_token(token)
#         if is_valid:
#             usuario = db.query(Usuario).filter(Usuario.id_usuario == is_valid).first()
#             if usuario.rol == "Admin":
#                 # Verificar si el correo electrónico ya está registrado
#                 existing_user = (
#                     db.query(Usuario).filter(Usuario.correo == correo).first()
#                 )
#                 if existing_user:
#                     raise HTTPException(
#                         status_code=400, detail="Correo electrónico ya registrado"
#                     )

#                 # Genera un ID de usuario aleatorio
#                 id_usuario = generar_random_id()
#                 user = (
#                     db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
#                 )
#                 if user:
#                     raise HTTPException(
#                         status_code=400, detail="Id de usuario ya Existe"
#                     )

#                 # Encriptar la contraseña antes de almacenarla
#                 hashed_password = bcrypt.hashpw(
#                     contrasenia.encode("utf-8"), bcrypt.gensalt()
#                 )

#                 # Validar y crear el usuario en la base de datos con la contraseña encriptada
#                 usuario_db = Usuario(
#                     id_usuario=id_usuario,
#                     rol=rol,
#                     empresa=empresa,
#                     nom_usuario=nom_usuario,
#                     apellido_usuario=apellido_usuario,
#                     correo=correo,
#                     tipo_doc=tipo_doc,
#                     num_doc=num_doc,
#                     direccion=direccion,
#                     municipio=municipio,
#                     contrasenia=hashed_password.decode(
#                         "utf-8"
#                     ),  # Almacena la contraseña encriptada
#                 )
#                 try:
#                     db.add(usuario_db)
#                     db.commit()
#                     db.refresh(usuario_db)
#                     return {"mensaje": "Usuario creado exitosamente"}
#                 except Exception as e:
#                     db.rollback()  # Realiza un rollback en caso de error para deshacer cambios
#                     raise HTTPException(
#                         status_code=400, detail=f"Error al crear la empresa: {str(e)}"
#                     )
#             return {"mensaje": "Usuario creado exitosamente"}
#         else:
#             raise HTTPException(status_code=401, detail="No autorizado")
#     else:
#         raise HTTPException(status_code=401, detail="No autorizado")


# INICIAR SESION
@app.post("/iniciarSesion", response_class=RedirectResponse)
async def login(
    request: Request,
    email: Optional[str] = Form(""),
    password: Optional[str] = Form(""),
    db: Session = Depends(get_database),
):
    # SI EL FORMULARIO ESTA VACIO
    if not all([email, password]):
        alerta = {
            "mensaje": "Por favor ingrese los datos.",
            "color": "info",
        }
        return template.TemplateResponse("login.html", {"request": request, "alerta": alerta})
        #return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

    usuario = db.query(Usuario).filter(Usuario.correo == email).first()
    if usuario is None:
        alerta = {
            "mensaje": "El correo " + email + " es incorrecto.",
            "color": "danger",
        }
        return template.TemplateResponse("login.html", {"request": request, "alerta": alerta})
        #return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

    if not bcrypt.checkpw(
        password.encode("utf-8"), usuario.contrasenia.encode("utf-8")
    ):
        alerta = {
            "mensaje": "La contraseña es incorrecta.",
            "color": "danger",
        }
        return template.TemplateResponse("login.html", {"request": request, "alerta": alerta})
        #return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

    tokenge = generar_token(usuario.id_usuario)
    token = Token(token=tokenge)
    db.add(token)
    db.commit()

    #datos_usuario = get_datos_usuario(usuario.id_usuario, db)
    # Codificar el diccionario en la URL como un parámetro
    #encoded_usuario = urllib.parse.urlencode(datos_usuario)

    # Construir la URL con el diccionario de usuario codificado
    redirect_url = f"/index"

    template.TemplateResponse(
        "index.html", {"request": request, "usuario": usuario}
    )
    response = RedirectResponse(url=redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="token", value=tokenge)
    return response


# CERRAR SESION
@app.post("/cerrarSesion", response_class=RedirectResponse)
async def una_ruta(token: str = Cookie(None), db: Session = Depends(get_database)):
    if token:
        deleteToken = db.query(Token).filter(Token.token == token).first()
        if deleteToken:
            db.delete(deleteToken)
            db.commit()
            return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
        else:
            return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    else:
        raise HTTPException(status_code=401, detail="No autorizado")


# ACCESO A REGISTRO DE USUARIO
@app.get("/form_registro_usuario", response_class=HTMLResponse)
def get_form_usuario(
    request: Request, token: str = Cookie(None), db: Session = Depends(get_database)
):
    if token:
        is_token_valid = verificar_token(token, db)  # retorna el id_usuario

        if is_token_valid:
            rol_usuario = get_rol(is_token_valid, db)
            print(rol_usuario)
            if rol_usuario == SUPER_ADMIN or rol_usuario == ADMIN:
                datos_usuario = get_datos_usuario(is_token_valid, db)
                return template.TemplateResponse(
                    "registro_usuario.html", {"request": request, "usuario": datos_usuario}
                )
            else:
                alerta = {
                    "mensaje": "No tiene los permisos para esta acción",
                    "color": "warning",
                }
                return template.TemplateResponse(
                    "index.html", {"request": request, "alerta": alerta}
                )
        else:
            return RedirectResponse(url="/", status_code=status.HTTP_403_FORBIDDEN)
    else:
        return RedirectResponse(url="/", status_code=status.HTTP_403_FORBIDDEN)

# Opcion consultar empresa
@app.get("/consultar_empresa", response_class=HTMLResponse)
def consultarEmpresa(request: Request, token: str = Cookie(None), db: Session = Depends(get_database)):

    if token:
        token_valido = verificar_token(token, db)
        if token_valido:
            rol_usuario = get_rol(token_valido, db)
            if rol_usuario == SUPER_ADMIN:
                query_empresas = db.query(Empresa)
                if query_empresas:
                    return template.TemplateResponse("consultar_empresa.html", {"request": request, "empresa": query_empresas})
                else:
                    raise HTTPException(status_code=403, detail="No hay empresas que consultar")
            elif rol_usuario == ADMIN:
                # si se quieren traer varias empresas hay que decirle en lugar de .first() .all()
                query_empresas_admin = db.query(Empresa).join(Usuario, Empresa.id_empresa == Usuario.empresa).all()
                if query_empresas_admin:
                    return template.TemplateResponse("consultar_empresa.html",  {"request": request, "empresa": query_empresas_admin})
                else:
                   raise HTTPException(status_code=403, detail="No hay empresas para consultar")
            else:
                raise HTTPException(status_code=403, detail="No puede entrar")
        else:
            return RedirectResponse(url="/", status_code=status.HTTP_403_FORBIDDEN)
    else:
        return RedirectResponse(url="/", status_code=status.HTTP_403_FORBIDDEN)    

# Opcion consultar Usuario
@app.get("/consultar_usuario", response_class=HTMLResponse)
def consultarUsuario(request: Request, token: str = Cookie(None), db: Session = Depends(get_database)):

    if token:
        token_valido = verificar_token(token, db)
        if token_valido:
            rol_usuario = get_rol(token_valido, db)
            if rol_usuario == SUPER_ADMIN:
                query_usuarios = db.query(Usuario)
                if query_usuarios:
                    return template.TemplateResponse("consultar_usuario.html",  {"request": request, "usuarios": query_usuarios})
                else:
                    raise HTTPException(status_code=403, detail="No hay usuarios para consultar")
            elif rol_usuario == ADMIN:
                usuario = get_datos_usuario(token_valido, db)
                if usuario:
                    print(usuario)
                    # Accediendo a los datos del diccionario que retorna la función de get_datos_usuario
                    id_empresa = usuario.get("empresa")
                    query_usuarios_admin = db.query(Usuario).filter(Usuario.empresa == id_empresa).all()
                    if query_usuarios_admin:
                        return template.TemplateResponse("consultar_usuario.html",  {"request": request, "usuarios": query_usuarios_admin})
                    else:
                        raise HTTPException(status_code=403, detail="No hay usuarios para consultar") 
                else:
                    raise HTTPException(status_code=403, detail="Problemas al momento de consultar el usuario") 
            else:
                raise HTTPException(status_code=403, detail="No cuenta con los permisos") 
        else:
            return RedirectResponse(url="/", status_code=status.HTTP_403_FORBIDDEN)                       
    else:
        return RedirectResponse(url="/", status_code=status.HTTP_403_FORBIDDEN)           


# ACCESO A PERFIL DE USUARIO
@app.get("/perfil_usuario", response_class=HTMLResponse)
def get_perfil_usuario(
    request: Request, token: str = Cookie(None), db: Session = Depends(get_database)
):
    if token:
        is_token_valid = verificar_token(token, db)  # retorna el id_usuario

        if is_token_valid:
            rol_usuario = get_rol(is_token_valid, db)
            print(rol_usuario)
            if rol_usuario == SUPER_ADMIN or rol_usuario == "Admin":
                datos_usuario = get_datos_usuario(is_token_valid, db)
                return template.TemplateResponse(
                    "perfil_usuario.html", {"request": request, "usuario": datos_usuario}
                )
            else:
                alerta = {
                    "mensaje": "No tiene los permisos para esta acción",
                    "color": "warning",
                }
                return template.TemplateResponse(
                    "index.html", {"request": request, "alerta": alerta}
                )
        else:
            return RedirectResponse(url="/", status_code=status.HTTP_403_FORBIDDEN)
    else:
        return RedirectResponse(url="/", status_code=status.HTTP_403_FORBIDDEN)            

# GENERAR DOCUMENTOS PERSONALIZADOS
@app.post("/generar_docx_P01_F_03/")
async def generar_docx_P01_F_03(
    nombre_de_la_asociacion: str = Form(...),
    nit: str = Form(...),
    direccion: str = Form(...),
    municipio: str = Form(...),
    departamento: str = Form(...),
    telefono: str = Form(...),
    web: str = Form(...),
    correo: str = Form(...),
    horario: str = Form(...),
    vereda: str = Form(...),
    sigla: str = Form(...),
    fecha: str = Form(...)
):
    datos = {
        '[Nombre de la Asociación]': nombre_de_la_asociacion,
        '[Campo NIT]': nit,
        '[Campo Dirección]': direccion,
        '[Campo Municipio]': municipio,
        '[Campo Departamento]': departamento,
        '[Campo Teléfonos]': telefono,
        '[Campo Página Web]': web,
        '[Campo Correo]': correo,
        '[Campo Horario Atención]': horario,
        '[SIGLA]': sigla,
        '[Vereda]': vereda,
        '[Municipio]': municipio,
        '[Departamento]': departamento,
        '[Fecha de Constitución]': fecha
    }

    archivo = 'public/dist/ArchivosDescarga/P01-F-03 Estatutos Asociación Suscriptores'
    documento_modificado = reemplazar_texto(archivo, datos)
    documento_modificado.save('P01-F-03 Estatutos Asociación Suscriptores Editado.docx')

    return {"mensaje": "Archivo generado exitosamente!"}

@app.post("/generar_pdf_P01_F_03/")
async def generar_pdf_P01_F_03():
    archivo_docx = 'P01-F-03 Estatutos Asociación Suscriptores Editado.docx'
    archivo_pdf = 'P01-F-03 Estatutos Asociación Suscriptores.pdf'
    convertir_a_pdf(archivo_docx, archivo_pdf)
    return {"mensaje": "Archivo PDF generado exitosamente!"}