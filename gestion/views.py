from django.shortcuts import render
from gestion.servicios import cuentas

def landing_page(request):
    return render(request, 'landing-page/landing.html')

def cuenta_page(request):
    lista_cuentas = cuentas.obtener_cuentas()

    lista = {
        "cuentas": lista_cuentas
    }
    return render(request, 'cuenta/cuenta-page.html', lista)

def crear_cuenta(request):
    resultado = {}
    if request.method == 'POST':
        respuesta = cuentas.crear_cuenta(request)

        if respuesta["success"] == False:
            resultado["success"] = False
            resultado["mensaje"] = respuesta["mensaje"]
        else:
            resultado["success"] = True
            resultado["mensaje"] = respuesta["mensaje"]

        resultado["cuentas"] = cuentas.obtener_cuentas()

        return render(request, 'cuenta/cuenta-page.html', resultado)
    else:
        resultado["cuentas"] = cuentas.obtener_cuentas()
        return render(request, 'cuenta/cuenta-page.html', resultado)


