from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Length # Import Length for character count sorting

def index(request):
    search_term = request.GET.get('search')
    # Get the sort_by parameter from the URL, defaulting to 'name_asc'
    sort_by = request.GET.get('sort_by', 'name_asc') 
    
    # --- Base Queryset ---
    if search_term:
        movies_list = Movie.objects.filter(name__icontains=search_term)
    else:
        movies_list = Movie.objects.all()

    # --- Sorting Logic ---
    sort_name = 'Title (A-Z)' # Default display name
    
    if sort_by == 'name_asc':
        # Sort by title alphabetically ascending (A-Z)
        movies_list = movies_list.order_by('name')
        sort_name = 'Title (A-Z)'
    elif sort_by == 'name_desc':
        # Sort by title alphabetically descending (Z-A) - Reverse Alphabetical
        movies_list = movies_list.order_by('-name')
        sort_name = 'Title (Z-A)'
    elif sort_by == 'length_asc':
        # Sort by title length ascending (Shortest First)
        # Annotate (calculate) the length and then order by it
        movies_list = movies_list.annotate(name_len=Length('name')).order_by('name_len')
        sort_name = 'Title Length (Shortest First)'
    elif sort_by == 'length_desc':
        # Sort by title length descending (Longest First)
        movies_list = movies_list.annotate(name_len=Length('name')).order_by('-name_len')
        sort_name = 'Title Length (Longest First)'

    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies_list
    template_data['current_sort'] = sort_by # Pass current sort for UI highlighting
    template_data['sort_name'] = sort_name # Pass display name for UI
    template_data['search_term'] = search_term # Pass search term back for link construction
    
    return render(request, 'movies/index.html', {'template_data': template_data})

def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)
    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    return render(request, 'movies/show.html', {'template_data': template_data})
@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)
@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html',
            {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)
@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id,
        user=request.user)
    review.delete()
    return redirect('movies.show', id=id)