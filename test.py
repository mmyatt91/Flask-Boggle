from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
    
    def test_homepage(self):
        with self.client:
            res = self.client.get('/')
            self.assertIn('board', session)
            self.assertIn(b'<p>High Score:', res.data)
            self.assertIn(b'Score:', res.data)
            self.assertIn(b'Seconds Left:', res.data)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))

    def test_validity(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["H", "E", "L", "L", "O"],
                                 ["H", "E", "L", "L", "O"],
                                 ["H", "E", "L", "L", "O"],
                                 ["H", "E", "L", "L", "O"],
                                 ["H", "E", "L", "L", "O"]]
        res = self.client.get('/check-word?word=hello')
        self.assertEqual(res.json['result'], 'ok')
    
    def test_invalidity(self):
        self.client.get ('/')
        res = self.client.get('/check-word?word=bailar')
        self.assertEqual(res.json['result'], 'not-word')


