from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
# from rest_framework.decorators import api_view
from watchlist_app.models import WatchList , StreamPlatform , Review
from watchlist_app.api.serializers import (WatchListSerializer,StreamPlatformSerializer,
                                           ReviewSerializer)
from rest_framework import status 
from rest_framework import generics 
from rest_framework import viewsets
# from rest_framework import  mixins
from rest_framework.views import APIView
from watchlist_app.api.permissions import AdminOrReadOnly, ReviewUserOrReadOnly
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly

class ReviewList(generics.ListAPIView):
    
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)
    
class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    
    
    def get_queryset(self):
        return Review.objects.all()
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)
        
        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist, review_user = review_user)
        if review_queryset.exists():
            raise ValidationError("you have already reviewd this movoie")
        
        
        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data["data"]
        else:
            watchlist.avg_rating = (watchlist.avg_rating +  serializer.validated_data["data"]) / 2
            
        watchlist.number_rating = watchlist.number_rating + 1
        watchlist.save()
            
        serializer.save(watchlist = watchlist,review_user = review_user)
    
    
    
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ ReviewUserOrReadOnly]
    
    
    
class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

#
class StreamPlatformVS(viewsets.ViewSet):
    
    
    def list(self,request):
        queryset  = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(queryset,many = True)
        return Response(serializer.data)
    
    def retrieve(self,request,pk = None):
        queryset = StreamPlatform.objects.all()
        watchlist = get_object_or_404(queryset,pk=pk)
        serializer = StreamPlatformSerializer(watchlist)
        return Response(serializer.data)


    def create (self,request):
        serializer = StreamPlatformSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
        
        
        
class StreamPlatformAV(APIView):
    def get(self,request):
        platform = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platform,many = True)
        return Response(serializer.data)
    
    
    def post(self,request):
        serializer = StreamPlatformSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    
 
class StreamPlatformDetailAV(APIView):
    def get(self,request,pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist: 
            return Response({'Error': 'not foune'}, status.Http_404_Not_Found)
        serializer = StreamPlatformSerializer(platform)
        return Response(serializer.data)  
    
    def put(self,request,pk):
        platform = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) 
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST )
        
    def delete(self,request,pk):
        platform = StreamPlatform.objects.get(pk=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)   
        
class WatchListAV(APIView):
    def get(self,request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many = True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        

class WatchDetailAV(APIView):
    def get(self,request,pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist: 
            return Response({'Error': 'not foune'}, status.Http_404_Not_Found)
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)

    def put(self,request,pk):
        movie = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) 
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST )
        
    def delete(self,request,pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# @api_view(['GET', 'POST'])
# def movie_list(request):
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = Movieserializer(movies, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = Movieserializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)


# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_details(request, pk):
    
#     if request.method == 'GET':
#         try:
#             movie = Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist: 
         
#             return Response({'Error': 'Movie not foune'}, status.Http_404_Not_Found)
#     serializer = Movieserializer(movie)
#     return Response(serializer.data)

#     if request.method == 'PUT':
#         movie = Movie.objects.get(pk=pk)
#         serializer = Movieserializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer .save()
#             return Response(serializer.data) 
#         else:
#             return Response(serializer.errors, status.HTTP_400_BAD_REQUEST )
#     if request.method == 'DELETE':
#         movie = Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response(status= status.HTTP_204_NO_CONTENT)  
# class ReviewList(mixins.ListModelMixin,mixins.CreateModelMixin,
#                  generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSeralizer
    
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
    
# class ReviewDetail(mixins.RetrieveModelMixin,generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSeralizer
    
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)