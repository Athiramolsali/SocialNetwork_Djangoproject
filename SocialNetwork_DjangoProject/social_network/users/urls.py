from django.urls import path
from .views import AllFriendsListAPIView,SignupAPIView, LoginAPIView,UserSearchAPIView,SendFriendRequestAPIView,FriendRequestActionAPIView,ListFriendsAPIView,PendingFriendRequestsAPIView

urlpatterns = [
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('search/', UserSearchAPIView.as_view(), name='user-search'),
    path('friend-request/send/', SendFriendRequestAPIView.as_view(), name='send-friend-request'),
    path('friend-request/respond/', FriendRequestActionAPIView.as_view(), name='respond-friend-request'),
    path('friend-request-accepted/', ListFriendsAPIView.as_view(), name='-friend-request-accepted'),
    path('friend-requests/pending/', PendingFriendRequestsAPIView.as_view(), name='pending-friend-requests'),
    path('friend-requests/all/', AllFriendsListAPIView.as_view(), name='friend-requests-all'),
    


]
