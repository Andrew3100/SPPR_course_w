from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse
from .models import *
import random as r
import itertools
import numpy as np
from numpy import random
from scipy.optimize import linear_sum_assignment



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
        for_assigment = []

        for user in users_for_ppr:
            times = []
            for i in range(0,len(post)):
                times.append(user.plain_execute_time+r.randint(0,10))
            dict[user.username] = times
            for_assigment.append(times)
        dictionary['user_times'] = dict

        # Решение задачи о назначениях
        # Numpy структура для обработки матрицы
        task_matrix = np.array(for_assigment)
        assigment_by_Hun = TaskAssignment(task_matrix, 'Hungary')
        # Матрица
        control_matrix = assigment_by_Hun.task_matrix
        control_i = assigment_by_Hun.row_ind
        control_j = assigment_by_Hun.col_ind
        main_matrix = []

        for i in range(0, len(control_matrix)):
            interface_matrix = []
            for l in range(0,len(control_matrix[i])):
                if i == control_i[i] and l == control_j[i]:
                    # control_matrix[i][l] = 300
                    interface_matrix.append(str(control_matrix[i][l]) + ' ')
                else:
                    interface_matrix.append(str(control_matrix[i][l]))
            main_matrix.append(interface_matrix)
        m = 0
        for user in users_for_ppr:
            times = []
            # for i in range(0,len(post)):
            #     times.append(user.plain_execute_time+r.randint(0,10))
            dict[user.username] = main_matrix[m]
            for_assigment.append(times)
            m = m + 1
        dictionary['user_times'] = dict

        dictionary['str']  = control_i
        dictionary['row']  = control_j
        dictionary['cost'] = assigment_by_Hun.min_cost
        dictionary['control_matrix'] = main_matrix
    return render(request, 'C:/Users/Andre/PycharmProjects/SPPR_course_w/hunguaryMethod/templates/home.html', dictionary)
