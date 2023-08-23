from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Agregando los archivos estaticos que están en la carpeta dist del proyecto
app.mount("/static", StaticFiles(directory="public/dist"), name="static")

template = Jinja2Templates(directory='public/templates')


@app.get("/loging", response_class=HTMLResponse)
def login(request: Request):
    return template.TemplateResponse('loging.html', {"request": request})


@app.get("/", response_class=HTMLResponse)
def inicio(request: Request):
    return template.TemplateResponse('index.html', {"request": request})

# -- 1.1 --
# CENSO


@app.get("/censo", response_class=HTMLResponse)
def pagCenso(request: Request):
    return template.TemplateResponse('censo.html', {"request": request})

# CONCEPTOS BASICO


@app.get("/conceptos_basicos", response_class=HTMLResponse)
def pagConceptosBasicos(request: Request):
    return template.TemplateResponse('conceptos_basicos.html', {"request": request})

# ESTATUTOS


@app.get("/estatutos", response_class=HTMLResponse)
def pagEstatutos(request: Request):
    return template.TemplateResponse('estatutos.html', {"request": request})

# CONTRATO DE CONDICIONES UNIFORME


@app.get("/contrato_condiciones", response_class=HTMLResponse)
def pagContrato_de_condiciones_uniformes(request: Request):
    return template.TemplateResponse('contrato_condiciones.html', {"request": request})

# INVITACION A LA ASAMBLEA


@app.get("/invitacion_asamblea", response_class=HTMLResponse)
def pagInvitacion_a_la_asamblea(request: Request):
    return template.TemplateResponse('invitacion_asamblea.html', {"request": request})


# FIN 1.1


# -- 1.2 --

# LLAMADO A LISTA
@app.get("/llamado_lista", response_class=HTMLResponse)
def pagLlamado(request: Request):
    return template.TemplateResponse("llamado_lista.html", {"request": request})

# VERIFICACION DEL CUORUM


@app.get("/cuorum", response_class=HTMLResponse)
def pagCuorum(request: Request):
    return template.TemplateResponse("cuorum.html", {"request": request})

# ORDEN DEL DIA


@app.get("/orden_dia", response_class=HTMLResponse)
def pagOrdenDia(request: Request):
    return template.TemplateResponse("orden_dia.html", {"request": request})

# ELECCION A LA COMISION


@app.get("/eleccion_comision", response_class=HTMLResponse)
def pagEleccion(request: Request):
    return template.TemplateResponse("eleccion_comision.html", {"request": request})

# APROBACION ESTATUTOS


@app.get("/aprobacion_estatutos", response_class=HTMLResponse)
def pagAprobacion_estatutos(request: Request):
    return template.TemplateResponse("aprobacion_estatutos.html", {"request": request})

# ELECCION DE LA JUNTA


@app.get("/eleccion_junta_administradora", response_class=HTMLResponse)
def pagEleccion_junta_administradora(request: Request):
    return template.TemplateResponse("eleccion_junta_administradora.html", {"request": request})

# APROBACION DE LA ACTA


@app.get("/aprobacion_acta_constitucion", response_class=HTMLResponse)
def PagAprobacion_acta_constitucion(request: Request):
    return template.TemplateResponse("aprobacion_acta_constitucion.html", {"request": request})


# FIN 1.2


@app.get("/registro_suscriptor", response_class=HTMLResponse)
def PagRegistro_suscriptor(request: Request):
    return template.TemplateResponse("registro_suscriptor.html", {"request": request})


@app.get("/registro_comision", response_class=HTMLResponse)
def PagRegistro_comiSion(request: Request):
    return template.TemplateResponse("registro_comision.html", {"request": request})
