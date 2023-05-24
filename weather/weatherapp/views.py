from django.shortcuts import render, redirect
from .models import City
import json
import urllib.request

# Create your views here.

def index(request):

    weather_data = []
    err_msg = ''
    message = ''
    deleted_msg = ''
    message_class = ''
    data = []

    if request.method == 'POST':
        if 'Add' in request.POST:
            city = request.POST['city']
            try:
                if City.objects.filter(name=city).exists():
                    err_msg = 'City already exists!'
                else:
                    url = 'http://api.weatherapi.com/v1/current.json?key=7b5f89d1b9be4c95b1961439232405&q=' + city + '&aqi=no'
                    res = urllib.request.urlopen(url)
                    City(name=city).save()
            except urllib.error.HTTPError as e:
                if e.code == 400:
                    err_msg = 'Invalid city name'
        else:
            city = request.POST.get('delete')
            City.objects.filter(name=city).delete()
            deleted_msg = 'City Deleted succesfully!'
            
    if err_msg:
        message = err_msg
        message_class = 'is-danger'
    elif deleted_msg:
        message = deleted_msg
        message_class = 'is-success'
    else:
        message = 'City Added successfully'
        message_class = 'is-success'


    cities = City.objects.all()
    for city in cities:
            name = city.name
            url = 'http://api.weatherapi.com/v1/current.json?key=7b5f89d1b9be4c95b1961439232405&q=' + name + '&aqi=no'
            res = urllib.request.urlopen(url)
            json_data = json.load(res)
            city_weather = {
                'name' : json_data['location']['name'],
                'country' : json_data['location']['country'],
                'temperature' : json_data['current']['temp_c'],
                'icon' : json_data['current']['condition']['icon'],
                'description' : json_data['current']['condition']['text']
            }
            weather_data.append(city_weather)   
        
    data = {
        'weather_data' : weather_data,
        'message_class' : message_class,
        'message' : message,
    }

    return render(request, 'index.html', data)
