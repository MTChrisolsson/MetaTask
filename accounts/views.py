from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from .models import Organization, Account
from .forms import AddMemberForm, UserRegistrationForm


def register_view(request):
    if  request.user.is_authenticated:
        return redirect('home_index')
    """
    Registers a new user.
    """

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
def profile_index(request):
    return render(request, 'accounts/profile_index.html', {'user': request.user})


@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'Logged out successfully!')
        return redirect('home_index')
    return redirect('home_index')

@login_required
def organization_add_member(request, slug):
    org = get_object_or_404(Organization, slug=slug)
    if not request.user.is_staff:
        return redirect('/') # Or raise 403

    if request.method == 'POST':
        form = AddMemberForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].lower()
            first = form.cleaned_data['first_name'] or ''
            last = form.cleaned_data['last_name'] or ''
            password = form.cleaned_data['password1']
            acct = Account.objects.filter(email=email).first()
            if acct:
                if acct.organization and acct.organization != org:
                    messages.error(request, "User already belongs to another organization.")
                else:
                    acct.organization = org
                    acct.save()
                    messages.success(request, "Existing user assigned to organization.")
            else:
                acct = Account.objects.create_user(
                    email=email,
                    password=password if password else None,
                    first_name=first,
                    last_name=last,
                    organization=org
                )
                messages.success(request, "New user created and assigned.")
            return redirect('org_add_member', slug=org.slug)
    else:
        form = AddMemberForm()

    context = {
        'organization': org,
        'form': form,
        'members': org.members.all(),
    }
    return render(request, 'accounts/organization_add_member.html', context)