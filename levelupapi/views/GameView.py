"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import game
from levelupapi.models.game import Game


class GameView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        game = Game.objects.get(pk=pk)
        serializer = GameSerializer(game)
        return Response(serializer.data)
        

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        games = Game.objects.all()
        
        game_type = request.query_params.get('type', None)
        if game_type is not None:
            games = games.filter(game_type_id=game_type)
    
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)

class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Game
        fields = ('id', 'game_type', "title", "maker", "gamer", "number_of_players", "skill_level")