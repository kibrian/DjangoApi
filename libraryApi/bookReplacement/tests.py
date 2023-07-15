from django.test import TestCase

# Create your tests here.
class CreateBookTestCase(TestCase):
    def test_create_book(self):
        data = {
            'id': 1,
            'title': 'Book Title'
        }
        response = self.client.post('/api/books/', data)
        
        self.assertEqual(response.status_code, 200)
        # Add more assertions to test the response content or other conditions

