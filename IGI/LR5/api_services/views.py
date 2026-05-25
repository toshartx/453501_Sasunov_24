from django.shortcuts import render
from .services import WeatherService, RecipeService

def weather(request):
    """Страница с прогнозом погоды"""
    weather_data = None
    
    if request.method == 'POST':
        city = request.POST.get('city', '').strip()
        if city:
            weather_service = WeatherService()
            weather_data = weather_service.get_current_weather(city)
    
    return render(request, 'api_services/weather.html', {'weather': weather_data})


def recipes(request):
    """Страница поиска рецептов"""
    recipes_data = None
    search_query = ''
    
    if request.method == 'GET' and request.GET.get('q'):
        search_query = request.GET.get('q', '').strip()
        if search_query:
            recipe_service = RecipeService()
            recipes_data = recipe_service.search_recipes(search_query)
    
    return render(request, 'api_services/recipes.html', {
        'recipes_data': recipes_data,
        'search_query': search_query
    })