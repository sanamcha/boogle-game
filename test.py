from unittest import TestCase
from flask import session
from app import app
from boggle import Boggle



class FlaskTests(TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_index(self):
        with self.client:
            response = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get("bestscore"))
            self.assertIsNone(session.get("tplays"))
            self.assertIn("<p>High Score:", response.data)
            self.assertIn("Score", response.data)
            self.assertIn("Remaining Time:", response.data)

    def test_valid_word(self):
        with self.client as client:
            with client.session_transaction() as sess_trans:
                sess_trans['board'] = [["H", "A", "T", "T"], ["H", "A", "T", "T"], ["H", "A", "T", "T"], ["H", "A", "T", "T"],["H", "A", "T", "T"]
                ]

        response = self.client.get('/check?word=hat')
        self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        self.client.get('/')
        response = self.client.get('/check?word=sanamm')
        self.assertEqual(response.json['result'], 'not-on-board')

    def non_english_word(self):
        self.client.get('/')
        response = self.client.get('/check?word=abcdefghihkj')
        self.assertEqual(response.json['result'], 'not-word')



