#-*- coding=utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
from bot.gui.models import TaskForm





def index(request):
    '''
Description:
    Import and show the index page.

Return value:
    HttpResponse
    '''

    return render_to_response('index.html')




def new(request):
    '''
Description:
    Show the add form

Return value:
    HttpResponse
    '''

    if request.method == 'POST': 
        f = TaskForm(request.POST)
        if f.is_valid():
            f.save()
            message = 'Dodano'
            form = TaskForm()
        else:
            message = 'Nie dodano:'
            form = f

    else:
        form = TaskForm()
        message = ''

    return render_to_response(
        'add.html',
        { 'message': message,
          'form': form.as_table(),
        }
    )    

    





