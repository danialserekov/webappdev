from django.db import models
from django.utils import timezone
import uuid
from users.models import Profile

class Post(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
                          primary_key=True, editable=False)
    owner = models.ForeignKey(
        Profile, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    content = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(
        null=True, blank=True, default="default.jpg")
    category = models.ManyToManyField('Category', blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-vote_ratio', '-vote_total', 'title']

    @property
    def reviewers(self):
        queryset = self.review_set.all().value_list('owner__id', flat=True)
        return queryset

    @property
    def getvoteCount(self):
        reviews = self.review_set.all()
        totalVotes = reviews.count()

        if totalVotes > 0:  # Avoid division by zero
            upVotes = reviews.filter(value='up').count()
            ratio = (upVotes / totalVotes) * 100
        else:
            upVotes = 0
            ratio = 0

        self.vote_total = totalVotes
        self.vote_ratio = ratio

        self.save()

    

class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Like'),
        ('down', 'Dislike'),
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    published_date = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
                          primary_key=True, editable=False)
    
    class Meta:
        unique_together = [['owner', 'post']]
    
    def __str__(self):
        return self.value
    
class Category(models.Model):
    name = models.CharField(max_length=200)
    published_date = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
                          primary_key=True, editable=False)
    
    def __str__(self):
        return self.name


