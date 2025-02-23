from django.contrib import admin
from .models import Categorias, Departamentos, Fornecedores, Bens, Movimentacoes

admin.site.register(Categorias)
admin.site.register(Departamentos)
admin.site.register(Fornecedores)
admin.site.register(Bens)
admin.site.register(Movimentacoes)
