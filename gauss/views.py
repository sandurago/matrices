from django.shortcuts import render
from .models import User, Result, GaussForm
import numpy as np
import datetime, pytz
from django import forms
from .forms.sample import SampleForm

def index(request):
  context = {
    'range_for_rows': None,
    'range_for_columns': None,
    'number_of_rows': 0,
    'number_of_columns': 0,
    'info': 'Gauss method matrix calculation.',
    'initial_matrix': None,
    'matrix_after_transformations': None,
    'result': float(request.POST.get('result', 0)),
    'err': None,
    'isSave': False,
  }

  if request.method == 'POST':
    rows_from_input = request.POST.get('rows', 0)
    number_of_rows = int(rows_from_input)
    number_of_columns = number_of_rows + 1

    context['range_for_rows'] = range(1, number_of_rows + 1)
    context['range_for_columns'] = range(1, number_of_columns + 1)

    context['number_of_rows'] = number_of_rows
    context['number_of_columns'] = number_of_columns

    if 'calculate' in request.POST:
      matrix = list()
      for i in context['range_for_rows']:
        row = list()
        for j in context['range_for_columns']:
          number = float(request.POST.get('num-' + str(i) + str(j)))
          row.append(number)
        matrix.append(row)

      matrix = np.array(matrix)
      context['initial_matrix'] = np.copy(matrix)

      for i in range(0, context['number_of_rows']-1):
        index = i+1;
        for j in range(index, context['number_of_rows']):
          if matrix[i][i] == 0 and i == 0:
            matrix[[i, j]] = matrix[[j, i]]
          elif matrix[i][i] == 0 and i != 0:
            matrix[[j, i]] = matrix[[i, j]]

          num = matrix[j][i] / matrix[i][i]
          matrix[j] = matrix[j] - (matrix[i] * num)

      num = context['number_of_rows']-1
      res = list()
      for i in range(num, -1, -1):
        calc = 0
        for j in range(num+1, -1, -1):
          if i != j:
            calc += matrix[i][j]
        if matrix[i][i] != 0:
          x = calc/matrix[i][i]
          res.insert(0, round(float(x), 2))
        else:
          context['err'] = 'Division by zero attempted. Cannot apply Gauss elimination!'
          res = None
          break
      context['matrix_after_transformations'] = np.round(matrix, 2)

      context['result'] = res

    if 'save' in request.POST:
      user = request.POST.get('username')

      if_exists = User.objects.filter(username = user)
      tz = pytz.timezone('Europe/Paris')
      now = datetime.datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')

      if if_exists:
        u = User.objects.get(username = user)
        items = context['result']
        print(items)
        if items != None:
          print('here')
          for i in range(len(items)):
            print('inside')
            r = Result(date = now, result = items[i], user_id = u.pk)
            r.save()
            print(r)

    context['test'] = ' lol'


  return render(request, "gauss/index.html", context)


def sample(request):
  rows = request.POST.get('rows')
  values = request.POST.getlist('values')
  context = {
    'nb_rows': rows,
    'rows': range(0) if rows is None else range(int(rows)),
    'values': list(map(int, values))
  }
  return render(request, 'gauss/sample-form.html', context)
