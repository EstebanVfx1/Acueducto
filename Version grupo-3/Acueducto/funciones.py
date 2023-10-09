# FUNCION GENERAR TOKEN
from datetime import datetime, timedelta
from jose import jwt
from docx import Document
from fpdf import FPDF
from models import Token, Usuario, Empresa
from docx2pdf import convert
import PyPDF2

SECRET_KEY = "sd45g4f45SWFGVHHuoyiad4F5SFD65V4SFDVOJWNHACUfwghdfvcguDCwfghezxhAzAKHGFBJYTFdkjfghtjkdgb"


def generar_token(usuario_id: str):
    expiration = datetime.utcnow() + timedelta(hours=1)  # Token expira en 1 hora
    payload = {"sub": usuario_id, "exp": expiration}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

# FUNCION VERIFICAR TOKEN


def verificar_token(token: str, db):
    if token is None:
        return None
    consultar = db.query(Token).filter(Token.token == token).first()
    if consultar:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms="HS256")
            return payload.get("sub")
        except jwt.ExpiredSignatureError:  # Token ha expirado
            deleteToken = db.query(Token).filter(Token.token == token).first()
            if deleteToken:
                db.delete(deleteToken)
                db.commit()
            return None
        except jwt.JWTError:  # Token inválido
            return None
    else:  # Token no válido
        return None


# FUNCION PARA OBTENER EL ROL DE USUARIO
def get_rol(id_usuario, db):
    if id_usuario:
        usuario = db.query(Usuario).filter(
            Usuario.id_usuario == id_usuario).first()
        if usuario:
            return usuario.rol
        else:
            return None
    else:
        return None
    
# FUNCION PARA OBTENER LA EMPRESA DEL USUARIO
def get_empresa(id_usuario, db):
    if id_usuario:
        usuario = db.query(Usuario).filter(
            Usuario.id_usuario == id_usuario).first()
        if usuario:
            return usuario.empresa
        else:
            return None
    else:
        return None


# FUNCION PARA OBTENER LOS DATOS DE USUARIO
def get_datos_usuario(id_usuario, db):
    if id_usuario:
        usuario = db.query(Usuario).filter(
            Usuario.id_usuario == id_usuario).first()
        if usuario:
            datos_usuario = {
                "id_usuario": usuario.id_usuario,
                "nom_usuario": usuario.nom_usuario,
                "apellido_usuario": usuario.apellido_usuario,
                "num_doc": usuario.num_doc,
                "direccion": usuario.direccion,
                "municipio": usuario.municipio,
                "rol": usuario.rol,
                "estado": usuario.estado,
                "empresa": usuario.empresa,
                "correo": usuario.correo
                # Agrega otros campos del usuario
            }
            return datos_usuario
        else:
            return None
    else:
        return None

# CAMBIAR LOS CAMPOS "[]" POR VALORES DE FORMULARIO
def reemplazar_texto(docx_path, datos):
    document = Document(docx_path)
    
    for paragraph in document.paragraphs:
        for campo, valor in datos.items():
            if campo in paragraph.text:
                paragraph.text = paragraph.text.replace(campo, valor)

    return document

# CONVIERTE EL DOCUMENTO DOCX A PDF
def convertir_a_pdf(docx_path, pdf_path):
    try:
        # Llama a la función convert para convertir el documento DOCX a PDF
        convert(docx_path, pdf_path)
        return True  # La conversión fue exitosa
    except Exception as e:
        print(f"Error al convertir a PDF: {str(e)}")
        return False  # Ocurrió un error durante la conversión


# OBTENER DATOS EMPRESA:
def get_datos_empresa(id_empresa, db):
    if id_empresa:
        empresa = db.query(Empresa).filter(
            Empresa.id_empresa == id_empresa).first()
        if empresa:
            datos_empresa = {
                "id_empresa": empresa.id_empresa,
                "nom_empresa": empresa.nom_empresa,
                "tel_fijo": empresa.tel_fijo,
                "tel_cel": empresa.tel_cel,
                "email": empresa.email,
                "estado": empresa.estado,
            }
            return datos_empresa
        else:
            return None
    else:
        return None


# OBTERNER DATOS EMPRESA (TODAS LAS REGISTRADAS):

def get_datos_empresas(db) -> list[str]:
    nom_empresas = db.query(Empresa.nom_empresa).all()
    return [nombre[0] for nombre in nom_empresas]


#FUNCION PARA ELIMINAR EL CACHE (HEADERS) 4/10/2023

def elimimar_cache():
    headers = {
        "Cache-Control": "no-store, must-revalidate",
        "Pragma": "no-cache",
    }
    return headers