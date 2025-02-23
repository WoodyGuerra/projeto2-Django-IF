from django import forms
from .models import Bens, Categorias, Departamentos, Fornecedores, Movimentacoes


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categorias
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da categoria'}),
        }


class DepartamentoForm(forms.ModelForm):
    class Meta:
        model = Departamentos
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do departamento'}),
        }


class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedores
        fields = ['nome', 'contato', 'endereco']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do fornecedor'}),
            'contato': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contato'}),
            'endereco': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Endereço', 'rows': 3}),
        }


class BemForm(forms.ModelForm):
    class Meta:
        model = Bens
        fields = ['nome', 'categoria', 'departamento', 'fornecedor', 'data_aquisicao', 'valor', 'codigo_rfid', 'imagem']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do bem'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'departamento': forms.Select(attrs={'class': 'form-control'}),
            'fornecedor': forms.Select(attrs={'class': 'form-control'}),
            'data_aquisicao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'codigo_rfid': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código RFID'}),
            'imagem': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }


class MovimentacaoForm(forms.ModelForm):
    class Meta:
        model = Movimentacoes
        fields = ['bem', 'departamento_destino', 'responsavel']  # Removed 'departamento_origem'
        widgets = {
            'bem': forms.Select(attrs={'class': 'form-control'}),
            'departamento_destino': forms.Select(attrs={'class': 'form-control'}),
            'responsavel': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Responsável pela movimentação'}),
        }
