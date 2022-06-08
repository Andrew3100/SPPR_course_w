from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse
from .models import *
import random as r
import itertools
import numpy as np
from numpy import random
from scipy.optimize import linear_sum_assignment
import time as t
from github import Github


class TaskAssignment:
    import sklearn
    # Инициализация класса, обязательными входными параметрами являются матрица задач и метод распределения, среди которых есть два метода распределения, метод all_permutation или метод Венгрии.
    def __init__(self, task_matrix, mode):
        self.task_matrix = task_matrix
        self.mode = mode
        if mode == 'all_permutation':
            self.min_cost, self.best_solution = self.all_permutation(task_matrix)
        if mode == 'Hungary':
            self.min_cost, self.best_solution, self.row_ind, self.col_ind = self.Hungary(task_matrix)

        # Полный метод аранжировки

    def Hungary(self, task_matrix):
        b = task_matrix.copy()
        # Строка и столбец минус 0
        for i in range(len(b)):
            row_min = np.min(b[i])
            for j in range(len(b[i])):
                b[i][j] -= row_min
        for i in range(len(b[0])):
            col_min = np.min(b[:, i])
            for j in range(len(b)):
                b[j][i] -= col_min
        line_count = 0
        # Когда количество строк меньше длины матрицы, цикл
        while (line_count < len(b)):
            line_count = 0
            row_zero_count = []
            col_zero_count = []
            for i in range(len(b)):
                row_zero_count.append(np.sum(b[i] == 0))
            for i in range(len(b[0])):
                col_zero_count.append((np.sum(b[:, i] == 0)))
                # Нажать порядок (ветка или столбец)
            line_order = []
            row_or_col = []
            for i in range(len(b[0]), 0, -1):
                while (i in row_zero_count):
                    line_order.append(row_zero_count.index(i))
                    row_or_col.append(0)
                    row_zero_count[row_zero_count.index(i)] = 0
                while (i in col_zero_count):
                    line_order.append(col_zero_count.index(i))
                    row_or_col.append(1)
                    col_zero_count[col_zero_count.index(i)] = 0
                    # Нарисуйте линию, покрывающую 0, и получите матрицу после строки минус минимальное значение и столбец плюс минимальное значение
            delete_count_of_row = []
            delete_count_of_rol = []
            row_and_col = [i for i in range(len(b))]
            for i in range(len(line_order)):
                if row_or_col[i] == 0:
                    delete_count_of_row.append(line_order[i])
                else:
                    delete_count_of_rol.append(line_order[i])
                c = np.delete(b, delete_count_of_row, axis=0)
                c = np.delete(c, delete_count_of_rol, axis=1)
                line_count = len(delete_count_of_row) + len(delete_count_of_rol)
                # Когда количество строк равно длине матрицы, выскакиваем
                if line_count == len(b):
                    break
                    # Определяем, нужно ли рисовать линию, чтобы покрыть все нули, если она покрывает, операции сложения и вычитания
                if 0 not in c:
                    row_sub = list(set(row_and_col) - set(delete_count_of_row))
                    min_value = np.min(c)
                    for i in row_sub:
                        b[i] = b[i] - min_value
                    for i in delete_count_of_rol:
                        b[:, i] = b[:, i] + min_value
                    break
        row_ind, col_ind = linear_sum_assignment(b)
        min_cost = task_matrix[row_ind, col_ind].sum()
        best_solution = list(task_matrix[row_ind, col_ind])
        return min_cost, best_solution, row_ind, col_ind




def in_url(get,request):
    current_url = request.get_full_path_info()
    array = current_url.split('?')
    if len(array) == 0:
        # array = current_url.split('?')
        # if len(array) == 0:
        return False
    del array[0]
    array = array
    dict = {}
    print(array)
    for i in array:
        arr = i.split('=')
        dict[arr[0]] = arr[1]
    print(dict)
    gets = list(dict.keys())
    if get in gets:
        return True
    return False




# Create your views here.
def projects(request):

    # Список проектов
    projects = Projects.objects.filter(status=1)
    dictionary = {}
    dictionary['projects'] = projects
    return render(request, 'C:/Users/Andrey/PycharmProjects/SPPR_course_w/hunguaryMethod/templates/projects.html', dictionary)


