from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import Partida, Jogador ,Set, ActionHistory, Mesa
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.utils import timezone
from operacao.models import Set
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_datetime

@login_required
def ponto(request, mesa_id):
    mesa = get_object_or_404(Mesa, id=mesa_id)
    return render(request, 'ponto.html', {'mesa': mesa})
@login_required
def placar(request, mesa_id):
    mesa = get_object_or_404(Mesa, id=mesa_id)
    return render(request, 'placar.html', {'mesa': mesa})
def aovivo(request, mesa_id):
    mesa = get_object_or_404(Mesa, id=mesa_id)
    return render(request, 'aovivo.html', {'mesa': mesa})

def tabela(request):
    return render(request, 'tabela.html')

def amistoso(request):
    return render(request, 'amistoso.html')

def start_game(request):
     if request.method == 'POST':
        jogador1_nome = request.POST.get('jogador1')
        jogador2_nome = request.POST.get('jogador2')
        sets = int(request.POST.get('sets'))
        mesa_id = int(request.POST.get('mesa'))
        
        jogador1, created1 = Jogador.objects.get_or_create(nome=jogador1_nome)
        jogador2, created2 = Jogador.objects.get_or_create(nome=jogador2_nome)
        
        mesa = get_object_or_404(Mesa, id=mesa_id)
        
        partida = Partida.objects.create(jogador1=jogador1, jogador2=jogador2, mesa=mesa, melhor_de=sets)
        mesa.partida_atual = partida
        mesa.save()
        return redirect('/operacao/placar/', partida_id=partida.pk)
        return HttpResponseRedirect('/')


def obter_partida_atual(request, mesa_id):
    try:
        mesa = Mesa.objects.get(id=mesa_id)
        partida_atual_id = mesa.partida_atual.id if mesa.partida_atual else None
        return JsonResponse({'partida_id': partida_atual_id})
    except Mesa.DoesNotExist:
        return JsonResponse({'error': 'Mesa não encontrada'}, status=404)


def atualizar_placar(request, mesa_id):
    mesa = Mesa.objects.get(id=mesa_id)
    partida = mesa.partida_atual
    sets_jogador1 = partida.sets.filter(vencedor_id=partida.jogador1_id).count()
    sets_jogador2 = partida.sets.filter(vencedor_id=partida.jogador2_id).count()
    
    ultimo_set = partida.sets.last()  # Obtém o último set da partida

    # Verifica se existe um set e atualiza os dados
    if ultimo_set:
        
        data = {
            'jogador1': partida.jogador1.nome,
            'jogador2': partida.jogador2.nome,
            'melhor_de':partida.melhor_de,
            'sets_jogador1': sets_jogador1,
            'pontos_jogador1': ultimo_set.pontos_jogador1,
            'sets_jogador2': sets_jogador2,
            'pontos_jogador2': ultimo_set.pontos_jogador2,
            'tacada': ultimo_set.tacada
        
        }
    else:
        # Se não houver set, retorna valores padrão
        data = {
            'jogador1': partida.jogador1.nome,
            'jogador2': partida.jogador2.nome,
            'melhor_de': partida.melhor_de,
            'sets_jogador1': 0,
            'pontos_jogador1': 0,
            'sets_jogador2': 0,
            'pontos_jogador2': 0,
            'tacada': 0
        }

    return JsonResponse(data)

def adicionar_pontos(request):
    if request.method == 'POST':
        partida_id = request.POST.get('partida_id')
        player = request.POST.get('player')
        falta = int(request.POST.get('falta'))
        points = int(request.POST.get('points'))

        partida = Partida.objects.get(id=partida_id)
        ultimo_set = partida.sets.last()

        if player == '1':
            ultimo_set.pontos_jogador1 += points
        elif player == '2':
            ultimo_set.pontos_jogador2 += points

        if falta == 0:
            if ultimo_set.tacada is None:
                ultimo_set.tacada = 0
            ultimo_set.tacada += points

        ultimo_set.save()

       
        # Salvar no histórico
        ActionHistory.objects.create(partida=partida, player=player, points=points, falta=falta)

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'failed'})

