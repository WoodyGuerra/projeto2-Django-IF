from django.db import models

class Categorias(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

class Departamentos(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

class Fornecedores(models.Model):
    nome = models.CharField(max_length=200, unique=True)
    contato = models.CharField(max_length=100, blank=True, null=True)
    endereco = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome

class Bens(models.Model):
    nome = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categorias, on_delete=models.CASCADE)
    departamento = models.ForeignKey(Departamentos, on_delete=models.CASCADE)
    fornecedor = models.ForeignKey(Fornecedores, on_delete=models.SET_NULL, null=True, blank=True)
    data_aquisicao = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    codigo_rfid = models.CharField(max_length=50, unique=True)
    imagem = models.ImageField(upload_to='bens/', blank=True, null=True)

    def __str__(self):
        return self.nome

class Movimentacoes(models.Model):
    bem = models.ForeignKey(Bens, on_delete=models.CASCADE)
    departamento_origem = models.ForeignKey(Departamentos, related_name='origem', on_delete=models.CASCADE)
    departamento_destino = models.ForeignKey(Departamentos, related_name='destino', on_delete=models.CASCADE)
    data_movimentacao = models.DateTimeField(auto_now_add=True)
    responsavel = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.bem.nome} - {self.departamento_origem} → {self.departamento_destino}"
