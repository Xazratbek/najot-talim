from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Post
from rest_framework import status
from .serializers import PostSerializer
from django.shortcuts import get_object_or_404



class PostListView(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts,many=True)
        return Response(
            {
                "status": status.HTTP_200_OK,
                "data":serializer.data
            }
        )

class PostCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        serializer = PostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": status.HTTP_201_CREATED,
                "message":"Post qo'shildi",
                "data": serializer.data
            },status=status.HTTP_201_CREATED)
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class PostUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request,pk):
        post = get_object_or_404(Post,pk=pk)
        if post.author != request.user:
            return Response({"error": "Siz faqat o'zingizning postingizni tahrirlashingiz mumkin!"},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = PostSerializer(data=request.data,context={"request": request},instance=post)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": status.HTTP_200_OK,
                "message": "Post yangilandi",
                "post":serializer.data
            })

        return Response({
        "status": status.HTTP_400_BAD_REQUEST,
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request,pk):
        post = get_object_or_404(Post,pk=pk)
        if post.author != request.user:
            return Response({"error": "Siz faqat o'zingizning postingizni tahrirlashingiz mumkin!"},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = PostSerializer(data=request.data,context={"request":request},instance=post,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": status.HTTP_200_OK,
                "message":"Qisman yangilandi"
            })

        return Response({
        "status": status.HTTP_400_BAD_REQUEST,
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

class PostDeleteView(APIView):
    def delete(self, request,pk):
        post =  get_object_or_404(Post,pk=pk)
        if post.author != request.user:
            return Response({"error": "Siz faqat o'zingizning postingizni tahrirlashingiz mumkin!"},
                            status=status.HTTP_403_FORBIDDEN)
        if post:
            post.delete()
            return Response({
                "status": status.HTTP_204_NO_CONTENT,
                "message":"Post o'chirildi"
            })
        return Response({
        "status": status.HTTP_400_BAD_REQUEST,
        "errors": "Post topilmadi"
    }, status=status.HTTP_400_BAD_REQUEST)