def desfazer_ultima_acao(request):
    if request.method == 'POST':
        partida_id = request.POST.get('partida_id')
        
        partida = Partida.objects.get(id=partida_id)
        ultimo_set = partida.sets.last()

        # Obter a última ação do histórico
        ultima_acao = ActionHistory.objects.filter(partida=partida).last()
        
        if ultima_acao:
            if str(ultima_acao.player) == "1":
                novo_pontos_jogador1 = max(ultimo_set.pontos_jogador1 - ultima_acao.points, 0)
                ultimo_set.pontos_jogador1 = novo_pontos_jogador1
            elif str(ultima_acao.player) == "2":
                novo_pontos_jogador2 = max(ultimo_set.pontos_jogador2 - ultima_acao.points, 0)
                ultimo_set.pontos_jogador2 = novo_pontos_jogador2
            else:
                return JsonResponse({'status': 'failed', 'message': 'Jogador inválido na última ação'})

            if ultima_acao.falta == 0:
                current_break_points = max(ultimo_set.tacada - ultima_acao.points, 0)
                ultimo_set.tacada = current_break_points  # Atualizar a coluna tacada
            else:
                current_break_points = ultimo_set.tacada

            ultimo_set.save()
            ultima_acao.delete()  # Remover a ação do histórico

            return JsonResponse({'status': 'success', 'currentBreakPoints': current_break_points})
    
    return JsonResponse({'status': 'failed'})

def reset_tacada(request):
    if request.method == 'POST':
        partida_id = request.POST.get('partida_id')
        
        try:
            partida = Partida.objects.get(id=partida_id)
            ultimo_set = partida.sets.last()
            if ultimo_set:
                ultimo_set.tacada = 0
                ultimo_set.save()
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'failed', 'message': 'Set não encontrado'})
        except Partida.DoesNotExist:
            return JsonResponse({'status': 'failed', 'message': 'Partida não encontrada'})

    return JsonResponse({'status': 'failed'})

def encerrar_frame(request):
    if request.method == 'POST':
        partida_id = request.POST.get('partida_id')
        partida = Partida.objects.get(id=partida_id)
        
        ultimo_set = partida.sets.last()
        
        if ultimo_set.pontos_jogador1 > ultimo_set.pontos_jogador2:
            ultimo_set.vencedor = partida.jogador1
        elif ultimo_set.pontos_jogador2 > ultimo_set.pontos_jogador1:
            ultimo_set.vencedor = partida.jogador2
        ultimo_set.save()

        sets_jogador1 = partida.sets.filter(vencedor_id=partida.jogador1_id).count()
        sets_jogador2 = partida.sets.filter(vencedor_id=partida.jogador2_id).count()

        # Verifica se algum jogador alcançou a quantidade necessária de sets para vencer a partida
        if sets_jogador1 > partida.melhor_de // 2:
            partida.vencedor = partida.jogador1
        elif sets_jogador2 > partida.melhor_de // 2:
            partida.vencedor = partida.jogador2

        # Cria um novo set se a partida não tiver vencedor e a quantidade total de sets for menor que melhor_de
        if not partida.vencedor and (sets_jogador1 + sets_jogador2) < partida.melhor_de:
            novo_set = Set(partida=partida, numero_set=ultimo_set.numero_set + 1)
            novo_set.save()
        
        partida.save()
        
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'})

@login_required
def cadastrar_partida(request):
    if request.method == 'POST':
        data_partida_str = request.POST.get('data_partida')
        jogador1_nome = request.POST.get('jogador1')
        jogador2_nome = request.POST.get('jogador2')
        sets_str = request.POST.get('sets')

        if not data_partida_str or not jogador1_nome or not jogador2_nome or not sets_str:
            return render(request, 'cadastrar_partida.html', {'error': 'Todos os campos são obrigatórios.'})

        data_partida = parse_datetime(data_partida_str)
        if not data_partida:
            return render(request, 'cadastrar_partida.html', {'error': 'Data e hora inválidas.'})

        try:
            sets = int(sets_str)
        except ValueError:
            return render(request, 'cadastrar_partida.html', {'error': 'Quantidade de sets inválida.'})

        jogador1, created1 = Jogador.objects.get_or_create(nome=jogador1_nome)
        jogador2, created2 = Jogador.objects.get_or_create(nome=jogador2_nome)

        partida = Partida(
            data_partida=data_partida,
            jogador1=jogador1,
            jogador2=jogador2,
            melhor_de=sets
        )
        partida.save()
        return redirect('lista_partidas')

    return render(request, 'cadastrar_partida.html')

@login_required
def lista_partidas(request):
    partidas = Partida.objects.all()
    return render(request, 'lista_partidas.html', {'partidas': partidas})

@login_required
def editar_partida(request, partida_id):
    partida = get_object_or_404(Partida, id=partida_id)

    if request.method == 'POST':
        jogador1_nome = request.POST.get('jogador1')
        jogador2_nome = request.POST.get('jogador2')
        sets = int(request.POST.get('sets'))

        jogador1, created1 = Jogador.objects.get_or_create(nome=jogador1_nome)
        jogador2, created2 = Jogador.objects.get_or_create(nome=jogador2_nome)

        partida.jogador1 = jogador1
        partida.jogador2 = jogador2
        partida.melhor_de = sets
        partida.save()

        return redirect('lista_partidas') 

    return render(request, 'editar_partida.html', {'partida': partida})
