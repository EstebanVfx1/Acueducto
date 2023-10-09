from fastapi import HTTPException, Depends, Cookie, Response
from fastapi import HTTPException
import bcrypt
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from str_aleatorio import generar_random_id
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
SUPER_ADMIN = "SuperAdmin"
datos_usuario = None

app = FastAPI()

# Agregando los archivos estaticos que están en la carpeta dist del proyecto
app.mount("/static", StaticFiles(directory="public/dist"), name="static")

template = Jinja2Templates(directory="public/templates")


def generarDocx_P01_F_03(
    request: Request, 
    token: str, 
    db: Session,
    nombre_de_la_asociacion: str,
    nit: str,
    direccion: str,
    municipio: str,
    departamento: str,
    telefono: str,
    web: str,
    correo: str,
    horario: str,
    vereda: str,
    sigla: str,
    fecha: str,
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
        '[Dirección]': direccion,
        '[Vereda]': vereda,
        '[Municipio]': municipio,
        '[Departamento]': departamento,
        '[Fecha de Constitución]': fecha
    }

    archivo = 'public/dist/ArchivosDescarga/P01-F-03 Estatutos Asociación Suscriptores.docx'
    documento_modificado = reemplazar_texto(archivo, datos)
    documento_modificado.save('public/dist/ArchivosDescarga/P01-F-03 Estatutos Asociación Suscriptores Editado.docx')

    archivo_docx = 'public/dist/ArchivosDescarga/P01-F-03 Estatutos Asociación Suscriptores Editado.docx'
    archivo_pdf = 'public/dist/ArchivosDescarga/P01-F-03 Estatutos Asociación Suscriptores.pdf'
    convertir_a_pdf(archivo_docx, archivo_pdf)

    if token:
        is_token_valid = verificar_token(token, db)  # retorna el id_usuario

        if is_token_valid:
            rol_usuario = get_rol(is_token_valid, db)
            print(rol_usuario)
            headers = elimimar_cache()
            datos_usuario = get_datos_usuario(is_token_valid, db)
            if rol_usuario == SUPER_ADMIN or rol_usuario == "Admin":
                
                response = template.TemplateResponse(
                    "archivo_control_documental.html", {"request": request, "usuario": datos_usuario}
                )
                response.headers.update(headers)  # Actualiza las cabeceras
                return response
            else:
                alerta = {
                    "mensaje": "No tiene los permisos para esta acción",
                    "color": "warning",
                }
                response = template.TemplateResponse(
                    "index.html", {"request": request, "alerta": alerta,"usuario": datos_usuario}
                )
                response.headers.update(headers)  # Actualiza las cabeceras
                return response
        else:
            return RedirectResponse(url="/", status_code=status.HTTP_403_FORBIDDEN)
    else:
        return RedirectResponse(url="/", status_code=status.HTTP_403_FORBIDDEN)