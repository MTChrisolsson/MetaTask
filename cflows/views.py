# cflows/views.py
from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
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