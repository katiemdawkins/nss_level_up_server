"""View module for handling requests about game types"""
from multiprocessing import Event
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import game
from levelupapi.models.game import Game
from levelupapi.models.game_type import GameType
from levelupapi.models.gamer import Gamer
from django.core.exceptions import ValidationError


class GameView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game)
            return Response(serializer.data)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        games = Game.objects.all()
        
        #'type' argument, if you do a fetch call, it needs to match the query parameter
        #kind of like useParams in front end
        #type is what the url is sending in 
        #we make the rules. we chose the work type 
        game_type = request.query_params.get('type', None)
        if game_type is not None:
            games = games.filter(game_type_id=game_type)
    
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        #make and instance of it
        serializer = CreateGameSerializer(data=request.data)
        #raise exception=True - this field is required
        #more verbose
        serializer.is_valid(raise_exception=True)
        #gamer=gamer is checking that it's getting an integer id
        serializer.save(gamer=gamer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """

        game = Game.objects.get(pk=pk)
        serializer = CreateGameSerializer(game, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        #return None ? you have to return something
        #saying none bc nothing is coming back
        #but we get the status code to know it works
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        
        # game.title = request.data["title"]
        # game.maker = request.data["maker"]
        # game.number_of_players = request.data["number_of_players"]
        # game.skill_level = request.data["skill_level"]

        # game_type = GameType.objects.get(pk=request.data["game_type"])
        # game.game_type = game_type
        # game.save()

        # return Response(None, status=status.HTTP_204_NO_CONTENT)
    def destroy(self, request, pk):
        game = Game.objects.get(pk=pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    

class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Game
        fields = ('id', "gamer", "title", "maker", "number_of_players", "skill_level", 'game_type')
        depth = 1
        
#for the create method fields include
#anything the client will send up
class CreateGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'title', 'maker', 'number_of_players', 'skill_level', 'game_type')