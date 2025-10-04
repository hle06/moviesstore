# petitions/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import MoviePetition

# View to list all petitions
class PetitionListView(ListView):
    model = MoviePetition
    template_name = 'petitions/petition_list.html'
    context_object_name = 'petitions'
    ordering = ['-created_at'] # Show newest first

# View to create a new petition
# LoginRequiredMixin ensures only logged-in users can create a petition
class PetitionCreateView(LoginRequiredMixin, CreateView):
    model = MoviePetition
    template_name = 'petitions/petition_form.html'
    fields = ['movie_title', 'reason'] # Fields the user will fill out
    success_url = reverse_lazy('petitions:list') # Redirect to the list after success

    # This method automatically sets the petition's creator to the current user
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

# This view handles the voting logic
@login_required
def vote_on_petition(request, petition_id):
    # Ensure it's a POST request for security
    if request.method == 'POST':
        petition = get_object_or_404(MoviePetition, pk=petition_id)
        user = request.user
        
        # Check if user has already voted
        if user in petition.voters.all():
            # If they have, remove their vote (allows un-voting)
            petition.voters.remove(user)
        else:
            # If they haven't, add their vote
            petition.voters.add(user)
            
    return redirect('petitions:list')