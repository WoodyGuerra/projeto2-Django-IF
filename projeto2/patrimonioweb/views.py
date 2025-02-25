from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum, Count

from django.core.paginator import Paginator

from .models import Bens, Categorias, Departamentos, Fornecedores, Movimentacoes

from .forms import BemForm, CategoriaForm, DepartamentoForm, FornecedorForm, MovimentacaoForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User


# =====================================
# USÚARIOS
# =====================================

# View de login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard_bens')
        else:
            messages.error(request, 'Usuário ou senha inválidos. Tente novamente.')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


# View de logout
@login_required
def logout_view(request):
    logout(request)
    return redirect('dashboard_bens')

# View de cadastro de usuário

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro realizado com sucesso! Faça login.')
            return redirect('login')
        else:
            messages.error(request, 'Erro ao criar conta. Verifique os dados e tente novamente.')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def perfil_usuario(request):
    usuario = request.user

    context = {
        'usuario': usuario
    }

    return render(request, 'registration/perfil_usuario.html', context)


# =====================================
# DASHBOARD
# =====================================

def dashboard_bens(request):
    total_assets = Bens.objects.count()
    bens = Bens.objects.all().order_by('data_aquisicao')

    # Cálculo do valor acumulado ao longo do tempo
    datas = []
    valores = []
    total_acumulado = 0

    for bem in bens:
        datas.append(bem.data_aquisicao.strftime('%d-%m-%Y'))
        total_acumulado += float(bem.valor)
        valores.append(total_acumulado)

    # Preparação da tabela de ativos
    tabela_dados = [{
        'nome': bem.nome,
        'data': bem.data_aquisicao.strftime('%d-%m-%Y'),
        'valor': float(bem.valor),
    } for bem in bens]

    # Distribuição dos ativos por categoria
    category_distribution = Bens.objects.values('categoria__nome').annotate(total=Count('id'))
    category_names = [item['categoria__nome'] for item in category_distribution]
    category_totals = [item['total'] for item in category_distribution]

    # Buscar movimentações recentes
    recent_movements = Movimentacoes.objects.order_by('-data_movimentacao')[:3]

    context = {
        'total_assets': total_assets,
        'category_names': category_names,
        'category_totals': category_totals,
        'recent_movements': recent_movements,
        'datas': datas,
        'valores': valores,
        'tabela_dados': tabela_dados,
        'total_acumulado': total_acumulado
    }

    return render(request, 'dashboard_bens.html', context)



# =====================================
# BENS
# =====================================

# Listar Bens
@login_required
def bens_list(request):
    bens_list = Bens.objects.all().order_by('id')
    paginator = Paginator(bens_list, 4)  # 4 por pagina
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'bens/bens_list.html', {'page_obj': page_obj})


# Detalhar Bem
@login_required
def bens_detail(request, pk):
    bem = get_object_or_404(Bens, pk=pk)
    return render(request, 'bens/bens_detail.html', {'bem': bem})



# Criar Bem
@login_required
def bens_create(request):
    if request.method == "POST":
        form = BemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('bens_list')
    else:
        form = BemForm()
    return render(request, 'bens/bens_create.html', {'form': form})



# Atualizar Bem
@login_required
def bens_update(request, pk):
    bem = get_object_or_404(Bens, pk=pk)
    if request.method == "POST":
        form = BemForm(request.POST, request.FILES, instance=bem)
        if form.is_valid():
            form.save()
            return redirect('bens_list')
    else:
        form = BemForm(instance=bem)
    return render(request, 'bens/bens_update.html', {'form': form, 'bem': bem})



# Excluir Bem
@login_required
def bens_delete(request, pk):
    bem = get_object_or_404(Bens, pk=pk)
    if request.method == "POST":
        bem.delete()
        return redirect('bens_list')
    return render(request, 'bens/bens_confirm_delete.html', {'bem': bem})




# =====================================
# CATEGORIAS
# =====================================

# Listar Categorias
@login_required
def categorias_list(request):
    categorias = Categorias.objects.all()
    return render(request, 'categorias/categorias_list.html', {'categorias': categorias})



# Detalhar Categoria
@login_required
def categorias_detail(request, pk):
    categoria = get_object_or_404(Categorias, pk=pk)
    return render(request, 'categorias/categorias_detail.html', {'categoria': categoria})



# Criar Categoria
@login_required
def categorias_create(request):
    if request.method == "POST":
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categorias_list')
    else:
        form = CategoriaForm()
    return render(request, 'categorias/categorias_create.html', {'form': form})



# Atualizar Categoria
@login_required
def categorias_update(request, pk):
    categoria = get_object_or_404(Categorias, pk=pk)
    if request.method == "POST":
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('categorias_list')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'categorias/categorias_update.html', {'form': form})



# Excluir Categoria
@login_required
def categorias_delete(request, pk):
    categoria = get_object_or_404(Categorias, pk=pk)
    if request.method == "POST":
        categoria.delete()
        return redirect('categorias_list')
    return render(request, 'categorias/categorias_confirm_delete.html', {'categoria': categoria})




# =====================================
# DEPARTAMENTOS
# =====================================

# Listar Departamentos
@login_required
def departamentos_list(request):
    departamentos = Departamentos.objects.all()
    return render(request, 'departamentos/departamentos_list.html', {'departamentos': departamentos})



# Detalhar Departamento
@login_required
def departamentos_detail(request, pk):
    departamento = get_object_or_404(Departamentos, pk=pk)
    return render(request, 'departamentos/departamentos_detail.html', {'departamento': departamento})



