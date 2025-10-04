# petitions/urls.py
from django.urls import path
from .views import PetitionListView, PetitionCreateView, vote_on_petition

app_name = 'petitions'

urlpatterns = [
    path('', PetitionListView.as_view(), name='list'),
    path('new/', PetitionCreateView.as_view(), name='create'),
    path('<int:petition_id>/vote/', vote_on_petition, name='vote'),
]