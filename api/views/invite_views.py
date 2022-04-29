from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404


from ..models.invite import Invite as InviteModel
from ..serializers import InviteSerializer

# Create your views here.
class Invite(generics.ListCreateAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class = InviteSerializer
    def get(self, request):
        """Index request"""
        # Get all the invites:
        # 1. query for all the invites --> here we use .all()
        # Filter the invites by owner, so you can only see your owned invites
        # the host is the owner of the invite
        invites = InviteModel.objects.all()
        # invites = InviteModel.objects.filter(host_id=request.user.id, friend_id=request.user.id)
        # Run the data through the serializer
        # 2. Serializer --> formats the data we just found
        data = InviteSerializer(invites, many=True).data
        return Response({ 'invites': data })

    def post(self, request):
        """Create request"""
        # Add user to request data object
        request.data['invite']['host_id'] = request.user.id
        # Serialize/create invite
        invite = InviteSerializer(data=request.data['invite'])
        # If the invite data is valid according to our serializer...
        if invite.is_valid():
            # Save the created invite & send a response
            invite.save()
            return Response({ 'invite': invite.data }, status=status.HTTP_201_CREATED)
        # If the data is not valid, return a response with the errors
        return Response(invite.errors, status=status.HTTP_400_BAD_REQUEST)

class InviteDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Show request"""
        # Locate the invite to show
        invite = get_object_or_404(InviteModel, pk=pk)
        # Only want to show owned and received invites?
        if request.user != invite.host_id and request.user != invite.friend_id:
            raise PermissionDenied('Unauthorized, you do not own this invite')

        # Run the data through the serializer so it's formatted
        data = InviteSerializer(invite).data
        return Response({ 'invite': data })

    def delete(self, request, pk):
        """Delete request"""
        # Locate invite to delete
        invite = get_object_or_404(InviteModel, pk=pk)
        # Check the invite's owner against the user making this request
        if request.user != invite.host_id:
            raise PermissionDenied('Unauthorized, you do not own this invite')
        # Only delete if the user owns the invite
        invite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        """Update Request"""
        # Locate Invite
        # get_object_or_404 returns a object representation of our Invite
        invite = get_object_or_404(InviteModel, pk=pk)
        # Check the invite's owner against the user making this request
        if request.user != invite.host_id:
            raise PermissionDenied('Unauthorized, you do not own this invite')

        # Ensure the owner field is set to the current user's ID
        request.data['invite']['host_id'] = request.user.id
        # Validate updates with serializer
        data = InviteSerializer(invite, data=request.data['invite'], partial=True)
        if data.is_valid():
            # Save & send a 204 no content
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # If the data is not valid, return a response with the errors
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
