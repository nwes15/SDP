from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import os
from django.utils import timezone

def upload_to_registro(instance, filename):
    """Função para organizar o upload das fotos por data"""
    today = timezone.now().strftime('%Y/%m/%d')
    return f'registros/{today}/{instance.motorista.user.username}_{filename}'

class Mercado(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome do Mercado")
    endereco = models.TextField(blank=True, null=True, verbose_name="Endereço")
    telefone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    data_cadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Mercado"
        verbose_name_plural = "Mercados"
        ordering = ['nome']

    def __str__(self):
        return self.nome

class Veiculo(models.Model):
    placa = models.CharField(max_length=8, unique=True, verbose_name="Placa")
    modelo = models.CharField(max_length=50, verbose_name="Modelo")
    cor = models.CharField(max_length=30, verbose_name="Cor")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    data_cadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Veículo"
        verbose_name_plural = "Veículos"
        ordering = ['placa']

    def __str__(self):
        return f"{self.placa} - {self.modelo} ({self.cor})"

class Motorista(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuário")
    nome_completo = models.CharField(max_length=100, verbose_name="Nome Completo")
    cpf = models.CharField(max_length=14, unique=True, verbose_name="CPF")
    telefone = models.CharField(max_length=20, verbose_name="Telefone")
    valor_dia = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        validators=[MinValueValidator(0)],
        verbose_name="Valor por Dia (R$)"
    )
    veiculo = models.ForeignKey(
        Veiculo, 
        on_delete=models.PROTECT, 
        verbose_name="Veículo"
    )
    mercado = models.ForeignKey(
        Mercado, 
        on_delete=models.PROTECT, 
        verbose_name="Mercado"
    )
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    data_cadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Motorista"
        verbose_name_plural = "Motoristas"
        ordering = ['nome_completo']

    def __str__(self):
        return f"{self.nome_completo} - {self.mercado.nome}"

class RegistroPonto(models.Model):
    TIPO_CHOICES = [
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
    ]

    motorista = models.ForeignKey(
        Motorista, 
        on_delete=models.CASCADE, 
        verbose_name="Motorista"
    )
    tipo = models.CharField(
        max_length=10, 
        choices=TIPO_CHOICES, 
        verbose_name="Tipo"
    )
    data_hora = models.DateTimeField(auto_now_add=True, verbose_name="Data/Hora")
    
    # Fotos obrigatórias
    foto_odometro = models.ImageField(
        upload_to=upload_to_registro, 
        verbose_name="Foto do Odômetro"
    )
    foto_combustivel = models.ImageField(
        upload_to=upload_to_registro, 
        verbose_name="Foto do Combustível"
    )
    
    # Valores informados pelo motorista
    km_odometro = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name="KM do Odômetro"
    )
    nivel_combustivel = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Nível Combustível (%)",
        help_text="Informe o percentual de combustível (0-100%)"
    )
    
    # Observações opcionais
    observacoes = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Observações"
    )

    class Meta:
        verbose_name = "Registro de Ponto"
        verbose_name_plural = "Registros de Ponto"
        ordering = ['-data_hora']
        unique_together = (('motorista', 'data_hora', 'tipo'),)

    def __str__(self):
        return f"{self.motorista.nome_completo} - {self.get_tipo_display()} - {self.data_hora.strftime('%d/%m/%Y %H:%M')}"

    @property
    def data_formatada(self):
        return self.data_hora.strftime('%d/%m/%Y')
    
    @property
    def hora_formatada(self):
        return self.data_hora.strftime('%H:%M')

    def get_registro_par(self):
        """Retorna o registro de entrada/saída correspondente do mesmo dia"""
        data_atual = self.data_hora.date()
        tipo_oposto = 'saida' if self.tipo == 'entrada' else 'entrada'
        
        try:
            return RegistroPonto.objects.get(
                motorista=self.motorista,
                tipo=tipo_oposto,
                data_hora__date=data_atual
            )
        except RegistroPonto.DoesNotExist:
            return None

    def calcular_horas_trabalhadas(self):
        """Calcula as horas trabalhadas no dia (se houver entrada e saída)"""
        if self.tipo == 'entrada':
            saida = self.get_registro_par()
            if saida:
                delta = saida.data_hora - self.data_hora
                return delta.total_seconds() / 3600  # Retorna em horas
        elif self.tipo == 'saida':
            entrada = self.get_registro_par()
            if entrada:
                delta = self.data_hora - entrada.data_hora
                return delta.total_seconds() / 3600  # Retorna em horas
        return 0

    def calcular_km_rodados(self):
        """Calcula os km rodados no dia (saída - entrada)"""
        if self.tipo == 'saida':
            entrada = self.get_registro_par()
            if entrada and self.km_odometro > entrada.km_odometro:
                return self.km_odometro - entrada.km_odometro
        return 0