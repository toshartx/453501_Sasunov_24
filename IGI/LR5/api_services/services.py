import requests
from django.conf import settings

class WeatherService:
    """Сервис для работы с OpenWeatherMap API (через прямые запросы)"""
    
    def __init__(self):
        self.api_key = settings.OPENWEATHER_API_KEY
        self.base_url = 'https://api.openweathermap.org/data/2.5/weather'
    
    def get_current_weather(self, city_name):
        """
        Получить текущую погоду для города
        Возвращает словарь с данными о погоде
        """
        try:
            response = requests.get(f"{self.base_url}?q={city_name}&appid={self.api_key}&units=metric&lang=ru")
            
            if response.status_code == 200:
                data = response.json()
                
                return {
                    'city': data['name'],
                    'temperature': round(data['main']['temp']),
                    'feels_like': round(data['main']['feels_like']),
                    'temp_min': round(data['main']['temp_min']),
                    'temp_max': round(data['main']['temp_max']),
                    'humidity': data['main']['humidity'],
                    'wind_speed': data['wind']['speed'],
                    'status': data['weather'][0]['description'],
                    'icon': data['weather'][0]['icon'],
                    'is_success': True
                }
            else:
                return {
                    'is_success': False,
                    'error': f'Город "{city_name}" не найден. Проверьте название.'
                }
        except Exception as e:
            return {
                'is_success': False,
                'error': f'Ошибка подключения: {str(e)}'
            }


class RecipeService:
    """Сервис для работы с TheMealDB API (рецепты)"""
    
    def __init__(self):
        self.base_url = 'https://www.themealdb.com/api/json/v1/1/'
    
    def search_recipes(self, query):
        """Поиск рецептов по названию"""
        try:
            response = requests.get(f'{self.base_url}search.php', params={'s': query})
            data = response.json()
            
            if data.get('meals'):
                recipes = []
                for meal in data['meals']:
                    ingredients = []
                    for i in range(1, 21):
                        ingredient = meal.get(f'strIngredient{i}')
                        measure = meal.get(f'strMeasure{i}')
                        if ingredient and ingredient.strip():
                            ingredients.append(f"{measure} {ingredient}".strip())
                    
                    recipes.append({
                        'id': meal['idMeal'],
                        'name': meal['strMeal'],
                        'category': meal.get('strCategory', 'Не указана'),
                        'area': meal.get('strArea', 'Не указана'),
                        'instructions': meal.get('strInstructions', 'Инструкции нет')[:500],
                        'image': meal['strMealThumb'],
                        'ingredients': ingredients,
                        'youtube': meal.get('strYoutube', ''),
                    })
                return {'is_success': True, 'recipes': recipes, 'count': len(recipes)}
            else:
                return {'is_success': True, 'recipes': [], 'count': 0, 'message': 'Рецепты не найдены'}
        except Exception as e:
            return {'is_success': False, 'error': f'Ошибка: {str(e)}'}