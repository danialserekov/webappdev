from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import PostSerializer
from blog.models import Post, Review

@api_view(['GET'])
def getRoutes(request):

    routes = [
        {'GET': 'api/news'},
        {'GET': 'api/news/post/id'},
        {'POST': 'api/news/post/id/vote'},

        {'POST': 'api/users/token'},
        {'POST': 'api/users/token/refresh'},
    ]
    return Response(routes)

@api_view(['GET'])
def getNews(request):
    news = Post.objects.all()
    serializer = PostSerializer(news, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getPost(request, pk):
    post = Post.objects.get(id=pk)
    serializer = PostSerializer(post, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def postVote(request, pk):
    post = Post.objects.get(id=pk)
    user = request.user.profile
    data = request.data

    review, published_date = Review.objects.get_or_create(
        owner=user,
        post=post,
    )

    review.value = data['value']
    review.save()
    post.getVoteCount

    print('DATA:', data)

    serializer = PostSerializer(post, many=False)
    return Response(serializer.data)