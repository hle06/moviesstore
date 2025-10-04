# petitions/models.py
from django.db import models
from django.conf import settings # More robust way to get the User model

class MoviePetition(models.Model):
    # Title of the movie being requested
    movie_title = models.CharField(max_length=200)

    # A short reason or description for the petition
    reason = models.TextField()

    # The user who created the petition
    # on_delete=models.CASCADE means if the user is deleted, their petitions are deleted too.
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Automatically set the creation date
    created_at = models.DateTimeField(auto_now_add=True)

    # This is the magic for voting. It links to all users who have voted.
    # We can easily get the vote count with petition.voters.count()
    voters = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='voted_petitions', blank=True)

    def __str__(self):
        return self.movie_title

    @property
    def total_votes(self):
        return self.voters.count()