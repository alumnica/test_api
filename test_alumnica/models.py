from django.db import models

# Create your models here.

from django.db import models
from django.utils import timezone
from enum import Enum
from datetime import timedelta
from django.contrib.auth.models import User



def upload_to(instance, filename):
    """
    Generic method to upload files to specific folder
    :param instance: file instance with folder name property
    :param filename: file name
    :return: path to upload file
    """
    folder = '{}/{}'.format(instance.folder, filename)    
    return folder


class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        return tuple((i.name,i.value) for i in cls)

class typeMoment(ChoiceEnum):  # A Subclass of Enum
    divergente    = 'divergente'
    asimilador  = 'asimilador'
    convergente = 'convergente'
    acomodador  = 'acomodador' 

class axis(ChoiceEnum):  # A Subclass of Enum
    obs    = 'observacion'
    abst  = 'abstraccion'
    exp_act = 'exp_activa'
    exp_con  = 'exp_concreta' 


class Alumno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username    


class QuestionColb(models.Model):    
    text = models.CharField(max_length=124, blank = False, null = False)    
    ranking = models.IntegerField( default=0, null = True) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

class OptionColb(models.Model):    
    text = models.CharField(max_length=64, blank = False, null = False)
    question = models.ForeignKey('QuestionColb', on_delete=models.CASCADE)
    axis = models.CharField(max_length=10, choices = axis.choices())     
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str (self.question) + " - " + self.text

class TestColb(models.Model):    
    question = models.ForeignKey('QuestionColb', on_delete=models.CASCADE,)
    user = models.ForeignKey('Alumno', on_delete=models.CASCADE,)
    axis_obs = models.PositiveSmallIntegerField(default=0)
    axis_abst = models.PositiveSmallIntegerField(default=0)
    axis_exp_act = models.PositiveSmallIntegerField(default=0)
    axis_exp_con = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return str (self.user)


class OptionCard(models.Model):    
    text = models.CharField(max_length=124, blank = False, null = False)
    type_moment = models.CharField(max_length=12, choices = typeMoment.choices()) 
    file_name = models.CharField(max_length=150, default='')
    file = models.ImageField(upload_to=upload_to)
    folder = models.CharField(max_length=150, default='general')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name + "-" + self.type_moment

class ParCard (models.Model):    
    text = models.CharField(max_length=124,  default="¿Con cuál te identificas más?")
    options = models.ManyToManyField('OptionCard')
    #option_2 = models.ForeignKey('OptionCard', on_delete=models.CASCADE, related_name="option_dos")    
    type_moment_selected =  models.CharField(max_length=10, choices = typeMoment.choices())   
    test = models.ForeignKey('TestCard', on_delete=models.CASCADE)
    
    def __str__(self):
        return str (self.test) + " - " + self.text

class TestCard(models.Model):        
    user = models.ForeignKey('Alumno', on_delete=models.CASCADE,)    
    id_last_set = models.PositiveIntegerField(default=0)
    affi_divergente = models.PositiveSmallIntegerField(default=0)
    affi_asimilador = models.PositiveSmallIntegerField(default=0)
    affi_convergente = models.PositiveSmallIntegerField(default=0)
    affi_acomodador = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return str (self.user )

    def get_pares(self):
        print ('get pares')
        return self.parcard_set.filter(type_moment_selected="")

    def get_last_set(self):
        print ('get get_last_set')
        return self.parcard_set.filter(id__gte = self.id_last_set)
    