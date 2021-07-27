from django.core import validators
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
# Create your models here.
class Misc(models.Model):
    name = models.CharField(max_length=50)

# MISC TYPE CLASS

    class Misctype(models.TextChoices):
        FOOD = 'Food', _('Food')
        TOY = 'Toy', _('Toy')

    misctype = models.CharField (
        max_length= 10,
        choices=Misctype.choices,
        default=Misctype.FOOD
    )

    def is_upperclass(self):
        return self.misctype in {
        self.Misctype.FOOD,
        self.Misctype.TOY,
        }

# DINO TYPE CLASS

    class Dinotype(models.TextChoices):
        CARNIVORE = 'Carnivore', _('Carnivore')
        HERBIVORE = 'Herbivore', _('Herbivore')
        PISCIVORE = 'Piscivore', _('Piscivore')

    dinotype = models.CharField (
        max_length= 10,
        choices=Dinotype.choices,
        default=Dinotype.CARNIVORE
    )

    def is_upperclass(self):
        return self.dinotype in {
        self.Dinotype.CARNIVORE,
        self.Dinotype.HERBIVORE,
        }

# SIZE CLASS

    class Size(models.TextChoices):
        LARGE = 'Large', _('Large')
        MEDIUM = 'Medium', _('Medium')
        SMALL = 'Small', _('Small')

    size = models.CharField (
        max_length= 10,
        choices=Size.choices,
        default=Size.MEDIUM
    )

    def is_upperclass(self):
            return self.size in {
            self.Size.MEDIUM,
            self.Size.LARGE,
            }

# DESCRIP, IMAGE AND PRICE

    description = models.CharField(max_length=500)
    image = models.CharField(max_length=250)
    price = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])

    def __str__(self):
        return f'{self.name}'

class Comment(models.Model):
    content = models.TextField(max_length=250)
    misc = models.ForeignKey(Misc, 
    related_name='comments', 
    on_delete=models.CASCADE
    )

    owner = models.ForeignKey(
        'jwt_auth.User',
        related_name='miscComments',
        on_delete=models.CASCADE
        
    )

    def __str__(self):
        return f'Comment {self.id} on {self.misc}'
