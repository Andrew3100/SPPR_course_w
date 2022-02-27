from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse
from .models import *
import random as r

# Проверяет, входит ли заданный GET-параметр в URL
def is_get_param_in_this_url(url, get):
    array = url.split('?')
    if len(array) == 0:
        return False
    del array[0]
    array = array
    dict = {}
    for i in array:
        arr = i.split('=')
        dict[arr[0]] = arr[1]
    gets = list(dict.keys())
    if get in gets:
        return True
    return False



# Create your views here.
def main(request):

    dictionary = {}

    dictionary['task_list'] = Tasks.objects.raw('SELECT * FROM sppr.tasks as tasked INNER JOIN sppr.task_type_ref WHERE task_type_ref.id = tasked.task_type')

    if is_get_param_in_this_url(request.get_full_path_info(),'start'):
        post = list(request.POST)
        del post[0]
        dictionary['post'] = post
        tasks_for_ppr = Tasks.objects.filter(id__in=post)
        dictionary['tasks_for_ppr'] = tasks_for_ppr
        users_for_ppr = Executors.objects.all()[:len(post)]
        dict = {}
        for user in users_for_ppr:
            times = []
            for i in range(0,len(post)):
                times.append(user.plain_execute_time+r.randint(0,10))
            dict[user.username] = times
        dictionary['user_times'] = dict

        # dictionary['users_for_ppr'] = users_for_ppr
    return render(request, 'C:/Users/Andrey/PycharmProjects/djangoProject2/hunguaryMethod/templates/home.html', dictionary)