def get_start_time_by_commit(string):
    arr = string.split('Время работы над задачей ')
    arr1 = arr[1].split(' - ')[0]
    return arr1


def get_end_time_by_commit(string):
    arr = string.split('Время работы над задачей ')
    arr1 = arr[1].split(' - ')[1]
    return arr1


def get_task_id_by_commit_message(string):
    arr = string.split('. Время работы над задачей ')[0]
    arr1 = arr.split(': ')[1]
    return arr1


def project_card(request):

    dictionary = {}
    dictionary['tasks_tab'] = Tasks.objects.all()

    for d in dictionary['tasks_tab']:
        d.count_auction = len(AuctionTask.objects.filter(task_id=d.id))

        # используя токен доступа
        # git = Github("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")

    # git = Github("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")
    # repos = git.get_repo('Andrew3100/BelAvtoProkat2022')
    #
    # cmt = repos.get_commit('8b01a8891c45a5ca25fdd6d74dbba1411fb38c54')

    # print(cmt.get_comments())

    # dictionary['data'] = cmt.raw_data['commit']['message'] --- ДАЁТ ДОСТУП К ТЕКСТУ КОММИТА






    # чтение коммитов проекта по API
    # git = Github("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")
    # repos = git.get_repo('Andrew3100/TestVKR')
    #
    # dict_commit = {}
    #
    dictionary['commits'] = sha_list = GitCommits.objects.all()
    # sha_inDB = []
    # for sha in sha_list:
    #     sha_inDB.append(sha.sha)
    #
    # for repo in repos.get_commits():
    #     print(repo.raw_data)
        # if repo.raw_data['commit']['message'] != 'Initial Commit' and repo.raw_data['sha'] not in sha_inDB:
        #     шифр коммита, по нему можно проверить поступал ли такой коммит в базу
            # dict_commit['start_work'] = get_start_time_by_commit(repo.raw_data['commit']['message'])
            # dict_commit['commit_and_push_time'] = repo.raw_data['commit']['author']['date']
            # dict_commit['commit_message'] = repo.raw_data['commit']['message']
            # taskid = get_task_id_by_commit_message(repo.raw_data['commit']['message'])
            # dict_commit['task_id'] = taskid
            # dict_commit['project_id'] = request.GET['project_id']
            # dict_commit['sha'] = repo.raw_data['sha']
            # GitCommits(**dict_commit).save()
            # dict_close_task = {}
            # dict_close_task['closed'] = dict_commit['start_work'] = get_start_time_by_commit(repo.raw_data['commit']['message'])
            # close_task = Tasks.objects.filter(id=taskid).update(**dict_close_task)


    d = {}
    # Заполнение аукциона
    # for i in range (1,9):
    #     for g in range(1,14):
    #         d['task_id'] = i
    #         d['user_id'] = g
    #         d['time'] = r.randint(120, 300)
    #         if g == r.randint(1,14):
    #             continue
    #         AuctionTask(**d).save()

    # Добавление задачи
    if in_url('make',request):
        dict = {}
        dictionary['project_id'] = request.GET['project_id']
        dict['task_name'] = request.POST['task_name']
        dict['created_ts'] = int(t.time())
        dict['difficult'] = request.POST['diff']
        dict['term'] = request.POST['time']
        dict['project_id'] = 1
        dict['type_id'] = request.POST['type']
        Tasks(**dict).save()
        dictionary1 = {}
        dictionary1['id'] = dict['project_id']
        return render(request,['C:/Users/Andrey/PycharmProjects/SPPR_course_w/hunguaryMethod/templates/relocated/add_task_reloc.html'],dictionary1)




    # Аукцион
    Auct = AuctionTask.objects.all()

    for au in Auct:
        au.user_id = get_fio_user_id(au.user_id)
        # print(au.id)

    dictionary['auct'] = Auct





    # СППР
    for_assigment = [
        [238,259,174,300,143,221],
        [186,172,149,219,187,295],
        [202,149,222,171,171,146],
        [262,218,203,191,266,299],
        [219,150,194,131,144,190],
        [227,283,300,124,216,226]
    ]
    # new = []
    # for fo in for_assigment:
    #     new1 = []
    #     for f in fo:
    #          new1.append(f + random.randint(7,15))
    #     new.append(new1)

    task_matrix = np.array(for_assigment)

    assigment_by_Hun = TaskAssignment(task_matrix, 'Hungary')
    # Матрица
    control_matrix = assigment_by_Hun.task_matrix
    control_i = assigment_by_Hun.row_ind
    control_j = assigment_by_Hun.col_ind
    main_matrix = []

    for i in range(0, len(control_matrix)):
        interface_matrix = []
        for l in range(0, len(control_matrix[i])):
            if i == control_i[i] and l == control_j[i]:
                # control_matrix[i][l] = 300
                interface_matrix.append(str(control_matrix[i][l]) + ' ')
            else:
                interface_matrix.append(str(control_matrix[i][l]))
        main_matrix.append(interface_matrix)
    m = 0
    # for user in users_for_ppr:
    #     times = []
    #     # for i in range(0,len(post)):
    #     #     times.append(user.plain_execute_time+r.randint(0,10))
    #     dict[user.username] = main_matrix[m]
    #     for_assigment.append(times)
    #     m = m + 1
    # dictionary['user_times'] = dict

    dictionary['str'] = control_i
    dictionary['row'] = control_j
    dictionary['cost'] = assigment_by_Hun.min_cost
    dictionary['control_matrix'] = main_matrix






    # isp = Programmers.objects.all()
    # arr = []
    # for sp in isp:
    #     arr.append(sp.firstname)
    #
    # data = []
    # for a in arr:
    #     res = AuctionTask.objects.raw(f'SELECT *,sum(time) as t FROM vkr.auction_task as auct INNER JOIN programmers as users ON users.id = auct.user_id WHERE firstname = "{a}"')
    #     for re in res:
    #         data.append(str(re.t) + ' ' + re.firstname)
    #
    # print(sorted(data))
    #
    # print(sorted(data)[0])
    # print(sorted(data)[1])
    # print(sorted(data)[2])
    # print(sorted(data)[3])
    # print(sorted(data)[4])
    # print(sorted(data)[5])











    return render(request, ['C:/Users/Andrey/PycharmProjects/SPPR_course_w/hunguaryMethod/templates/project_card.html'], dictionary)


