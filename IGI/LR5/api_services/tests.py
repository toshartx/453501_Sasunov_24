from django.test import TestCase
from django.contrib.auth.models import User
from unittest.mock import patch, Mock
from .services import WeatherService, RecipeService


class WeatherServiceTest(TestCase):
    def setUp(self):
        self.service = WeatherService()
    
    @patch('api_services.services.requests.get')
    def test_get_current_weather_success(self, mock_get):
        """Успешный запрос погоды"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'name': 'Minsk',
            'main': {
                'temp': 18.5,
                'feels_like': 17.2,
                'temp_min': 15.0,
                'temp_max': 20.0,
                'humidity': 65
            },
            'wind': {'speed': 3.5},
            'weather': [{'description': 'облачно', 'icon': '04d'}]
        }
        mock_get.return_value = mock_response
        
        result = self.service.get_current_weather('Minsk')
        
        self.assertTrue(result['is_success'])
        self.assertEqual(result['city'], 'Minsk')
    
    @patch('api_services.services.requests.get')
    def test_get_current_weather_city_not_found(self, mock_get):
        """Город не найден"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        result = self.service.get_current_weather('InvalidCity')
        
        self.assertFalse(result['is_success'])
        self.assertIn('не найден', result['error'])
    
    @patch('api_services.services.requests.get')
    def test_get_current_weather_exception(self, mock_get):
        """Ошибка соединения"""
        mock_get.side_effect = Exception('Connection error')
        
        result = self.service.get_current_weather('Minsk')
        
        self.assertFalse(result['is_success'])
        self.assertIn('Ошибка', result['error'])


class RecipeServiceTest(TestCase):
    def setUp(self):
        self.service = RecipeService()
    
    @patch('api_services.services.requests.get')
    def test_search_recipes_success(self, mock_get):
        """Успешный поиск рецептов"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'meals': [
                {
                    'idMeal': '123',
                    'strMeal': 'Chocolate Cake',
                    'strCategory': 'Dessert',
                    'strArea': 'American',
                    'strInstructions': 'Mix and bake...',
                    'strMealThumb': 'http://example.com/cake.jpg',
                    'strIngredient1': 'Flour',
                    'strMeasure1': '2 cups',
                    'strYoutube': 'http://youtube.com'
                }
            ]
        }
        mock_get.return_value = mock_response
        
        result = self.service.search_recipes('cake')
        
        self.assertTrue(result['is_success'])
        self.assertEqual(result['count'], 1)
        self.assertEqual(result['recipes'][0]['name'], 'Chocolate Cake')
    
    @patch('api_services.services.requests.get')
    def test_search_recipes_not_found(self, mock_get):
        """Рецепты не найдены"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'meals': None}
        mock_get.return_value = mock_response
        
        result = self.service.search_recipes('nonexistentdishxyz')
        
        self.assertTrue(result['is_success'])
        self.assertEqual(result['count'], 0)
    
    @patch('api_services.services.requests.get')
    def test_search_recipes_exception(self, mock_get):
        """Ошибка API"""
        mock_get.side_effect = Exception('API error')
        
        result = self.service.search_recipes('cake')
        
        self.assertFalse(result['is_success'])
        self.assertIn('Ошибка', result['error'])

class ApiViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_weather_page_redirect_for_anonymous(self):
        """Анонимный пользователь перенаправляется на логин"""
        response = self.client.get('/api/weather/')
        self.assertEqual(response.status_code, 302)
    
    def test_weather_page_authenticated(self):
        """Авторизованный пользователь видит страницу погоды"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/api/weather/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'api_services/weather.html')
    
    def test_weather_post_authenticated(self):
        """POST-запрос погоды с городом"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post('/api/weather/', {'city': 'Minsk'})
        self.assertEqual(response.status_code, 200)
    
    def test_recipes_page_redirect_for_anonymous(self):
        """Анонимный пользователь перенаправляется на логин"""
        response = self.client.get('/api/recipes/')
        self.assertEqual(response.status_code, 302)
    
    def test_recipes_page_authenticated(self):
        """Авторизованный пользователь видит страницу рецептов"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/api/recipes/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'api_services/recipes.html')
    
    def test_recipes_search_authenticated(self):
        """Поиск рецептов"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/api/recipes/?q=cake')
        self.assertEqual(response.status_code, 200)