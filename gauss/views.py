from django.shortcuts import render

def index(request):
  context = {
    'rows': None,
    'number_of_rows': 0,
    'info': 'Gauss method matrice calculation.',
    'type': '',
  }

  if request.method == 'POST':
    # if request.POST['rownum']:
    rows_from_input = request.POST.get('rows')
    if rows_from_input != '':
      number_of_rows = int(rows_from_input)
      context['rows'] = range(1, number_of_rows + 1)
      context['number_of_rows'] = number_of_rows
      context['type'] = isinstance(number_of_rows, int)
    else:
      context['number_of_rows'] = 0
    # elif request.POST['calculate']:


  return render(request, "gauss/index.html", context)


