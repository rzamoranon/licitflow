from django.http import HttpResponse

def index(request):
    return HttpResponse("Gestor de documentos funcionando")