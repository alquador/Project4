from django.urls import path
from .views.invite_views import Invite, InviteDetail, InviteAccept, InviteAcceptDetail
from .views.profile_views import Profile, ProfileDetail, MyProfile
from .views.user_views import SignUp, SignIn, SignOut, ChangePassword

urlpatterns = [
  	# Restful routing
    path('invites/', Invite.as_view(), name='invites'),
    path('invites/<int:pk>/', InviteDetail.as_view(), name='invites_detail'),
    path('invites/create/', Invite.as_view(), name='invites_create'),
    path('invites/<int:pk>/update/', InviteDetail.as_view(), name='invites_update'),
    path('invites/accepted/', InviteAccept.as_view(), name='invites_accept'),
    path('invites/accepted/<int:pk>/', InviteAcceptDetail.as_view(), name='invites_accept_detail'),
    path('invites/<int:pk>/delete/', InviteDetail.as_view(), name='invites_delete'),
    path('profiles/', Profile.as_view(), name='profiles'),
    path('profiles/mine/', MyProfile.as_view(), name='profiles_mine'), 
    path('profiles/<int:pk>/', ProfileDetail.as_view(), name='profile_detail'),
    path('profiles/create/', Profile.as_view(), name='profiles_create'),
    path('profiles/<int:pk>/update/', ProfileDetail.as_view(), name='profiles_update'),
    path('profiles/<int:pk>/delete/', ProfileDetail.as_view(), name='profiles_delete'),
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('change-pw/', ChangePassword.as_view(), name='change-pw')
]
