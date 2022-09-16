from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

from profiles_api import serializers
from profiles_api import models
from profiles_api import permissions

# Create your views here.
class HelloApiView (APIView):
    """Test API View"""

    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """Returns a list of APIView features"""

        an_apiview = [
        'Uses HTTP method as functions (get, post, put, delete)',
        'Is similar to a traditional Django view',
        'Gives you the most control over your application logic',
        'Is mapped manually to URLs'
        ]

        return Response({'message':'Hello!', 'an_apiview': an_apiview})

    def post(self, request):
        """Create a hello message with our name"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'

            return Response ({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Handle updating an object"""

        return Response({'method':'PUT'})

    def patch(self, request, pk=None):
        """Handle partial update of object"""

        return Response({'method': 'PATCH'})

    def delete(self, request, pk=None):
        """Delete an object"""
        return Response ({'method':'DELETE'})

class HelloViewSet(viewsets.ViewSet):
     """Test View Sets"""

     serializer_class = serializers.HelloSerializer
     def list (self, request):
         """Return a hello message"""
         a_viwset=[
         'Uses actions (list, create, retreives, updates, partial updates)',
         'Automatically maps to URLs using Routers',
         'Provides ore functionality with less code'
         ]
         return Response ({'message': 'Hello!', 'a_viwset': a_viwset})

     def create (self, request):
        """Create a new Hello Message"""

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}!'
            return Response ({'message': message})
        else:
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

     def retrieve (self, request, pk=None):
        """Handle getting an object by its ID"""
        return Response({'hht_method': 'GET'})

     def update (self, request, pk=None):
        """Handle updating an object by its ID"""
        return Response({'hht_method': 'PUT'})

     def partial_update (self, request, pk=None):
        """Handle updating parts of an object by its ID"""
        return Response({'hht_method': 'PATCH'})

     def destroy (self, request, pk=None):
        """Handle removing an object by its ID"""
        return Response({'hht_method': 'DELETE'})

class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email')

class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""

    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating reading and updating profile feed items"""

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated)

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)
