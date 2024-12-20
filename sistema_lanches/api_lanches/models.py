from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True)
    endereco = models.TextField()

    def __str__(self):
        return self.nome

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nome

class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="pedidos")
    produtos = models.ManyToManyField(Produto)
    tipo_entrega = models.CharField(max_length=10, choices=[('entrega', 'Entrega'), ('retirada', 'Retirada')])
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, editable=False)

    def calcular_total(self):
        total = sum(produto.preco for produto in self.produtos.all())
        self.total = total
        return total

    def save(self, *args, **kwargs):
        self.calcular_total()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pedido de {self.cliente.nome}"
