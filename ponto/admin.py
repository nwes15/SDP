from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Mercado, Veiculo, Motorista, RegistroPonto

@admin.register(Mercado)
class MercadoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'ativo', 'data_cadastro')
    list_filter = ('ativo', 'data_cadastro')
    search_fields = ('nome', 'endereco')
    ordering = ('nome',)
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'endereco', 'telefone')
        }),
        ('Status', {
            'fields': ('ativo',)
        }),
    )

@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ('placa', 'modelo', 'cor', 'ativo', 'data_cadastro')
    list_filter = ('ativo', 'cor', 'data_cadastro')
    search_fields = ('placa', 'modelo')
    ordering = ('placa',)
    
    fieldsets = (
        ('Informações do Veículo', {
            'fields': ('placa', 'modelo', 'cor')
        }),
        ('Status', {
            'fields': ('ativo',)
        }),
    )

@admin.register(Motorista)
class MotoristaAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'cpf', 'telefone', 'veiculo', 'mercado', 'valor_dia', 'ativo')
    list_filter = ('ativo', 'mercado', 'veiculo', 'data_cadastro')
    search_fields = ('nome_completo', 'cpf', 'user__username')
    ordering = ('nome_completo',)
    
    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('user', 'nome_completo', 'cpf', 'telefone')
        }),
        ('Trabalho', {
            'fields': ('valor_dia', 'veiculo', 'mercado')
        }),
        ('Status', {
            'fields': ('ativo',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editando
            return ('user', 'cpf')
        return ()

@admin.register(RegistroPonto)
class RegistroPontoAdmin(admin.ModelAdmin):
    list_display = ('motorista', 'tipo', 'data_hora', 'km_odometro', 'nivel_combustivel', 'ver_fotos')
    list_filter = ('tipo', 'data_hora', 'motorista__mercado')
    search_fields = ('motorista__nome_completo', 'motorista__cpf')
    ordering = ('-data_hora',)
    readonly_fields = ('data_hora', 'ver_fotos_grandes')
    
    fieldsets = (
        ('Registro', {
            'fields': ('motorista', 'tipo', 'data_hora')
        }),
        ('Dados do Veículo', {
            'fields': ('km_odometro', 'nivel_combustivel')
        }),
        ('Fotos', {
            'fields': ('foto_odometro', 'foto_combustivel', 'ver_fotos_grandes')
        }),
        ('Observações', {
            'fields': ('observacoes',)
        }),
    )
    
    def ver_fotos(self, obj):
        if obj.foto_odometro and obj.foto_combustivel:
            return format_html(
                '<a href="{}" target="_blank">Ver Fotos</a>',
                reverse('admin:ponto_registroponto_change', args=[obj.id])
            )
        return "Sem fotos"
    ver_fotos.short_description = "Fotos"
    
    def ver_fotos_grandes(self, obj):
        html = ""
        if obj.foto_odometro:
            html += f'<div style="margin-bottom: 10px;"><strong>Odômetro:</strong><br><img src="{obj.foto_odometro.url}" style="max-width: 300px; max-height: 200px;"></div>'
        if obj.foto_combustivel:
            html += f'<div><strong>Combustível:</strong><br><img src="{obj.foto_combustivel.url}" style="max-width: 300px; max-height: 200px;"></div>'
        return mark_safe(html) if html else "Sem fotos"
    ver_fotos_grandes.short_description = "Visualizar Fotos"

# Customização do Django Admin
admin.site.site_header = "Sistema de Ponto - Administração Django"
admin.site.site_title = "Sistema de Ponto"
admin.site.index_title = "Painel Administrativo Django"