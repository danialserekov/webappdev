from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import Http404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from .models import Post, Review, Category
from .forms import PostForm, ReviewForm
from .utils import searchPost


def blogList(request):
    lst, search_query = searchPost(request)
    
    news = lst.order_by('-published_date') 

    paginator = Paginator(news, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'news': news, 
        'page_obj': page_obj, 
        'search_query': search_query
    }

    return render(request, 'blog/blog-list.html', context)

def postPage(request, pk):
    postObj = Post.objects.get(id=pk)
    form = ReviewForm()

    # Check if the user is authenticated and retrieve their existing review
    existing_review = None
    if request.user.is_authenticated:
        existing_review = postObj.review_set.filter(owner=request.user.profile).first()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.post = postObj
            review.owner = request.user.profile  # Ensure that the user is authenticated and has a profile
            if existing_review:
                # Update existing review
                existing_review.body = review.body
                existing_review.value = review.value  # Assuming you have a value field for like/dislike
                existing_review.save()
            else:
                review.save()

            # Update the post vote count
            postObj.getvoteCount  

            messages.success(request, 'Your review was successfully submitted.')
            return redirect('post-page', pk=postObj.id)  # Redirect to the same post page

    # Pre-fill the form with the existing review if it exists
    if existing_review:
        form = ReviewForm(initial={'body': existing_review.body, 'value': existing_review.value})

    return render(request, 'blog/post-page.html', {
        'postObj': postObj,
        'form': form,
        'existing_review': existing_review  # Pass existing review to the template
    })




@login_required(login_url='login')
def createPost(request):
    profile = request.user.profile
    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = profile
            post.save()
            return redirect('blog-list')
        
    context = {'form': form}
    return render(request, 'blog/post-form.html', context)

@login_required(login_url='login')
def updatePost(request, pk):
    profile = request.user.profile
    post = profile.post_set.get(id=pk)
    form = PostForm(instance=post)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog-list')
        
    context = {'form': form}
    return render(request, 'blog/post-form.html', context)

@login_required(login_url='login')
def deletePost(request, pk):
    profile = request.user.profile
    post = profile.post_set.get(id=pk)

    if request.method == 'POST':
        post.delete()
        return redirect('blog-list')
    context = {'object': post}
    return render(request, 'blog/post-delete.html', context)