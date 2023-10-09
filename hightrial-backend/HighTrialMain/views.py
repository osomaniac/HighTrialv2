from django.shortcuts import render
from dogs.models import Dog, Kennel, ColorGenetics, Wallet, Litter, User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

# Create your views here.
def index(request):
    return render(request, 'hightrial/index.html')
    
class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
    
def userProfile(request, owner_id):
    owner = User.objects.get(id=owner_id)
    dogs = Dog.objects.filter(owner=owner)
    kennelName = Kennel.objects.filter(owner=owner).first()
    wallet = Wallet.objects.filter(owner=owner).first()
    cash = wallet.money
    tickets = wallet.tickets
    litters = Litter.objects.filter(breeder=owner)
    context = {'username': owner.username, 'dogs':dogs, 'kennelName':kennelName, 'cash':cash, 'tickets':tickets, 'litters':litters}
    return render(request, 'users/profile.html', context)