@login_required
def excluir_partida(request, partida_id):
    if request.method == 'POST':
        partida = get_object_or_404(Partida, id=partida_id)
        partida.delete()
        return redirect('lista_partidas')
@login_required        
def zerar_partida(request, partida_id):
    partida = get_object_or_404(Partida, id=partida_id)
    
    # Zerar todos os sets
    sets = partida.sets.all()
    sets.delete()
    novo_set = Set(partida=partida, numero_set=1)
    novo_set.save()
    for set in sets:
        set.pontos_jogador1 = 0
        set.pontos_jogador2 = 0
        set.faltas_jogador1 = 0
        set.faltas_jogador2 = 0
        set.save()

    # Resetar o vencedor e outros campos da partida
    partida.vencedor_id = None
    partida.save()

    return redirect('lista_partidas') 

@login_required
def lista_mesas(request):
    mesas = Mesa.objects.all().prefetch_related('partidas', 'partida_atual')
    return render(request, 'lista_mesas.html', {'mesas': mesas})
@login_required
def adicionar_mesa(request):
    if request.method == 'POST':
        ultimo_id = Mesa.objects.all().order_by('id').last().id if Mesa.objects.exists() else 0
        Mesa.objects.create(id=ultimo_id + 1)  
        return redirect('lista_mesas')  


def remover_mesa(request):
    if request.method == 'POST':
        ultima_mesa = Mesa.objects.all().order_by('id').last()
        if ultima_mesa:
            # Desassocia a partida atual da mesa antes de deletar a mesa
            if ultima_mesa.partida_atual:
                ultima_mesa.partida_atual.mesa = None
                ultima_mesa.partida_atual.save()
            ultima_mesa.delete()
        return redirect('lista_mesas')
    return redirect('lista_mesas')  # Adiciona um redirecionamento para o caso de o método não ser POST


@login_required
def editar_mesa(request, mesa_id):
    mesa = get_object_or_404(Mesa, id=mesa_id)
    if request.method == 'POST':
        mesa.link_transmissao = request.POST.get('link_transmissao')
        partida_atual_id = request.POST.get('partida_atual')
        
        if partida_atual_id:
            partida_atual = get_object_or_404(Partida, id=partida_atual_id)
            
            # Desassociar a partida atual anterior, se existir
            if mesa.partida_atual and mesa.partida_atual != partida_atual:
                partida_atual_anterior = mesa.partida_atual
                partida_atual_anterior.mesa = None
                partida_atual_anterior.save()
                
            # Associar a nova partida à mesa
            mesa.partida_atual = partida_atual
            partida_atual.mesa = mesa
            partida_atual.save()
        else:
            # Se partida_atual_id estiver vazio, defina partida_atual como None e desassocie a mesa da partida atual
            if mesa.partida_atual:
                partida_atual_anterior = mesa.partida_atual
                partida_atual_anterior.mesa = None
                partida_atual_anterior.save()
            mesa.partida_atual = None
        
        mesa.save()
        return redirect('lista_mesas')
    else:
        partidas = Partida.objects.filter(mesa__isnull=True) | Partida.objects.filter(id=mesa.partida_atual_id)
        return render(request, 'editar_mesa.html', {'mesa': mesa, 'partidas': partidas})


def real_time_partidas(request):
    return render(request, 'real_time_partidas.html')

def atualizar_realtime_partidas(request):
    partidas = Partida.objects.filter(mesa__isnull=False).select_related('jogador1', 'jogador2', 'mesa')
    partidas_data = []

    for partida in partidas:
        sets_jogador1 = partida.sets.filter(vencedor_id=partida.jogador1_id).count()
        sets_jogador2 = partida.sets.filter(vencedor_id=partida.jogador2_id).count()
        ultimo_set = partida.sets.last()
        
        if ultimo_set:
            pontos_jogador1 = ultimo_set.pontos_jogador1
            pontos_jogador2 = ultimo_set.pontos_jogador2
        else:
            pontos_jogador1 = 0
            pontos_jogador2 = 0

        partidas_data.append({
            'mesa_id': partida.mesa.id,
            'jogador1': partida.jogador1.nome,
            'jogador2': partida.jogador2.nome,
            'pontos_jogador1': pontos_jogador1,
            'sets_jogador1': sets_jogador1,
            'pontos_jogador2': pontos_jogador2,
            'sets_jogador2': sets_jogador2,
            'melhor_de': partida.melhor_de,
            'vencedor': partida.vencedor.nome if partida.vencedor else None,
            'link_transmissao': partida.mesa.link_transmissao
        })

    return JsonResponse({'partidas': partidas_data})