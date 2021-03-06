
   
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404

from ..models.user import User
from ..models.profile import Profile as ProfileModel
from ..serializers import ProfileSerializer

# Create your views here.
class Profile(generics.ListCreateAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class = ProfileSerializer
    def get(self, request):
        """Index request of all Profiles"""
        # Get all the profiles:
        # 1. query for all the profiles --> here we use .all()
        profiles = ProfileModel.objects.all()
        # Filter the profiles by owner, so you can only see your owned profiles
        # profiles = ProfileModel.objects.filter(user_id=request.user.id)
        # Run the data through the serializer
        # 2. Serializer --> formats the data we just found
        data = ProfileSerializer(profiles, many=True).data
        return Response({ 'profiles': data })

    def post(self, request):
        """Create request"""
        # Add user to request data object
        request.data['profile']['user_id'] = request.user.id
        # Serialize/create profile
        profile = ProfileSerializer(data=request.data['profile'])
        # If the profile data is valid according to our serializer...
        if profile.is_valid():
            # Save the created profile & send a response
            profile.save()
            return Response({ 'profile': profile.data }, status=status.HTTP_201_CREATED)
        # If the data is not valid, return a response with the errors
        return Response(profile.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Show request"""
        # Locate the profile to show
        profile = get_object_or_404(ProfileModel, pk=pk)
        # Only want to show owned profiles?
        # I want the profiles to be viewable to all so the invite can be made
        # if request.user != profile.user:
        #     raise PermissionDenied('Unauthorized, you do not own this profile!')
        # Run the data through the serializer so it's formatted
        data = ProfileSerializer(profile).data
        return Response({ 'profile': data })

    def delete(self, request, pk):
        """Delete request"""
        # Locate profile to delete
        profile = get_object_or_404(ProfileModel, pk=pk)
        # Check the profile's owner against the user making this request
        if request.user != profile.user_id:
            raise PermissionDenied('Unauthorized, you do not own this profile!')
        # Only delete if the user owns the profile
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        """Update Request"""
        # Locate Profile
        # get_object_or_404 returns a object representation of our Profile
        profile = get_object_or_404(ProfileModel, pk=pk)
        # Check the profile's owner against the user making this request
        if request.user != profile.user_id:
            raise PermissionDenied('Unauthorized, you do not own this profile!')

        # Ensure the owner field is set to the current user's ID
        request.data['profile']['user_id'] = request.user.id
        # Validate updates with serializer
        data = ProfileSerializer(profile, data=request.data['profile'], partial=True)
        if data.is_valid():
            # Save & send a 204 no content
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # If the data is not valid, return a response with the errors
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

class MyProfile(generics.ListCreateAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class = ProfileSerializer
    def get(self, request):
        """Index request of all Profiles owned by the user"""
        # Get all the profiles:
        # 1. query for all the profiles --> here we use .all()
        # profiles = ProfileModel.objects.all()
        # Filter the profiles by owner, so you can only see your owned profiles
        profiles = ProfileModel.objects.filter(user_id=request.user.id)
        # Run the data through the serializer
        # 2. Serializer --> formats the data we just found
        data = ProfileSerializer(profiles, many=True).data
        return Response({ 'profiles': data })