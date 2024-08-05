from django.urls import path, re_path
from . import views, consumers

urlpatterns = [
    path('ponto/<int:mesa_id>/', views.ponto, name='ponto'),  
    path('placar/<int:mesa_id>/', views.placar, name='placar'),
    path('lista_mesas', views.lista_mesas, name='lista_mesas'),
    path('adicionar_mesa/', views.adicionar_mesa, name='adicionar_mesa'),
    path('remover_mesa', views.remover_mesa, name='remover_mesa'),
    path('editar_mesa/<int:mesa_id>/', views.editar_mesa, name='editar_mesa'),  
    path('aovivo/<int:mesa_id>/', views.aovivo, name='aovivo'),
    path('tabela/', views.tabela, name='tabela'),  
    path('amistoso/', views.amistoso, name='amistoso'),  
    path('start_game/', views.start_game, name='start_game'),
    path('atualizar_placar/<int:mesa_id>/', views.atualizar_placar, name='atualizar_placar'),
    path('adicionar_pontos/', views.adicionar_pontos, name='adicionar_pontos'),
    path('desfazer_ultima_acao/', views.desfazer_ultima_acao, name='desfazer_ultima_acao'),
    path('reset_tacada/', views.reset_tacada, name='reset_tacada'),
    path('encerrar_frame/', views.encerrar_frame, name='encerrar_frame'),
    path('cadastrar_partida/', views.cadastrar_partida, name='cadastrar_partida'),
    path('lista_partidas/', views.lista_partidas, name='lista_partidas'),
    path('editar_partida/<int:partida_id>/', views.editar_partida, name='editar_partida'),
    path('excluir_partida/<int:partida_id>/', views.excluir_partida, name='excluir_partida'),
    path('zerar_partida/<int:partida_id>/', views.zerar_partida, name='zerar_partida'),
    path('obter_partida_atual/<int:mesa_id>/', views.obter_partida_atual, name='obter_partida_atual'),
    path('real_time_partidas/', views.real_time_partidas, name='real_time_partidas'),
    path('atualizar_realtime_partidas/', views.atualizar_realtime_partidas, name='atualizar_realtime_partidas'),

    
    
]
