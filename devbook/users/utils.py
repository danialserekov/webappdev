from .models import Profile, Interests
from django.db.models import Q
from django.core.paginator import Paginator


def searchProfiles(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    # Get all profiles related to the searched interest
    interests = Interests.objects.filter(name__icontains=search_query)

    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) | 
        Q(short_intro__icontains=search_query) |
        Q(interests__in=interests)  # Use `interests` for the reverse ForeignKey relationship
    ) 

    
    return profiles, search_query