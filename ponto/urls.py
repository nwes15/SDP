from django.urls import path
from . import views

urlpatterns = [
    # Autenticação
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboards
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('motorista/', views.motorista_dashboard, name='motorista_dashboard'),
    
    # Registro de ponto
    path('registrar/<str:tipo>/', views.registrar_ponto, name='registrar_ponto'),
    
    # Administração - Motoristas
    path('admin/motoristas/', views.listar_motoristas, name='listar_motoristas'),
    path('admin/motoristas/cadastrar/', views.cadastrar_motorista, name='cadastrar_motorista'),
    path('admin/motoristas/editar/<int:id>/', views.editar_motorista, name='editar_motorista'),
    
    # Administração - Veículos
    path('admin/veiculos/', views.listar_veiculos, name='listar_veiculos'),
    path('admin/veiculos/cadastrar/', views.cadastrar_veiculo, name='cadastrar_veiculo'),
    path('admin/veiculos/editar/<int:id>/', views.editar_veiculo, name='editar_veiculo'),
    
    # Administração - Mercados
    path('admin/mercados/', views.listar_mercados, name='listar_mercados'),
    path('admin/mercados/cadastrar/', views.cadastrar_mercado, name='cadastrar_mercado'),
    path('admin/mercados/editar/<int:id>/', views.editar_mercado, name='editar_mercado'),
    
    # Relatórios
    path('admin/relatorios/', views.relatorio_ponto, name='relatorio_ponto'),
    path('admin/relatorios/gerar/', views.gerar_relatorio, name='gerar_relatorio'),
    path('admin/relatorio/exportar/', views.exportar_relatorio_excel, name='exportar_relatorio_excel'),
    
    # Registros
    path('admin/registros/', views.listar_registros, name='listar_registros'),
    path('admin/registros/<int:id>/', views.detalhe_registro_html, name='detalhe_registro_html'),
    path('admin/registros/<int:id>/', views.detalhe_registro, name='detalhe_registro'),
    path('admin/registros/<int:id>/fotos/', views.api_registro_fotos, name='api_registro_fotos'),

    
    # APIs
    path('admin/api/status-motoristas-hoje/', views.api_status_motoristas_hoje, name='api_status_motoristas_hoje'),
]