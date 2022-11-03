from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Song, Artiste, Lyric
from .serializers import SongSerializer, ArtisteSerializer, LyricSerializer

#   Artiste List
@api_view(['GET', 'POST'])
def artiste(request, format=None):
    """
    List all artist
    """
    if request.method == 'GET':
        artistes = Artiste.objects.all()
        serializer = ArtisteSerializer(artistes, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ArtisteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Song List using class views
class SongView(APIView):
    def get(self, request, format=None):
        songs = Song.objects.all()
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SongSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#Aritste patch, delete, get_detail
@api_view(['GET', 'PATCH', 'DELETE'])
def artiste_detail(request, pk, format=None):
    """
    Retrieve, update or delete an artiste
    """
    try:
        artistes = Artiste.objects.get(pk=pk)
    except Artiste.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ArtisteSerializer(artistes)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        serializer = ArtisteSerializer(artistes, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        artistes.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#Song patch, delete, get
class SongDetail(APIView):

    def get_object(self, pk):

        try:
            return Song.objects.get(pk=pk)
        except Song.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        song = self.get_object(pk)
        serializers = SongSerializer(song)
        return Response(serializers.data)

    def patch(self, request, pk):
        song = self.get_object(pk)
        data = request.data
        song.title = data.get("title", song.title)
        song.date_released = data.get("date_released", song.date_released)

        serializer = SongSerializer(song, data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        song = self.get_object(pk)
        song.delete()
        return Response({"message":"sucessfully deleted"}, status=status.HTTP_200_OK)
        

#Lyrics list
class LyricView(APIView):
    def get(self, request, format=None):
        lyrics = Lyric.objects.all()
        serializer = LyricSerializer(lyrics, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = LyricSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    