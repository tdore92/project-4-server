from django.core import validators
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Dinosaur(models.Model):
  name = models.CharField(max_length=50)

  class Type(models.TextChoices):
      CARNIVORE = 'CARN', _('Carnivore')
      HERBIVORE = 'HERB', _('Herbivore')
      PISCIVORE = 'PISC', _('Piscivore')

  type = models.CharField (
    max_length= 10,
    choices=Type.choices,
    default=Type.CARNIVORE
  )

  def is_upperclass(self):
    return self.type in {
      self.Type.CARNIVORE,
      self.Type.HERBIVORE,
    }

  danger_level = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

  
  class Size(models.TextChoices):
      LARGE = 'LRG', _('Large')
      MEDIUM = 'MED', _('Medium')
      SMALL = 'SML', _('Small')

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

  description = models.CharField(max_length=500)
  image = models.CharField(max_length=250)
  price = models.PositiveIntegerField(validators=[MinValueValidator(100), MaxValueValidator(10000000)])


  def __str__(self):
        return f'{self.name}'

