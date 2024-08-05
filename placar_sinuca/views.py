from django.shortcuts import redirect

def index(request):
    return redirect('/operacao/real_time_partidas/')