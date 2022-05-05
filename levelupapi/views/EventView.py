"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, event
from levelupapi.models.gamer import Gamer
from levelupapi.models.game import Game
from django.core.exceptions import ValidationError
from rest_framework.decorators import action

class EventView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        try:
            #pk = pk left side is the key you want to match from song
            #right side is the side you pass through and ask for
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event)
            return Response(serializer.data)
        except Event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        events = Event.objects.all()
        
        game = request.query_params.get('game', None)
        if game is not None:
            events = events.filter(game_id = game)
        #many =True means we want many fields back, default is false
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        organizer = Gamer.objects.get(user=request.auth.user)
        game = Game.objects.get(pk=request.data["game"])
        serializer = CreateEventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(organizer=organizer, game=game)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # event = Event.objects.create(
        #    game = game,
        #    description=request.data['description'],
        #    date=request.data['date'],
        #    time=request.data['time'],
        #    organizer = organizer
        # )
        # serializer= EventSerializer(event)
        # return Response(serializer.data)
        
    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        event = Event.objects.get(pk=pk)
        serializer = CreateEventSerializer(event, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        
        # event.description = request.data["description"]
        # event.date = request.data["date"]
        # event.time = request.data["time"]

        # game = Game.objects.get(pk=request.data["game"])
        # event.game = game
        # organizer = Gamer.objects.get(user=request.auth.user)
        # event.organizer = organizer
        # event.save()

        # return Response(None, status=status.HTTP_204_NO_CONTENT)
    def destroy(self, request, pk):
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['post'], detail=True)
    def signup(self, request, pk):
        """Post request for a user to sign up for an event"""

        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.add(gamer)
        return Response({'message': 'Gamer added'}, status=status.HTTP_201_CREATED)
    
    @action(methods=['delete'], detail=True)
    def leave(self, request, pk):
        """Post request for a user to sign up for an event"""

        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.remove(gamer)
        return Response({'message': 'Gamer removed'}, status=status.HTTP_204_NO_CONTENT)   
    
#Serializer -> taking data from Django and turning it into something we can use       
class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Event
        fields = '__all__'
        depth = 1
   #can do __all__ here on event serializer, cant do it below bc we
   #are trying to verify data
      
class CreateEventSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Event
        fields = ('id', 'game', "description", "date", "time", "organizer")