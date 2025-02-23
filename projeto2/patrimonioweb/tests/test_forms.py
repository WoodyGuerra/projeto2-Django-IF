from django.test import TestCase
from patrimonioweb.forms import CategoriaForm, DepartamentoForm, FornecedorForm, BemForm
from patrimonioweb.models import Categorias, Departamentos, Fornecedores, Bens
from datetime import date

class CategoriaFormTest(TestCase):
    def test_categoria_form_valid_data(self):
        form = CategoriaForm(data={"nome": "Equipamentos"})
        self.assertTrue(form.is_valid())

    def test_categoria_form_invalid_data(self):
        form = CategoriaForm(data={"nome": ""})
        self.assertFalse(form.is_valid())
        self.assertIn("nome", form.errors)

class DepartamentoFormTest(TestCase):
    def test_departamento_form_valid_data(self):
        form = DepartamentoForm(data={"nome": "TI"})
        self.assertTrue(form.is_valid())

    def test_departamento_form_invalid_data(self):
        form = DepartamentoForm(data={"nome": ""})
        self.assertFalse(form.is_valid())
        self.assertIn("nome", form.errors)

class FornecedorFormTest(TestCase):
    def test_fornecedor_form_valid_data(self):
        form = FornecedorForm(data={"nome": "Fornecedor A", "contato": "123456789", "endereco": "Rua A"})
        self.assertTrue(form.is_valid())

    def test_fornecedor_form_invalid_data(self):
        form = FornecedorForm(data={"nome": ""})
        self.assertFalse(form.is_valid())
        self.assertIn("nome", form.errors)

class BemFormTest(TestCase):
    def test_bem_form_valid_data(self):
        categoria = Categorias.objects.create(nome="Equipamentos")
        departamento = Departamentos.objects.create(nome="TI")
        form = BemForm(data={
            "nome": "Computador",
            "categoria": categoria.id,
            "departamento": departamento.id,
            "data_aquisicao": date.today(),
            "valor": 1500.00,
            "codigo_rfid": "RFID12345"
        })
        self.assertTrue(form.is_valid())

    def test_bem_form_invalid_data(self):
        form = BemForm(data={"nome": "", "categoria": "", "departamento": "", "data_aquisicao": "", "valor": "", "codigo_rfid": ""})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), len(form.errors.keys()))
