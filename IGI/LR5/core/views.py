from django.shortcuts import render
from .models import News

def home(request):
    """Главная страница с последней новостью"""
    latest_news = News.objects.filter(is_published=True).first()
    return render(request, 'core/home.html', {'latest_news': latest_news})


from .models import CompanyHistory, CompanyRequisite

def about(request):
    """Страница 'О компании'"""
    history = CompanyHistory.objects.all()
    requisites = CompanyRequisite.objects.all()
    return render(request, 'core/about.html', {
        'history': history,
        'requisites': requisites,
    })

from django.shortcuts import get_object_or_404

def news_list(request):
    """Список всех новостей"""
    news_list = News.objects.filter(is_published=True)
    return render(request, 'core/news_list.html', {'news_list': news_list})

def news_detail(request, news_id):
    """Детальная страница новости"""
    news = get_object_or_404(News, id=news_id, is_published=True)
    return render(request, 'core/news_detail.html', {'news': news})

from .models import Glossary

def glossary_list(request):
    """Словарь терминов"""
    terms = Glossary.objects.filter(is_published=True)
    return render(request, 'core/glossary_list.html', {'terms': terms})

from .models import Contact

def contacts(request):
    """Страница контактов"""
    employees = Contact.objects.all()
    return render(request, 'core/contacts.html', {'employees': employees})

def privacy(request):
    """Страница политики конфиденциальности"""
    return render(request, 'core/privacy.html')

from .models import Vacancy

def vacancies(request):
    """Страница вакансий"""
    vacancies_list = Vacancy.objects.filter(is_active=True)
    return render(request, 'core/vacancies.html', {'vacancies': vacancies_list})

from .models import Review
from .forms import ReviewForm
from django.shortcuts import redirect

def reviews(request):
    """Страница отзывов с формой добавления"""
    reviews_list = Review.objects.filter(is_published=True)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:reviews')
    else:
        form = ReviewForm()
    
    return render(request, 'core/reviews.html', {
        'reviews': reviews_list,
        'form': form
    })

from .models import PromoCode
from django.utils import timezone

def promocodes(request):
    """Страница промокодов"""
    now = timezone.now()
    active_codes = PromoCode.objects.filter(is_active=True, valid_from__lte=now, valid_to__gte=now)
    archive_codes = PromoCode.objects.filter(is_active=False) | PromoCode.objects.filter(valid_to__lt=now)
    
    return render(request, 'core/promocodes.html', {
        'active_codes': active_codes,
        'archive_codes': archive_codes
    })


from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .forms import RegistrationForm, LoginForm

def register(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('core:home')
    else:
        form = RegistrationForm()
    return render(request, 'core/register.html', {'form': form})


def user_login(request):
    """Вход пользователя"""
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('core:home')
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})


def user_logout(request):
    """Выход пользователя"""
    logout(request)
    return redirect('core:home')


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Client

@login_required
def profile(request):
    """Личный кабинет пользователя"""
    # Получаем или создаём клиента для пользователя
    client, created = Client.objects.get_or_create(user=request.user)
    orders = client.orders.all()
    
    return render(request, 'core/profile.html', {
        'client': client,
        'orders': orders
    })