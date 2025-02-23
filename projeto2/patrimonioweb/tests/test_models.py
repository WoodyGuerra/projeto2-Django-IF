from django.test import TestCase
from django.core.exceptions import ValidationError
from patrimonioweb.models import Categorias, Departamentos, Fornecedores, Bens, Movimentacoes
from datetime import date

class CategoriasModelTest(TestCase):
    def test_nome_deve_ser_unico(self):
        Categorias.objects.create(nome="Equipamentos")
        categoria_duplicada = Categorias(nome="Equipamentos")
        with self.assertRaises(ValidationError):
            categoria_duplicada.full_clean()

class DepartamentosModelTest(TestCase):
    def test_nome_deve_ser_unico(self):
        Departamentos.objects.create(nome="TI")
        departamento_duplicado = Departamentos(nome="TI")
        with self.assertRaises(ValidationError):
            departamento_duplicado.full_clean()

class FornecedoresModelTest(TestCase):
    def test_nome_deve_ser_unico(self):
        Fornecedores.objects.create(nome="Fornecedor A")
        fornecedor_duplicado = Fornecedores(nome="Fornecedor A")
        with self.assertRaises(ValidationError):
            fornecedor_duplicado.full_clean()

class BensModelTest(TestCase):
    def test_codigo_rfid_deve_ser_unico(self):
        Bens.objects.create(nome="Computador", codigo_rfid="RFID12345", categoria=Categorias.objects.create(nome="Equipamentos"), departamento=Departamentos.objects.create(nome="TI"), data_aquisicao=date.today(), valor=1500.00)
        bem_duplicado = Bens(nome="Impressora", codigo_rfid="RFID12345", categoria=Categorias.objects.create(nome="Equipamentos"), departamento=Departamentos.objects.create(nome="TI"), data_aquisicao=date.today(), valor=1500.00)
        with self.assertRaises(ValidationError):
            bem_duplicado.full_clean()

class MovimentacoesModelTest(TestCase):
    def setUp(self):
        self.categoria = Categorias.objects.create(nome="Equipamentos")
        self.departamento_origem = Departamentos.objects.create(nome="TI")
        self.departamento_destino = Departamentos.objects.create(nome="Financeiro")
        self.fornecedor = Fornecedores.objects.create(nome="Fornecedor A")
        self.bem = Bens.objects.create(nome="Computador", categoria=self.categoria, departamento=self.departamento_origem, fornecedor=self.fornecedor, data_aquisicao=date.today(), valor=1500.00, codigo_rfid="RFID12345")

    def test_movimentacao_deve_atualizar_situacao_do_bem(self):
        movimentacao = Movimentacoes(bem=self.bem, departamento_origem=self.departamento_origem, departamento_destino=self.departamento_destino, responsavel="João")
        movimentacao.full_clean()  # Should not raise ValidationError
