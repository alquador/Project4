from django.urls import path
from .views.invite_views import Invite, InviteDetail
from .views.profile_views import Profile, ProfileDetail
from .views.user_views import SignUp, SignIn, SignOut, ChangePassword

urlpatterns = [
  	# Restful routing
    path('invites/', Invite.as_view(), name='invites'),
    path('invites/<int:pk>/', InviteDetail.as_view(), name='invite_detail'),
    path('profiles/', Profile.as_view(), name='profiles'),
    path('profiles/<int:pk>/', ProfileDetail.as_view(), name='profile_detail'),
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('change-pw/', ChangePassword.as_view(), name='change-pw')
]
