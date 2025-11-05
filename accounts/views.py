from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home_index')  # Redirect to home page after registration
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'Logged out successfully!')
        return redirect('home_index')
    return redirect('home_index')
