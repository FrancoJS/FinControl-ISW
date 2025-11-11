from gestion import models

def crearCuenta(request):
    
    try:
        if request.method == 'POST':
            nombre = request.POST.get('nombre')
            saldo = request.POST.get('saldo')

    except:
        pass