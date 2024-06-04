from django.shortcuts import render

# Create your views here.
from team.serializers import TeamSerializer, TeamGETSerializer, TeamPatchSerializeer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from team.models import Team
from user.models import User
from user.serializers import UserSerializer



class TeamBase(APIView):
    """
    Base interface implementation for API's to manage teams.
    For simplicity a single team manages a single project. And there is a separate team per project.
    """
    def post(self,request):
        if 'id' and 'users' in request.data:
            return self.add_users_to_team(request)
        else:
            return self.create_team(request)
    
    def get(self, request, team_id=None):
        if 'id' in request.data:
            return self.describe_team(request)
        elif team_id is not None:
            return self. list_team_users(request, team_id)
        else:
            return self.list_teams(request)
        
    def delete(self,request):
        return self.remove_users_from_team(request)

    
    
    # create a team
    def create_team(self, request: str) -> str:
       
        data = request.data
        serializer = TeamSerializer(data)
        if serializer.is_valid():
            serializer.save()
            return Response({'id': serializer.data.get('id')}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    
    # list all teams
    def list_teams(self, request=None) -> str:
        
        data = Team.objects.all()
        serializer = TeamGETSerializer(data, many=True)
        return Response(serializer.data)

    
    
    # describe team
    def describe_team(self, request: str) -> str:
       
        data1 = request.data.get('id')
        try:
            data = Team.objects.get(id = data1)
        except Team.DoesNotExist:
            return Response({"MSG": "Team ID does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TeamGETSerializer(data)
        return Response(serializer.data)

    
    
    # update team
    def update_team(self, request: str) -> str:
       
        data1 = request.data.get('id')
        data = Team.objects.get(id = data1)
        serializer = TeamPatchSerializeer(data, data= request.data, partial=True)

        if serializer.is_valid():
            return Response({"MSG": "Updated"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, )

    
    
    # add users to team
    def add_users_to_team(self, request: str):
       
        team_id = request.data.get('id')
        try:
            team = Team.objects.get(id = team_id)
        except Team.DoesNotExist:
            return Response({"MSG": "Team with this ID does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        userid_add = request.data.get('users', [])   #.get('users') used same as present in models.py manytomanyfield
        user_add = User.objects.filter(id__in = userid_add)
        team.users.add(*user_add)

        serializer = TeamSerializer(team)
        return Response(serializer.data, status=status.HTTP_200_OK)


    
    
    # add users to team
    def remove_users_from_team(self, request: str):
        
        teamid = request.data.get('id')
        try:
            team = Team.objects.get(id = teamid)
        except Team.DoesNotExist:
            return Response({"MSG": "Team with this ID does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        userid = request.data.get('users', [])
        user_remove = User.objects.filter(id__in= userid)
        team.users.remove(*user_remove)

        return Response({"MSG": "User removed"}, status=status.HTTP_200_OK)

    
    
    # list users of a team
    def list_team_users(self, request, team_id):
       
        # teamid = request.data.get('id')        Have used url endpoint to get the list of users, since we are already using teamid to get the details of the specific teams
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response({"MSG": "Team with this ID does not exist"})

        users = team.users.all()

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

