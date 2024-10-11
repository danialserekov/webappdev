from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.db.models import Q
from .utils import searchProfiles
from .models import Profile, Message
from .forms import CustomerUserCreationForm, ProfileForm, InterestForm

def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'Username doesn\'t exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request, 'Username or password is incorrect')
    
    context = {'page': page}
    return render(request, 'users/login-register-page.html', context)


def logoutUser(request):
    logout(request)
    messages.error(request, 'User was logged out!')
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomerUserCreationForm()

    if request.method == 'POST':
        form = CustomerUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created')

            login(request, user)
            return redirect('edit-account')
        
        else:
            messages.success(
                request, 'An error has occured during registration')

    context = {'page': page, 'form': form}
    return render(request, 'users/login-register-page.html', context)

def profiles(request):
    profiles, search_query = searchProfiles(request)

    paginator = Paginator(profiles, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    

    context = {
        'profiles': profiles, 
        'page_obj': page_obj, 
        'search_query': search_query
    }
    return render(request, 'users/profiles.html', context)

def profilePage(request, pk):
    profile = Profile.objects.get(id=pk)
    context = {'profile': profile}
    return render(request, 'users/profile-page.html', context)

@login_required(login_url='login')
def UserAccount(request):
    profile = request.user.profile

    news = profile.post_set.all()

    context = {'profile': profile, 'news': news}
    return render(request, 'users/account.html', context)

@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)  # Change FILE to FILES
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/profile-form.html', context)

@login_required(login_url='login')
def addInterest(request):
    profile = request.user.profile
    form = InterestForm

    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            interest = form.save(commit=False)
            interest.owner = profile
            interest.save()
            messages.success(request, 'Interest was added successfully')
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/interest-form.html', context)

@login_required(login_url='login')
def updateInterest(request, pk):
    profile = request.user.profile
    interest = profile.interests_set.get(id=pk)  # Correctly accessing the interests

    form = InterestForm(instance=interest)

    if request.method == 'POST':
        form = InterestForm(request.POST, instance=interest)
        if form.is_valid():
            form.save()
            messages.success(request, 'Interest was updated successfully')
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/interest-form.html', context)

@login_required(login_url='login')
def deleteInterest(request, pk):
    profile = request.user.profile
    interest = profile.interests_set.get(id=pk)

    if request.method == 'POST':
        interest.delete()
        messages.success(request, 'Interest was deleted successfully')
        return redirect('account')

    context = {'interest': interest}
    return render(request, 'users/interest-delete.html', context)

@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequests': messageRequests, 'unreadCount': unreadCount}
    return render(request, 'users/inbox.html', context)

@login_required(login_url='login')
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message': message}

    return render(request, 'users/message.html', context)