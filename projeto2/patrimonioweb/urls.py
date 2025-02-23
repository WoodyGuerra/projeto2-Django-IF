from django.urls import path
from . import views

urlpatterns = [
    
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    
    
    path('', views.dashboard_bens, name='dashboard_bens'),
    path('bens/', views.bens_list, name='bens_list'),

    path('bens/<int:pk>/', views.bens_detail, name='bens_detail'),
    path('bens/novo/', views.bens_create, name='bens_create'),
    path('bens/editar/<int:pk>/', views.bens_update, name='bens_update'),
    path('bens/excluir/<int:pk>/', views.bens_delete, name='bens_delete'),
    
    
    path('categorias/', views.categorias_list, name='categorias_list'),
    path('categorias/<int:pk>/', views.categorias_detail, name='categorias_detail'),
    path('categorias/novo/', views.categorias_create, name='categorias_create'),
    path('categorias/editar/<int:pk>/', views.categorias_update, name='categorias_update'),
    path('categorias/excluir/<int:pk>/', views.categorias_delete, name='categorias_delete'),

    
    path('departamentos/', views.departamentos_list, name='departamentos_list'),
    path('departamentos/<int:pk>/', views.departamentos_detail, name='departamentos_detail'),
    path('departamentos/novo/', views.departamentos_create, name='departamentos_create'),
    path('departamentos/editar/<int:pk>/', views.departamentos_update, name='departamentos_update'),
    path('departamentos/excluir/<int:pk>/', views.departamentos_delete, name='departamentos_delete'),

    
    path('fornecedores/', views.fornecedores_list, name='fornecedores_list'),
    path('fornecedores/<int:pk>/', views.fornecedores_detail, name='fornecedores_detail'),
    path('fornecedores/novo/', views.fornecedores_create, name='fornecedores_create'),
    path('fornecedores/editar/<int:pk>/', views.fornecedores_update, name='fornecedores_update'),
    path('fornecedores/excluir/<int:pk>/', views.fornecedores_delete, name='fornecedores_delete'),

    
    path('movimentacoes/', views.movimentacoes_list, name='movimentacoes_list'),
    path('movimentacoes/<int:pk>/', views.movimentacoes_detail, name='movimentacoes_detail'),
    path('movimentacoes/nova/', views.movimentacoes_create, name='movimentacoes_create'),
    path('movimentacoes/editar/<int:pk>/', views.movimentacoes_update, name='movimentacoes_update'),
    path('movimentacoes/excluir/<int:pk>/', views.movimentacoes_delete, name='movimentacoes_delete'),

]
