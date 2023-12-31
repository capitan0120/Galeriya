from django.shortcuts import render, redirect
from .models import Category, Photo
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm

def loginUser(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('galeriya')

    return render(request, 'photo/login_register.html', {'page': page})


def logoutUser(request):
    logout(request)
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            if user is not None:
                login(request, user)
                return redirect('galeriya')

    context = {'form': form, 'page': page}
    return render(request, 'photo/login_register.html', context)
@login_required(login_url='login')
def galeriya(request):
    user = request.user
    category = request.GET.get('category')
    if category == None:
        photos = Photo.objects.filter(category__user=user)
    else:
        photos = Photo.objects.filter(category__name=category, category__user=user)
    categories = Category.objects.all()
    context = {
        "categories": categories,
        "photos": photos,
    }
    return render(request, 'photo/galeriya.html', context)
@login_required(login_url='login')
def viewPhoto(request, pk):
    photo = Photo.objects.get(id=pk)
    return render(request, 'photo/photo.html', {
        'photo': photo,
    })
@login_required(login_url='login')
def addPhoto(request):
    user = request.user
    categories = user.category_set.all()

    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['new_category'] != '':
            category, created = Category.objects.get_or_create(user=user, name=data['new_category'])
        else:
            category = None

        photo = Photo.objects.create(
            category=category,
            description=data['description'],
            image=image,
        )

        return redirect('galeriya')

    context = {
        'categories': categories
    }
    return render(request, 'photo/add.html', context)
