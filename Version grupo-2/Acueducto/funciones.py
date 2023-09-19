# FUNCION GENERAR TOKEN
from datetime import datetime, timedelta
from jose import jwt
from models import Token, Usuario

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
        usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
        if usuario:
            return usuario.rol
        else:
            return None
    else:
        return None


# FUNCION PARA OBTENER LOS DATOS DE USUARIO
def get_datos_usuario(id_usuario, db):
    if id_usuario:
        usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
        if usuario:
            datos_usuario = {
                "id_usuario": usuario.id_usuario,
                "nom_usuario": usuario.nom_usuario,
                "apellido_usuario": usuario.apellido_usuario,
                "num_doc": usuario.num_doc,
                "direccion": usuario.direccion,
                "municipio": usuario.municipio,
                "rol": usuario.rol,
                "empresa": usuario.empresa,
                "correo": usuario.correo
                # Agrega otros campos del usuario
            }
            return datos_usuario
        else:
            return None
    else:
        return None