from django.shortcuts import redirect, render
from .models import City, Judje, Sportsman, Trainer,Team
from .forms import SportsmanForm


def index(request):
    cities = Team.objects.all()
    return render(request, 'Mezhik/index.html', {'title': 'Main part of site', 'cities': cities})

def about(request):
    return render(request, 'Mezhik/about.html')

def city(request):
    cities = Team.objects.all()
    return render(request, 'Mezhik/city.html', {'title': 'Cities', 'cities': cities})

def sportsman(request):
    sportsman = Sportsman.objects.all()
    return render(request, 'Mezhik/sportsman.html',{'title': 'Sportsman info', 'sportsman': sportsman})

def create(request):
    error =''
    if request.method == 'POST':
        form =SportsmanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            error ='Incorrect Form'
    form = SportsmanForm()
    context = {
        'form' : form,
        'error': error
    }
    return render(request, 'Mezhik/create.html', context)

def request(request):
    return render(request, 'Mezhik/request.html', {'title' : 'Requests SQL'})

def request1(request):
    sportsman = Sportsman.objects.filter(city ='1')
    return render(request, 'Mezhik/request1.html', {'title' : 'Requset #2', 'sportsman': sportsman})

def request2(request):
    trainer = Trainer.objects.filter(team ='1')
    trainer1 = Trainer.objects.all()
    return render(request, 'Mezhik/request2.html',{'title': 'Request #3', 'trainer': trainer, 'trainer1': trainer1})

def request3(request):
    sportsman = Sportsman.objects.exclude(sex ='M')
    return render(request, 'Mezhik/request3.html',{'title': 'Request #4', 'sportsman': sportsman})
def request4(request):
    sportsman = Sportsman.objects.filter(city ='3', team ='1')
    return render(request, 'Mezhik/request4.html',{'title': 'Request #5', 'sportsman': sportsman})
def request5(request):
    sportsman = Sportsman.objects.filter(sportsman_name ="Stepan Bandera")
    judje = Judje.objects.filter
    return render(request, 'Mezhik/request4.html',{'title': 'Request #1.1', 'sportsman': sportsman})
