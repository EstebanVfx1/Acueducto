from fastapi import HTTPException, Depends, Cookie, Response
from fastapi import HTTPException
from typing import Optional
from cruds.EmpresasCrud import *
from cruds.UsuariosCrud import *
from cruds.SuperAdmin import *
from pdfs.P01_F_03 import *
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
from sqlalchemy.orm import Session, joinedload
from funciones import *
from models import Empresa, Servicio, Usuario, Token
import bcrypt
from database import get_database
from funciones import get_datos_empresa


SUPER_ADMIN = "SuperAdmin"
ADMIN = "Admin"
ESTADO = "Activo"
datos_usuario = None

app = FastAPI()

# Agregando los archivos estaticos que están en la carpeta dist del proyecto
app.mount("/static", StaticFiles(directory="public/dist"), name="static")

template = Jinja2Templates(directory="public/templates")


@app.get("/", response_class=HTMLResponse)
def login(request: Request):
    headers = elimimar_cache()
    # return template.TemplateResponse("login.html", {"request": request})
    response = template.TemplateResponse("login.html", {"request": request})
    response.headers.update(headers)  # Actualiza las cabeceras
    return response


@app.get("/index", response_class=RedirectResponse)
def inicio(
    request: Request, token: str = Cookie(None), db: Session = Depends(get_database)
):
    if token:
        is_valid = verificar_token(token, db)
        if is_valid:
            usuario = db.query(Usuario).filter(Usuario.id_usuario == is_valid).first()
            headers = elimimar_cache()

            response = template.TemplateResponse(
                "index.html", {"request": request, "usuario": usuario}
            )
            response.headers.update(headers)  # Actualiza las cabeceras
            return response
        else:
            return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

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
            datos_usuario = get_datos_usuario(is_token_valid, db)
            headers = elimimar_cache()
            if rol_usuario == SUPER_ADMIN or rol_usuario == ADMIN:
                response = template.TemplateResponse(
                    "paso-1/paso1-1/censo.html",
                    {"request": request, "usuario": datos_usuario},
                )
                response.headers.update(headers)  # Actualiza las cabeceras
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
                response.headers.update(headers)  # Actualiza las cabeceras
                return response

        else:
            return RedirectResponse(url="/index", status_code=status.HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


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
            datos_usuario = get_datos_usuario(is_token_valid, db)
            headers = elimimar_cache()
            if rol_usuario == SUPER_ADMIN or rol_usuario == ADMIN:
                response = template.TemplateResponse(
                    "paso-1/paso1-1/conceptos_basicos.html",
                    {"request": request, "usuario": datos_usuario},
                )
                response.headers.update(headers)  # Actualiza las cabeceras
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
                response.headers.update(headers)  # Actualiza las cabeceras
                return response
        else:
            return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


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
            datos_usuario = get_datos_usuario(is_token_valid, db)
            headers = elimimar_cache()
            if rol_usuario == SUPER_ADMIN or rol_usuario == ADMIN:
                response = template.TemplateResponse(
                    "paso-1/paso1-1/estatutos.html",
                    {"request": request, "usuario": datos_usuario},
                )
                response.headers.update(headers)  # Actualiza las cabeceras
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
                response.headers.update(headers)  # Actualiza las cabeceras
                return response
        else:
            return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


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
            datos_usuario = get_datos_usuario(is_token_valid, db)
            headers = elimimar_cache()
            if rol_usuario == SUPER_ADMIN or rol_usuario == ADMIN:
                response = template.TemplateResponse(
                    "paso-1/paso1-1/contrato_condiciones.html",
                    {"request": request, "usuario": datos_usuario},
                )
                response.headers.update(headers)  # Actualiza las cabeceras
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
                response.headers.update(headers)  # Actualiza las cabeceras
                return response
        else:
            return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


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
            datos_usuario = get_datos_usuario(is_token_valid, db)
            headers = elimimar_cache()
            if rol_usuario == SUPER_ADMIN or rol_usuario == ADMIN:
                response = template.TemplateResponse(
                    "paso-1/paso1-1/invitacion_asamblea.html",
                    {"request": request, "usuario": datos_usuario},
                )
                response.headers.update(headers)  # Actualiza las cabeceras
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
                response.headers.update(headers)  # Actualiza las cabeceras
                return response
        else:
            return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


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
            datos_usuario = get_datos_usuario(is_token_valid, db)
            headers = elimimar_cache()
            if rol_usuario == SUPER_ADMIN or rol_usuario == ADMIN:
                response = template.TemplateResponse(
                    "paso-1/paso1-2/llamado_lista.html",
                    {"request": request, "usuario": datos_usuario},
                )
                response.headers.update(headers)  # Actualiza las cabeceras
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
                response.headers.update(headers)  # Actualiza las cabeceras
                return response
        else:
            return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


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
            datos_usuario = get_datos_usuario(is_token_valid, db)
            headers = elimimar_cache()
            if rol_usuario == SUPER_ADMIN or rol_usuario == ADMIN:
                response = template.TemplateResponse(
                    "paso-1/paso1-2/cuorum.html",
                    {"request": request, "usuario": datos_usuario},
                )
                response.headers.update(headers)  # Actualiza las cabeceras
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
                response.headers.update(headers)  # Actualiza las cabeceras
                return response
        else:
            return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


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
            datos_usuario = get_datos_usuario(is_token_valid, db)
            headers = elimimar_cache()
            if rol_usuario == SUPER_ADMIN or rol_usuario == ADMIN:
                response = template.TemplateResponse(
                    "paso-1/paso1-2/orden_dia.html",
                    {"request": request, "usuario": datos_usuario},
                )
                response.headers.update(headers)  # Actualiza las cabeceras
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
                response.headers.update(headers)  # Actualiza las cabeceras
                return response
        else:
            return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


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
            datos_usuario = get_datos_usuario(is_token_valid, db)
            headers = elimimar_cache()
            if rol_usuario == SUPER_ADMIN or rol_usuario == ADMIN:
                response = template.TemplateResponse(
                    "paso-1/paso1-2/eleccion_comision.html",
                    {"request": request, "usuario": datos_usuario},
                )
                response.headers.update(headers)  # Actualiza las cabeceras
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
                response.headers.update(headers)  # Actualiza las cabeceras
                return response
        else:
            return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


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
            datos_usuario = get_datos_usuario(is_token_valid, db)
            headers = elimimar_cache()
            if rol_usuario == SUPER_ADMIN or rol_usuario == ADMIN:
                response = template.TemplateResponse(
                    "paso-1/paso1-2/aprobacion_estatutos.html",
                    {"request": request, "usuario": datos_usuario},
                )
                response.headers.update(headers)  # Actualiza las cabeceras
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
                response.headers.update(headers)  # Actualiza las cabeceras
                return response
        else:
            return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


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
            datos_usuario = get_datos_usuario(is_token_valid, db)
            headers = elimimar_cache()
            if rol_usuario == SUPER_ADMIN or rol_usuario == ADMIN:
                response = template.TemplateResponse(
                    "paso-1/paso1-2/eleccion_junta_administradora.html",
                    {"request": request, "usuario": datos_usuario},
                )
                response.headers.update(headers)  # Actualiza las cabeceras
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
                response.headers.update(headers)  # Actualiza las cabeceras
                return response
        else:
            return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


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
            datos_usuario = get_datos_usuario(is_token_valid, db)
            headers = elimimar_cache()
            if rol_usuario == SUPER_ADMIN or rol_usuario == ADMIN:
                response = template.TemplateResponse(
                    "paso-1/paso1-2/aprobacion_acta_constitucion.html",
                    {"request": request, "usuario": datos_usuario},
                )
                response.headers.update(headers)  # Actualiza las cabeceras
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
                response.headers.update(headers)  # Actualiza las cabeceras
                return response
        else:
            return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


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
            datos_usuario = get_datos_usuario(is_token_valid, db)
            headers = elimimar_cache()
            if rol_usuario == SUPER_ADMIN or rol_usuario == ADMIN:
                response = template.TemplateResponse(
                    "paso-1/paso1-3/archivo_control_documental.html",
                    {"request": request, "usuario": datos_usuario},
                )
                response.headers.update(headers)  # Actualiza las cabeceras
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
                response.headers.update(headers)  # Actualiza las cabeceras
                return response
        else:
            return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/registro_suscriptor", response_class=HTMLResponse)
def PagRegistro_suscriptor(request: Request):
    headers = elimimar_cache()
    response = template.TemplateResponse(
        "registro_suscriptor.html", {"request": request}
    )
    response.headers.update(headers)
    return response


@app.get("/registro_comision", response_class=HTMLResponse)
def PagRegistro_comiSion(request: Request):
    headers = elimimar_cache()
    response = template.TemplateResponse("registro_comision.html", {"request": request})
    response.headers.update(headers)
    return response


# FUNCIONES PARA LA TAREA DE DIEGO
# CREAR USUARIO
@app.get("/form_super_admin", response_class=HTMLResponse)
def PagRegistro_comiSion(request: Request):
    headers = elimimar_cache()
    response = template.TemplateResponse(
        "crud-usuarios/addUsuario.html", {"request": request}
    )
    response.headers.update(headers)
    return response


# PARA CREAR SUPER ADMIN
@app.post("/crear_super_admin/")
def create_super_admin(
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
    respuesta = createSuper_admin(
        id_usuario,
        rol,
        empresa,
        nom_usuario,
        apellido_usuario,
        correo,
        tipo_doc,
        num_doc,
        direccion,
        municipio,
        contrasenia,
        db,
    )
    return respuesta


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
        return template.TemplateResponse(
            "login.html", {"request": request, "alerta": alerta}
        )
        # return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

    usuario = db.query(Usuario).filter(Usuario.correo == email).first()
    if usuario is None:
        alerta = {
            "mensaje": "El correo " + email + " es incorrecto.",
            "color": "danger",
        }
        return template.TemplateResponse(
            "login.html", {"request": request, "alerta": alerta}
        )
        # return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

    # EN CASO QUE EL USUARIO ESTE INACTIVO
    if usuario.estado == "Inactivo":
        alerta = {
            "mensaje": "El usuario " + email + " está inactivo.",
            "color": "warning",
        }
        return template.TemplateResponse(
            "login.html", {"request": request, "alerta": alerta}
        )

    if not bcrypt.checkpw(
        password.encode("utf-8"), usuario.contrasenia.encode("utf-8")
    ):
        alerta = {
            "mensaje": "La contraseña es incorrecta.",
            "color": "danger",
        }
        return template.TemplateResponse(
            "login.html", {"request": request, "alerta": alerta}
        )
        # return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

    tokenge = generar_token(usuario.id_usuario)
    token = Token(token=tokenge)
    db.add(token)
    db.commit()

    # datos_usuario = get_datos_usuario(usuario.id_usuario, db)
    # Codificar el diccionario en la URL como un parametro
    # encoded_usuario = urllib.parse.urlencode(datos_usuario)

    # Construir la URL con el diccionario de usuario codificado
    redirect_url = f"/index"

    template.TemplateResponse("index.html", {"request": request, "usuario": usuario})
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


# GENERAR DOCUMENTOS PERSONALIZADOS
@app.post("/generar_docx_P01_F_03/")
def generar_docx_P01_F_03(
    request: Request,
    token: str = Cookie(None),
    db: Session = Depends(get_database),
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
    fecha: str = Form(...),
):
    respuesta = generarDocx_P01_F_03(
        request,
        token,
        db,
        nombre_de_la_asociacion,
        nit,
        direccion,
        municipio,
        departamento,
        telefono,
        web,
        correo,
        horario,
        vereda,
        sigla,
        fecha,
    )
    return respuesta


# Otras importaciones necesarias (como SUPER_ADMIN, ADMIN, Usuario, verificar_token, get_rol, get_database, etc.)

# =============================================== BLOQUE PARA LA CREACION DEL USUARIO ===============================================


# --- FUNCION PARA DAR ACCESO AL REGISTRO DEL USUARIO
@app.get("/form_registro_usuario", response_class=HTMLResponse)
def get_form_usuario(
    request: Request, token: str = Cookie(None), db: Session = Depends(get_database)
):
    respuesta = get_formUsuario(request,token,db)
    return respuesta


# --- FUNCION PARA LA CREACION DE USUARIOS
@app.post("/crearUser")
def create_usuario(
    rol: str = Form(...),
    empresa: int = Form(...),
    nom_usuario: str = Form(...),
    apellido_usuario: str = Form(...),
    correo: str = Form(...),
    tipo_doc: str = Form(...),
    num_doc: str = Form(...),
    direccion: str = Form(...),
    municipio: str = Form(...),
    contrasenia: str = Form(...),
    token: str = Cookie(None),
    db: Session = Depends(get_database),
):
    respuesta = createUsuario(
        rol,
        empresa,
        nom_usuario,
        apellido_usuario,
        correo,
        tipo_doc,
        num_doc,
        direccion,
        municipio,
        contrasenia,
        token,
        db,
    )
    return respuesta


# --- FUNCION PARA VERIFICAR CAMPOS EN LA CREACION DE USUARIOS


# =============================================== FIN DEL BLOQUE DE LA CREACION DEL USUARIO ===============================================


# =============================================== BLOQUE USUARIOS(GENERAL) ===============================================


# --- FUNCION PARA MOSTRAR TODOS LOS USUARIOS(GENERAL)
@app.get("/usuarios", response_class=HTMLResponse)
def consultarUsuario(
    request: Request, token: str = Cookie(None), db: Session = Depends(get_database)
):
    respuesta = consultarUsuarios(request,token,db)
    return respuesta


# --- FUNCION PARA MOSTRAR LA PAGINA DONDE SE EDITA EL USUARIO(GENERAL)
@app.post("/EditarUsuarios/", response_class=HTMLResponse)
def Editar_Usuarios(
    request: Request,
    id_usuario: str = Form(...),
    token: str = Cookie(None),
    db: Session = Depends(get_database),
):
    respuesta = EditarUsuarios(request,id_usuario,token,db)
    return respuesta


# --- FUNCION PARA ACTUALIZAR EL USUARIO(GENERAL)
@app.post("/updateUser/")
def updateUser(
    id_usuario: str = Form(...),
    nom_usuario: str = Form(...),
    apellido_usuario: str = Form(...),
    tipo_doc: str = Form(...),
    num_doc: str = Form(...),
    correo: str = Form(...),
    municipio: str = Form(...),
    direccion: str = Form(...),
    estado: str = Form(...),
    token: str = Cookie(None),
    db: Session = Depends(get_database),
):
    respuesta = actualizarUsuario(
        id_usuario,
        nom_usuario,
        apellido_usuario,
        tipo_doc,
        num_doc,
        correo,
        municipio,
        direccion,
        estado,
        token,
        db,
    )
    return respuesta


# ---FUNCION PARA CAMBIAR EL ESTADO DEL USUARIO EN EL TABLA
@app.post("/CambiarEstadoUsuario/{id_usuario}")
def cambiar_estado_usuario(
    id_usuario: str, token: str = Cookie(None), db: Session = Depends(get_database)
):
    respuesta = cambiarEstadoUsuario(id_usuario, token, db)
    return respuesta


# =============================================== FIN BLOQUE USUARIOS(GENERAL) ===============================================


# ============================================ BLOQUE PARA EL PERFIL DEL USUARIO(PERSONAL) ============================================


# --- MOSTRAMOS PAGINA CON EL ACCESO AL PERFIL DEL USUARIO(PERSONAL)
@app.get("/perfil_usuario", response_class=HTMLResponse)
def get_perfil_usuario(
    request: Request, token: str = Cookie(None), db: Session = Depends(get_database)
):
    respuesta = getPerfilUsuario(request,token,db)
    return respuesta


# --- RUTA PARA QUE EL USUARIO PUEDA VER SU INFORMACION PERSONAL DESDE EL PERFIL
@app.post("/EditarUsuario/", response_class=HTMLResponse)
def Editar_Usuario(
    request: Request,
    id_usuario: str = Form(...),
    token: str = Cookie(None),
    db: Session = Depends(get_database),
):
    respuesta = EditarUsuarioPerfil(request,id_usuario,token,db)
    return respuesta


# --- FUNCI0N PARA ACTUALIZAR LOS DATOS DEL PERFIL (PERSONAL):
@app.post("/actualizarPerfil")
def actualizar_perfil(
    nom_usuario: str = Form(...),
    apellido_usuario: str = Form(...),
    tipo_doc: str = Form(...),
    num_doc: str = Form(...),
    email: str = Form(...),
    direccion: str = Form(...),
    token: str = Cookie(None),
    db: Session = Depends(get_database),
):
    respuesta = actualizarPerfil(
        nom_usuario, apellido_usuario, tipo_doc, num_doc, email, direccion, token, db
    )
    return respuesta


# ============================================ FIN DE BLOQUE DEL PERFIL DEL USUARIO(PERSONAL) ============================================


# ============================================= BLOQUE PARA CREACION DE EMPRESA =============================================


# --- MOSTRAMOS LA PAGINA PARA REGISTRAR UNA EMPRESA
@app.get("/registro_empresa", response_class=HTMLResponse)
def MostrarRegistroEmpresa(
    request: Request, token: str = Cookie(None), db: Session = Depends(get_database)
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
                response = template.TemplateResponse(
                    "crud-empresas/registro_empresa.html",
                    {"request": request, "usuario": usuario},
                )
                response.headers.update(headers)
                return response

            else:
                raise HTTPException(
                    status_code=403,
                    detail="NO TIENES LOS PERMISOS PARA ACCEDER A ESTA PAGINA ",
                )
        else:
            return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


# --- CREAMOS UNA EMPRESA
@app.post("/registrarEmpresa")
def crearEmpresa(
    nom_empresa: str = Form(...),
    direccion_empresa: str = Form(...),
    tel_fijo: str = Form(...),
    tel_cel: str = Form(...),
    email: str = Form(...),
    token: str = Cookie(None),
    db: Session = Depends(get_database),
):
    respuesta = insertarEmpresa(
        nom_empresa, direccion_empresa, tel_fijo, tel_cel, email, token, db
    )
    return respuesta


# ============================================= FIN DE BLOQUE DE CREACION DE EMPRESA =============================================


# =============================================- BLOQUE PARA ACTUALIZAR EMPRESAS =============================================-


# --- FUNCION PARA MOSTRAR TODAS LA EMPRESAS
@app.get("/empresas", response_class=HTMLResponse)
def consultarEmpresas(
    request: Request, token: str = Cookie(None), db: Session = Depends(get_database)
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
                query_empresas = db.query(Empresa)
                if query_empresas:
                    response = template.TemplateResponse(
                        "crud-empresas/consultar_empresa.html",
                        {
                            "request": request,
                            "empresa": query_empresas,
                            "usuario": usuario,
                        },
                    )
                    response.headers.update(headers)
                    return response
                else:
                    raise HTTPException(
                        status_code=403, detail="No hay empresas que consultar"
                    )
            else:
                raise HTTPException(status_code=403, detail="No puede entrar")
        else:
            return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


# --- FUNCION PARA CAMBIAR EL ESTADO DE LA EMPRESA
@app.post("/CambiarEstadoEmpresa/{id_empresa}")
def cambiar_estado_empresa(
    id_empresa: int, token: str = Cookie(None), db: Session = Depends(get_database)
):
    respuesta = cambiarEstadoEmpresa(id_empresa, token, db)
    return respuesta


# --- RUTA PARA MOSTRAR LA PAGUNA DONDE SE EDITA LA EMPRESA
@app.post("/EditarEmpresa/", response_class=HTMLResponse)
def Editar_Empresas(
    request: Request,
    id_empresa: int = Form(...),
    token: str = Cookie(None),
    db: Session = Depends(get_database),
):
    if token:
        token_valido = verificar_token(token, db)
        if token_valido:
            rol_usuario = get_rol(token_valido, db)
            usuario = (
                db.query(Usuario).filter(Usuario.id_usuario == token_valido).first()
            )
            headers = elimimar_cache()
            if rol_usuario == SUPER_ADMIN or rol_usuario == ADMIN:
                empresa = get_datos_empresa(id_empresa, db)
                response = template.TemplateResponse(
                    "crud-empresas/EditarEmpresa.html",
                    {"request": request, "empresa": empresa, "usuario": usuario},
                )
                response.headers.update(headers)
                return response
            else:
                raise HTTPException(status_code=403, detail="No puede entrar")
        else:
            return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


# --- FUNCION PARA ACTUALIZAR LA EMPRESA
@app.post("/updateEmpresa")
def obtenerDatos(
    id_empresa: int = Form(...),
    nom_empresa: str = Form(...),
    tel_fijo: str = Form(...),
    tel_cel: str = Form(...),
    email: str = Form(...),
    estado: str = Form(...),
    token: str = Cookie(None),
    db: Session = Depends(get_database),
):
    respuesta = updateEmpresa(
        id_empresa, nom_empresa, tel_fijo, tel_cel, email, estado, token, db
    )
    if respuesta:
        return RedirectResponse("/empresas", status_code=status.HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


# ============================================= FIN DE BLOQUE PARA ACTUALIZAR EMPRESA =============================================
