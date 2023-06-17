from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.shortcuts import render, get_object_or_404

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse_lazy

from .forms import LoginForm, CreateCenterForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect

from .models import Center


def is_admin(user):
    return user.groups.filter(name='Admin').exists()


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if is_admin(user):
                    return redirect('admin_home')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


@login_required(login_url='login')
def home_view(request):
    username = request.user.username
    return render(request, 'regular_home.html', {'username': username})


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='access_denied')
def admin_home_view(request):
    username = request.user.username
    return render(request, 'admin_home.html', {'username': username})


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='access_denied')
def create_center_view(request):
    if request.method == 'POST':
        form = CreateCenterForm(request.POST)
        if form.is_valid():
            center_name = form.cleaned_data['center_name']
            start_hour = form.cleaned_data['start_hour']
            start_minute = form.cleaned_data['start_minute']
            end_hour = form.cleaned_data['end_hour']
            end_minute = form.cleaned_data['end_minute']

            center = Center(
                center_name=center_name,
                start_hour=start_hour,
                start_minute=start_minute,
                end_hour=end_hour,
                end_minute=end_minute
            )
            center.save()

            return redirect('admin_center_list')

    else:
        form = CreateCenterForm()

    return render(request, 'create_center.html', {'form': form})


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect(reverse_lazy('login'))


@login_required(login_url='login')
def center_list(request):
    centers = Center.objects.all()
    data = {'centers': centers, 'bookable': (not request.user.centers.exists())}
    if request.user.centers.exists():
        data={'centers': centers, 'bookable': (not request.user.centers.exists()),'booking':request.user.centers.first()}
    return render(request, 'center_list.html', data)


def access_denied_view(request):
    return render(request, 'access_denied.html')


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='access_denied')
def admin_center_list(request):
    centers = Center.objects.all()
    return render(request, 'admin_center_list.html', {'centers': centers})


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='access_denied')
def delete_center(request, center_id):
    center = get_object_or_404(Center, id=center_id)

    if request.method == 'POST':
        # Delete the center
        center.delete()

    return redirect('admin_center_list')


@login_required(login_url='login')
def book_center(request, center_id):
    center = get_object_or_404(Center, id=center_id)
    if center.applicants.count() < 10 and (not request.user.centers.exists()):
        center.applicants.add(request.user)
    return redirect('center_list')

def welcome(request):
    return render(request, 'welcome.html')