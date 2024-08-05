# operacao/models.py

from django.db import models
from datetime import datetime
from django.utils import timezone
from datetime import datetime, timedelta

class Jogador(models.Model):
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.nome

class Mesa(models.Model):
    link_transmissao = models.URLField(max_length=200, blank=True, null=True,default="")
    partida_atual = models.OneToOneField('Partida', related_name='mesa_atual', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Mesa {self.numero}"

class Partida(models.Model):
    id = models.AutoField(primary_key=True)
    jogador1 = models.ForeignKey(Jogador, related_name='partidas_como_jogador1', on_delete=models.CASCADE)
    jogador2 = models.ForeignKey(Jogador, related_name='partidas_como_jogador2', on_delete=models.CASCADE)
    mesa = models.ForeignKey(Mesa, related_name='partidas', on_delete=models.CASCADE, null=True, blank=True)
    data_partida = models.DateTimeField()
    melhor_de = models.IntegerField()
    vencedor = models.ForeignKey(Jogador, related_name='vitorias', on_delete=models.SET_NULL, null=True, blank=True)
    tempo_inicio = models.DateTimeField(default=timezone.now, null=True)
    tempo_total = models.DurationField(default=timedelta)
    

    def __str__(self):
        return f"{self.jogador1} vs {self.jogador2} - Mesa {self.mesa.numero if self.mesa else 'N/A'} - {self.data_partida}"

    def save(self, *args, **kwargs):
        super(Partida, self).save(*args, **kwargs)
        if not Set.objects.filter(partida=self).exists():
            Set.objects.create(partida=self, numero_set=1)
        super(Partida, self).save(*args, **kwargs)

    

class Set(models.Model):
    partida = models.ForeignKey(Partida, related_name='sets', on_delete=models.CASCADE)
    numero_set = models.IntegerField()
    vencedor = models.ForeignKey(Jogador, related_name='sets_vencidos', on_delete=models.SET_NULL, null=True, blank=True)
    pontos_jogador1 = models.IntegerField(default=0)
    pontos_jogador2 = models.IntegerField(default=0)
    faltas_jogador1 = models.IntegerField(default=0)
    faltas_jogador2 = models.IntegerField(default=0)
    tempo_pontos_jogador1 = models.DurationField(null=True)
    tempo_pontos_jogador2 = models.DurationField(null=True)
    tempo_faltas_jogador1 = models.DurationField(null=True)
    tempo_faltas_jogador2 = models.DurationField(null=True)
    tacada = models.IntegerField(default=0)

    def __str__(self):
        return f"Set {self.numero_set} - {self.partida} - Vencedor: {self.vencedor}"


class ActionHistory(models.Model):
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE, related_name='actions')
    player = models.IntegerField()
    points = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    falta = models.IntegerField(default=0)


from django.db import models

