from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from levelupapi.models import Game, Gamer
from levelupapi.models.game_type import GameType
from levelupapi.views.game_type import GameTypeSerializer

class GameViewTests(APITestCase):

    # Add any fixtures you want to run to build the test database
    fixtures = ['users', 'tokens', 'gamers', 'game_types', 'games', 'events']
    
    def setUp(self):
        # Grab the first Gamer object from the database and add their token to the headers
        self.gamer = Gamer.objects.first()
        token = Token.objects.get(user=self.gamer.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_get_game(self):
        """Get Game Type Test
        """
        # Grab a game object from the database
        gametype = GameType.objects.first()

        url = f'/gametypes/{gametype.id}'

        response = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # Like before, run the game through the serializer that's being used in view
        expected = GameTypeSerializer(gametype)

        # Assert that the response matches the expected return data
        self.assertEqual(expected.data, response.data)
        
    def test_list_games(self):
        """Test list game types"""
        url = '/gametypes'

        response = self.client.get(url)
        
        # Get all the games in the database and serialize them to get the expected output
        all_game_types = GameType.objects.all()
        expected = GameTypeSerializer(all_game_types, many=True)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        self.assertEqual(expected.data, response.data)