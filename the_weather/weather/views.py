import requests
from django.shortcuts import render, redirect
from .models import City
OWM_KEY = ''
# Create your views here.
def index(request):
    url = 'http://api.weatherapi.com/v1/current.json?key=4a94268a79094898b56140331233103&q={}&aqi=no'
    err_msg = ''
    message = ''
    message_class = ''
    if request.method == "POST":
        if 'Add' in request.POST:
            new_city = request.POST.get("city")
            print(new_city)
            existing_city_count = City.objects.filter(name=new_city)
            print('ashguvashguvashguvashguvashguvashguvashguvashguvashguvashguvashguvv') #for debugging
            print(existing_city_count)
            r = requests.get(url.format(new_city, OWM_KEY)).json()
            try:
                if r['error']:
                    err_msg = 'Invalid City!'
            except:
                try:
                    db = City(name = new_city)
                    db.save()
                except:
                    print('ashguvashguvashguvashguvashguvashguvashguvashguvashguvashguvashguvv')
                #for debugging
                    err_msg = 'City already exists!'

        elif 'delete' in request.POST:
            city = request.POST.get('delete')
            db = City.objects.filter(name = city)
            db.delete()
            return redirect('/')    
        else:
            print('In else -> ashguvashguvashguvashguvashguvashguvashguvashguvashguvashguvashguvv')
    #for debugging
    if err_msg:
        message = err_msg
        message_class = 'is-danger'
    else:
        message = 'City added Succesfully!'
        message_class = 'is-success'
    cities = City.objects.all()
    weather_data = []
    for city in cities:
        r = requests.get(url.format(city)).json()
        print(r)

        city_weather = {
        'city': r['location']['name'],
        'temperature' : r['current']['temp_c'],
        'icon' : r['current']['condition']['icon'],
        'description' : r['current']['condition']['text']
        }
        weather_data.append(city_weather)
    context = {
    'weather_data': weather_data,
    'message': message,
    'message_class': message_class
    }

    return render(request, 'weather/weather.html', context)