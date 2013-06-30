#-*- coding=utf-8 -*-
from django.forms import ModelForm
from django.db import models




class Task(models.Model):
    '''
Description:
    Representation of a task of waiting for a free place in a group.

    Contains:
        lecture id
        type of class
        group number
        group number (internal)
        login to SZ
        passwd to SZ
        email adress
        jabber address
    '''
    def __unicode__(self):
        return unicode(self.przedmiot)

    GROUP_CHOICES = (
        ('c',  'Ćwiczenia'),
        ('p',  'Pracowania'),
        ('cp', 'Ćwiczenia/Pracowania'),
        ('s',  'Grupa seminaryjna'),
    )


    przedmiot = models.IntegerField()
    rodzaj_Zajec = models.CharField(max_length=2, choices=GROUP_CHOICES)
    grupa = models.IntegerField()
    grupa_do_zapisu = models.IntegerField(null=True, blank=True)
    login = models.IntegerField(null=True, blank=True, max_length=7)
    haslo = models.CharField(max_length=8,blank=True)
    email = models.EmailField(max_length=30)
    jabber = models.EmailField(max_length=30,blank=True)


class TaskForm(ModelForm):
    '''
Description:
    A form automatically generated for Task class
    '''
    class Meta:
        model = Task






