from .models import Post, Category
from django.db.models import Q

def searchPost(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    # Filter categories based on the search query
    categories = Category.objects.filter(name__icontains=search_query)

    # Filter posts based on the title, content, owner's name, or category
    lst = Post.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(content__icontains=search_query) |  # Use 'content' instead of 'description'
        Q(owner__name__icontains=search_query) |  # Assuming 'owner' is a ForeignKey to Profile or User model
        Q(category__in=categories)
    )

    return lst, search_query