# Criar Departamento
@login_required
def departamentos_create(request):
    if request.method == "POST":
        form = DepartamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('departamentos_list')
    else:
        form = DepartamentoForm()
    return render(request, 'departamentos/departamentos_create.html', {'form': form})



# Atualizar Departamento
@login_required
def departamentos_update(request, pk):
    departamento = get_object_or_404(Departamentos, pk=pk)
    if request.method == "POST":
        form = DepartamentoForm(request.POST, instance=departamento)
        if form.is_valid():
            form.save()
            return redirect('departamentos_list')
    else:
        form = DepartamentoForm(instance=departamento)
    return render(request, 'departamentos/departamentos_update.html', {'form': form, 'departamento': departamento})



# Excluir Departamento
@login_required
def departamentos_delete(request, pk):
    departamento = get_object_or_404(Departamentos, pk=pk)
    if request.method == "POST":
        departamento.delete()
        return redirect('departamentos_list')
    return render(request, 'departamentos/departamentos_confirm_delete.html', {'departamento': departamento})




# =====================================
# FORNECEDORES
# =====================================

# Listar Fornecedores
@login_required
def fornecedores_list(request):
    fornecedores = Fornecedores.objects.all()
    return render(request, 'fornecedores/fornecedores_list.html', {'fornecedores': fornecedores})



# Detalhar Fornecedor
@login_required
def fornecedores_detail(request, pk):
    fornecedor = get_object_or_404(Fornecedores, pk=pk)
    return render(request, 'fornecedores/fornecedores_detail.html', {'fornecedor': fornecedor})



# Criar Fornecedor
@login_required
def fornecedores_create(request):
    if request.method == "POST":
        form = FornecedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fornecedores_list')
    else:
        form = FornecedorForm()
    return render(request, 'fornecedores/fornecedores_create.html', {'form': form})



# Atualizar Fornecedor
@login_required
def fornecedores_update(request, pk):
    fornecedor = get_object_or_404(Fornecedores, pk=pk)
    if request.method == "POST":
        form = FornecedorForm(request.POST, instance=fornecedor)
        if form.is_valid():
            form.save()
            return redirect('fornecedores_list')
    else:
        form = FornecedorForm(instance=fornecedor)
    return render(request, 'fornecedores/fornecedores_update.html', {'form': form, 'fornecedor': fornecedor})



# Excluir Fornecedor
@login_required
def fornecedores_delete(request, pk):
    fornecedor = get_object_or_404(Fornecedores, pk=pk)
    if request.method == "POST":
        fornecedor.delete()
        return redirect('fornecedores_list')
    return render(request, 'fornecedores/fornecedores_confirm_delete.html', {'fornecedor': fornecedor})




# =====================================
# MOVIMENTAÇÕES
# =====================================

# Listar Movimentações
@login_required
def movimentacoes_list(request):
    movimentacoes = Movimentacoes.objects.all()
    return render(request, 'movimentacoes/movimentacoes_list.html', {'movimentacoes': movimentacoes})



# Detalhar Movimentação
@login_required
def movimentacoes_detail(request, pk):
    movimentacao = get_object_or_404(Movimentacoes, pk=pk)
    return render(request, 'movimentacoes/movimentacoes_detail.html', {'movimentacao': movimentacao})



# Criar Movimentação
@login_required
def movimentacoes_create(request):
    if request.method == "POST":
        form = MovimentacaoForm(request.POST)
        if form.is_valid():
            bem = form.cleaned_data['bem']
            departamento_origem = bem.departamento  # Lock the source department to the asset's current department
            departamento_destino = form.cleaned_data['departamento_destino']
            
            # Create the movement
            movimentacao = Movimentacoes(
                bem=bem,
                departamento_origem=departamento_origem,
                departamento_destino=departamento_destino,
                responsavel=form.cleaned_data['responsavel']
            )
            movimentacao.save()
            
            # Update the asset's department to the destination department
            bem.departamento = departamento_destino
            bem.save()
            
            return redirect('movimentacoes_list')
    else:
        form = MovimentacaoForm()
    return render(request, 'movimentacoes/movimentacoes_create.html', {'form': form})




# Atualizar Movimentação
@login_required
def movimentacoes_update(request, pk):
    movimentacao = get_object_or_404(Movimentacoes, pk=pk)
    if request.method == "POST":
        form = MovimentacaoForm(request.POST, instance=movimentacao)
        if form.is_valid():
            bem = form.cleaned_data['bem']
            departamento_origem = bem.departamento  # Lock the source department to the asset's current department
            departamento_destino = form.cleaned_data['departamento_destino']
            
            # Update the movement
            movimentacao.bem = bem
            movimentacao.departamento_origem = departamento_origem
            movimentacao.departamento_destino = departamento_destino
            movimentacao.responsavel = form.cleaned_data['responsavel']
            movimentacao.save()
            
            return redirect('movimentacoes_list')
    else:
        form = MovimentacaoForm(instance=movimentacao)
    return render(request, 'movimentacoes/movimentacoes_update.html', {'form': form, 'movimentacao': movimentacao})




# Excluir Movimentação
@login_required
def movimentacoes_delete(request, pk):
    movimentacao = get_object_or_404(Movimentacoes, pk=pk)
    if request.method == "POST":
        movimentacao.delete()
        return redirect('movimentacoes_list')
    return render(request, 'movimentacoes/movimentacoes_confirm_delete.html', {'movimentacao': movimentacao})
