# cflows/views.py
from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from .models import Car

def index(request):
    # Renderar mallen cflows/templates/cflows/cflows_index.html
    return render(request, 'cflows/cflows_index.html')



class CarListView(LoginRequiredMixin, ListView):
    model = Car
    template_name = 'cflows/car_list.html'
    context_object_name = 'cars'

    def get_queryset(self):
        # KRITISK FILTRERING:
        # Hämta endast bilar som tillhör den inloggade användarens organisation
        user = self.request.user
        
        # Kontrollera att användaren har en organisation (om den inte är en superanvändare)
        if user.is_authenticated and user.organization:
            return Car.objects.filter(organization=user.organization)
        
        # Försäkra dig om att inga data visas om användaren saknar organisation
        return Car.objects.none()
    
class CarDetailView(LoginRequiredMixin, ListView):
    model = Car
    template_name = 'cflows/car_detail.html'
    context_object_name = 'car'

    def get_queryset(self):
        user = self.request.user
        
        if user.is_authenticated and user.organization:
            return Car.objects.filter(organization=user.organization)
        
        return Car.objects.none()
    
@login_required
def create_car(request):
    # Logik för att skapa en ny bilpost
    if request.method == 'POST':
        # Hantera formulärdata och skapa en ny Car-post
        make = request.POST.get('make')
        model = request.POST.get('model')
        registration_number = request.POST.get('registration_number')
        registration_number = registration_number.upper()
        color = request.POST.get('color')
        year = request.POST.get('year')
        mileage = request.POST.get('mileage')

        # Skapa en ny Car-instans
        car = Car.objects.create(
            organization=request.user.organization,
            make=make,
            model=model,
            registration_number=registration_number,
            color=color,
            year=year,
            mileage=mileage
        )

        # Om du vill omdirigera efter skapandet
        return redirect('car_detail', pk=car.pk)

    return render(request, 'cflows/car_form.html')

@login_required
def car_list(request):
    # Logik för att lista bilar
    cars = Car.objects.filter(organization=request.user.organization)
    return render(request, 'cflows/car_list.html', {'cars': cars})


@login_required
def car_filter(request):
    # Get initial queryset
    cars = Car.objects.filter(organization=request.user.organization)
    
    # Get filter values
    filters = {
        'make': request.GET.get('make', ''),
        'model': request.GET.get('model', ''),
        'year': request.GET.get('year', '')
    }
    
    # Apply filters
    if filters['make']:
        cars = cars.filter(make__icontains=filters['make'])
    if filters['model']:
        cars = cars.filter(model__icontains=filters['model'])
    if filters['year']:
        cars = cars.filter(year=filters['year'])
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'cflows/car_list_partial.html', {'cars': cars})
    
    return render(request, 'cflows/cflows_index.html', {
        'cars': cars,
        'filters': filters
    })