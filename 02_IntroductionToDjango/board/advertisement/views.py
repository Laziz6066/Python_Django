from django.shortcuts import render

def advertisement_list(request):
    return render(request, 'advertisement/advertisement_list.html')

def classes(request):
    return render(request, 'advertisement/classes.html')

def dictionaries(request):
    return render(request, 'advertisement/dictionaries.html')

def functions(request):
    return render(request, 'advertisement/functions.html')

def list(request):
    return render(request, 'advertisement/list.html')

def tuples(request):
    return render(request, 'advertisement/tuples.html')