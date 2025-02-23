from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from patrimonioweb.models import Bens, Categorias, Departamentos, Fornecedores, Movimentacoes
from datetime import date

class UserAuthTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_login_view(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)  

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302) 

    def test_perfil_usuario_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('perfil_usuario'))
        self.assertEqual(response.status_code, 200)  

class DashboardViewTests(TestCase):
    def test_dashboard_bens_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('dashboard_bens'))
        self.assertEqual(response.status_code, 200) 

class BensViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')  
        self.categoria = Categorias.objects.create(nome="Equipamentos")
        self.departamento = Departamentos.objects.create(nome="TI")
        self.bem = Bens.objects.create(nome="Computador", categoria=self.categoria, departamento=self.departamento, data_aquisicao=date.today(), valor=1500.00, codigo_rfid="RFID12345")

    def test_bens_list_view(self):
        response = self.client.get(reverse('bens_list'))
        self.assertEqual(response.status_code, 200)

    def test_bens_detail_view(self):
        response = self.client.get(reverse('bens_detail', args=[self.bem.pk]))
        self.assertEqual(response.status_code, 200) 

    def test_bens_create_view(self):
        response = self.client.post(reverse('bens_create'), {'nome': 'Impressora', 'categoria': self.categoria.pk, 'departamento': self.departamento.pk, 'data_aquisicao': date.today(), 'valor': 800.00, 'codigo_rfid': 'RFID67890'})
        self.assertEqual(response.status_code, 302) 

    def test_bens_update_view(self):
        response = self.client.post(reverse('bens_update', args=[self.bem.pk]), {'nome': 'Computador Atualizado', 'categoria': self.categoria.pk, 'departamento': self.departamento.pk, 'data_aquisicao': date.today(), 'valor': 1600.00, 'codigo_rfid': 'RFID12345'})
        self.assertEqual(response.status_code, 302) 

    def test_bens_delete_view(self):
        response = self.client.post(reverse('bens_delete', args=[self.bem.pk]))
        self.assertEqual(response.status_code, 302)  

class CategoriasViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.categoria = Categorias.objects.create(nome="Equipamentos")

    def test_categorias_list_view(self):
        response = self.client.get(reverse('categorias_list'))
        self.assertEqual(response.status_code, 200) 

    def test_categorias_create_view(self):
        response = self.client.post(reverse('categorias_create'), {'nome': 'Novo Categoria'})
        self.assertEqual(response.status_code, 302) 

    def test_categorias_update_view(self):
        response = self.client.post(reverse('categorias_update', args=[self.categoria.pk]), {'nome': 'Categoria Atualizada'})
        self.assertEqual(response.status_code, 302)  

    def test_categorias_delete_view(self):
        response = self.client.post(reverse('categorias_delete', args=[self.categoria.pk]))
        self.assertEqual(response.status_code, 302)  

class DepartamentosViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.departamento = Departamentos.objects.create(nome="TI")

    def test_departamentos_list_view(self):
        response = self.client.get(reverse('departamentos_list'))
        self.assertEqual(response.status_code, 200)   

    def test_departamentos_create_view(self):
        response = self.client.post(reverse('departamentos_create'), {'nome': 'Novo Departamento'})
        self.assertEqual(response.status_code, 302) 

    def test_departamentos_update_view(self):
        response = self.client.post(reverse('departamentos_update', args=[self.departamento.pk]), {'nome': 'Departamento Atualizado'})
        self.assertEqual(response.status_code, 302)  

    def test_departamentos_delete_view(self):
        response = self.client.post(reverse('departamentos_delete', args=[self.departamento.pk]))
        self.assertEqual(response.status_code, 302)  

class FornecedoresViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.fornecedor = Fornecedores.objects.create(nome="Fornecedor A")

    def test_fornecedores_list_view(self):
        response = self.client.get(reverse('fornecedores_list'))
        self.assertEqual(response.status_code, 200)  

    def test_fornecedores_detail_view(self):
        response = self.client.get(reverse('fornecedores_detail', args=[self.fornecedor.pk]))
        self.assertEqual(response.status_code, 200)  

    def test_fornecedores_create_view(self):
        response = self.client.post(reverse('fornecedores_create'), {'nome': 'Fornecedor B'})
        self.assertEqual(response.status_code, 302)  

    def test_fornecedores_update_view(self):
        response = self.client.post(reverse('fornecedores_update', args=[self.fornecedor.pk]), {'nome': 'Fornecedor Atualizado'})
        self.assertEqual(response.status_code, 302) 

    def test_fornecedores_delete_view(self):
        response = self.client.post(reverse('fornecedores_delete', args=[self.fornecedor.pk]))
        self.assertEqual(response.status_code, 302) 
class MovimentacoesViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.categoria = Categorias.objects.create(nome="Equipamentos")
        self.departamento = Departamentos.objects.create(nome="TI")
        self.bem = Bens.objects.create(
            nome="Computador",
            categoria=self.categoria,
            departamento=self.departamento,
            data_aquisicao=date.today(),
            valor=1500.00,
            codigo_rfid="RFID12345"
        )
        self.movimentacao = Movimentacoes.objects.create(
            bem=self.bem,
            departamento_origem=self.departamento,
            departamento_destino=self.departamento,
            responsavel="Responsável A"
        )

    def test_movimentacoes_list_view(self):
        response = self.client.get(reverse('movimentacoes_list'))
        self.assertEqual(response.status_code, 200) 

    def test_movimentacoes_detail_view(self):
        response = self.client.get(reverse('movimentacoes_detail', args=[self.movimentacao.pk]))
        self.assertEqual(response.status_code, 200) 

    def test_movimentacoes_create_view(self):
        response = self.client.post(reverse('movimentacoes_create'), {'bem': self.bem.pk, 'departamento_destino': self.departamento.pk, 'responsavel': 'Responsável B'})
        self.assertEqual(response.status_code, 302) 

    def test_movimentacoes_update_view(self):
        response = self.client.post(reverse('movimentacoes_update', args=[self.movimentacao.pk]), {'bem': self.bem.pk, 'departamento_destino': self.departamento.pk, 'responsavel': 'Responsável Atualizado'})
        self.assertEqual(response.status_code, 302)  

    def test_movimentacoes_delete_view(self):
        response = self.client.post(reverse('movimentacoes_delete', args=[self.movimentacao.pk]))
        self.assertEqual(response.status_code, 302)  