def get_fio_user_id(id):
    prog = Programmers.objects.filter(id=id)
    for prog1 in prog:
        fio = prog1.firstname + ' ' + prog1.lastname + ' ' + prog1.surname
    return fio

def gitData(request):
    dictionary = {}

    # используя токен доступа
    # git = Github("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")

    git = Github("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")
    repos = git.get_repo('Andrew3100/BelAvtoProkat2022')

    cmt = repos.get_commit('8b01a8891c45a5ca25fdd6d74dbba1411fb38c54')

    # print(cmt.get_comments())


    # dictionary['data'] = cmt.raw_data['commit']['message'] --- ДАЁТ ДОСТУП К ТЕКСТУ КОММИТА









    return render(request, 'C:/Users/Andrey/PycharmProjects/SPPR_course_w/hunguaryMethod/templates/git.html', dictionary)




def project(request):


    return render(request, 'C:/Users/Andrey/PycharmProjects/SPPR_course_w/hunguaryMethod/templates/home.html',dictionary)







def sppr(request):
    dictionary['task_list'] = Tasks.objects.raw(
        'SELECT * FROM sppr.tasks as tasked INNER JOIN sppr.task_type_ref WHERE task_type_ref.id = tasked.task_type')

    if is_get_param_in_this_url(request.get_full_path_info(), 'start'):
        post = list(request.POST)
        del post[0]
        dictionary['post'] = post
        tasks_for_ppr = Tasks.objects.filter(id__in=post)
        dictionary['tasks_for_ppr'] = tasks_for_ppr
        users_for_ppr = Executors.objects.all()[:len(post)]
        dict = {}
        for_assigment = []

        for user in users_for_ppr:
            times = []
            for i in range(0, len(post)):
                times.append(user.plain_execute_time + r.randint(0, 10))
            dict[user.username] = times
            for_assigment.append(times)
        dictionary['user_times'] = dict

        # Решение задачи о назначениях
        # Numpy структура для обработки матрицы


    return render(request, 'C:/Users/Andrey/PycharmProjects/SPPR_course_w/hunguaryMethod/templates/sppr.html',dictionary)





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


