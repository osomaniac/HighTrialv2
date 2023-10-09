from django.urls import path
from . import views
from HighTrialMain import views as ht_views


app_name = 'dogs_app'

urlpatterns = [
    path('', views.dogs, name='dogs'),
    path('<int:dog_id>/', views.dog, name='dog'),
    path('breed-dogs/', views.breedDogs, name="breed-dogs"),
    path('litter/<int:dam_id>to<int:sire_id>', views.breedingResults, name="view-litter"),
    path('edit-dog/<int:dog_id>', views.editDog, name="edit-dog"),
    path('litter/<int:litter_id>', views.litter, name="litter")
]