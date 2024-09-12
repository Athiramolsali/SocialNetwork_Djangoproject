from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer,ListUserSerializer,FriendRequestSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from .models import FriendRequest
from django.utils import timezone
from datetime import timedelta



class SignupAPIView(APIView):
    permission_classes = [AllowAny]  # Allow anyone to access this view

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User created successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class LoginAPIView(APIView):
    permission_classes = [AllowAny] 

    def post(self, request):
        email = request.data.get('email').lower()
        password = request.data.get('password')
        user = authenticate(username=email, password=password)
        
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
    


 #API to search  users
class UserSearchAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        search_key = request.query_params.get('search_key', '')
        paginator = PageNumberPagination()
        paginator.page_size = 10

        if '@' in search_key:
            users = User.objects.filter(email__iexact=search_key)
        else:
            users = User.objects.filter(Q(first_name__icontains=search_key) | Q(last_name__icontains=search_key))

        result_page = paginator.paginate_queryset(users, request)
        serializer = ListUserSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    

#Send Friend Request
class SendFriendRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        to_user_id = request.data.get('to_user_id')
        to_user = User.objects.get(id=to_user_id)
        
        # Rate limiting: max 3 requests per minute
        one_minute_ago = timezone.now() - timedelta(minutes=1)
        recent_requests = FriendRequest.objects.filter(from_user=request.user, time__gte=one_minute_ago)
        
        if recent_requests.count() >= 3:
            return Response({'error': 'You can only send 3 friend requests per minute.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

       #Check if already sent
        if FriendRequest.objects.filter(from_user=request.user, to_user=to_user).exists():
            return Response({'error': 'Friend request already sent.'}, status=status.HTTP_400_BAD_REQUEST)
        #Sent new friend request
        friend_request = FriendRequest.objects.create(from_user=request.user, to_user=to_user)
        return Response({'message': 'Friend request sent.'}, status=status.HTTP_201_CREATED)
    

#API to update the status of a previously sent friend request(Accept or Reject)
class FriendRequestActionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request_id = request.data.get('request_id')
        action = request.data.get('action')  # 'accept' or 'reject'
        try:
            friend_request = FriendRequest.objects.filter(id=request_id,to_user=request.user.id).first()
            if not friend_request:
                return Response({'error': 'Friend request not found.'}, status=status.HTTP_404_NOT_FOUND)

            if action == 'accept':
                friend_request = FriendRequest.objects.filter(id=request_id, to_user=request.user.id).update(is_accepted=True)
               
                return Response({'message': 'Friend request accepted.'}, status=status.HTTP_200_OK)
            elif action == 'reject':
                FriendRequest.objects.filter(id=request_id, to_user=request.user.id).delete()
                return Response({'message': 'Friend request rejected.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid action.'}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FriendsListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        friends = User.objects.filter(
            Q(sent_requests__to_user=request.user, sent_requests__is_accepted=True) |
            Q(received_requests__from_user=request.user, received_requests__is_accepted=True)
        ).distinct()
        
        serializer = UserSerializer(friends, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


# List pending friend requests
class PendingFriendRequestsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pending_requests = FriendRequest.objects.filter(to_user=request.user.id, is_accepted=False)
        serializer = FriendRequestSerializer(pending_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    



#All list of requests
class AllFriendsListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        friends = FriendRequest.objects.all()
        serializer = FriendRequestSerializer(friends, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

# API to list friends(list of users who have accepted friend request)
class ListFriendsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        friend_requests = FriendRequest.objects.filter(
            Q(from_user=request.user) | Q(to_user=request.user),
            is_accepted=True
        )
        serializer = FriendRequestSerializer(friend_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    



