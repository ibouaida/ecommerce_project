# Product models placeholder
class Category(models.Model):
    name = models.CharField(max_length=100)

class Product(models.Model):
    seller = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/')
