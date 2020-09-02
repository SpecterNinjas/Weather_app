from django.shortcuts import render,redirect
import requests
from .models import City
from .forms import CityForm


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=e173943de671729fb2e5bd512e755ba5'
    message = ''
    mesg_err = ''
    message_class = ''
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']

            city_count = City.objects.filter(name=new_city).count()
            if city_count == 0:
                res = requests.get(url.format(new_city)).json()
                if res['cod'] == 200:
                    form.save()
                else:
                    mesg_err = "This city does not exit in the World!"
            else:
                mesg_err = "This city already exists!"
    cities = City.objects.all()
    weather_data = []
    form = CityForm()
    for city in cities:
        r = requests.get(url.format(city)).json()
        city_weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'icon': r['weather'][0]['icon'],
            'description': r['weather'][0]['description'],
        }
        weather_data.append(city_weather)

        if mesg_err:
            message = mesg_err
            message_class = 'is-danger'
        else:
            message = "City Weather added succesfully!"
            message_class = 'is-success'

    context = {'weather_data': weather_data, 'form': form, 'message': message, message_class: "message_class"}
    return render(request, 'the_weather/index.html', context)


def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect("index")
