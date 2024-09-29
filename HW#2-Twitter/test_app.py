import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from app import app

class MastodonAPITestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.mastodon')
    def test_create_post(self, mock_mastodon):

        mock_post = {'id': 123, 'content': 'Test post'}
        mock_mastodon.status_post.return_value = mock_post
        response = self.app.post('/create', data='Test post content')

        # Assertions
        self.assertEqual(response.status_code, 201) 
        self.assertEqual(response.get_json()['id'], 123)

    @patch('app.mastodon')
    def test_retrieve_post(self, mock_mastodon):

        mock_post = {'id': 123, 'content': 'Test reterive'}
        mock_mastodon.status.return_value = mock_post
        response = self.app.get('/retrieve/123')

        # Assertions
        self.assertEqual(response.status_code, 200) 
        self.assertIn('content', response.get_json())
        self.assertEqual(response.get_json()['content'], 'Test reterive')

    @patch('app.mastodon') 
    def test_delete_post(self, mock_mastodon):

        mock_post = {'id': '123', 'content': 'Test delete'}
        mock_mastodon.status_delete.return_value = mock_post
        response = self.app.delete('/delete/123')

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.get_json())
        self.assertIn('id', response.get_json())
        self.assertEqual(response.get_json()['id'], mock_post['id'])
        self.assertEqual(response.get_json()['message'], 'Post deleted successfully.')

    @patch('app.mastodon')
    def test_create_post_no_content(self, mock_mastodon):
        '''Test create post with no content'''
        
        mock_post = {'id': '123', 'content': None}
        mock_mastodon.status_post.return_value = mock_post
        response = self.app.post('/create', data='')

        # Assertions
        self.assertEqual(response.status_code, 400)  # HTTP 400 Bad Request
        self.assertIn('error', response.get_json())  # Response JSON contains 'error'
        self.assertEqual(response.get_json()['error'], 'Post content is required')

    @patch('app.mastodon')
    def test_retrieve_post_not_found(self, mock_mastodon):
        '''Test retrieve post with non-existent ID'''
        
        mock_post = {'id': 'none'}
        mock_mastodon.status.delete.return_value = mock_post
        response = self.app.get('/retrieve/123456789')

        # Assertions
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.get_json())

if __name__ == '__main__':
    unittest.main()
