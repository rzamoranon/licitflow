from django.http import HttpResponse

def index(request):
    return HttpResponse("Módulo de oportunidades funcionando")