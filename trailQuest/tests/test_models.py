from django.test import TestCase
from trailQuest.models import Trail, Review
from django.contrib.auth.models import User

# Create your tests here.
class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='unique@gmail.com', username='unique', password='&1Ad1Ad%')
        self.trail = Trail.objects.create(name='Paramatta River', location='Sydney', distance=5.0, elevation_gain=100, difficulty_level='Beginner', trail_type='Loop', estimated_time=2.0)
        self.review = Review.objects.create(user=self.user, trail=self.trail, rating=5, comment="Testing!")

    # FIELDS TEST
    def test_user_username(self):
        self.assertEqual(self.user.username, 'unique')

    # RELATIONAL TEST 
    def test_user_review_relationship(self):
        self.assertEqual(self.user.reviews.first(), self.review)
    
    def test_user_trail_relationship(self):
        self.assertEqual(self.user.reviews.first().trail, self.trail)
    
class TrailModelTest(TestCase):
    def setUp(self):
        self.trail = Trail.objects.create(name='Paramatta River', location='Sydney', distance=5.0, elevation_gain=100, difficulty_level='Beginner', trail_type='Loop', estimated_time=2.0)
        self.user = User.objects.create_user(email='unique@gmail.com', username='unique', password='&1Ad1Ad%')
        self.review = Review.objects.create(user=self.user, trail=self.trail, rating=5, comment="Testing!")

    # FIELDS TEST 
    def test_trail_name(self):
        self.assertEqual(self.trail.name, 'Paramatta River')

    # RELATIONAL TEST
    def test_trail_reviews_relationship(self):
        self.assertEqual(self.trail.reviews.first(), self.review)
    
    def test_trail_user_relationship(self):
        self.assertEqual(self.trail.reviews.first().user, self.user)

class ReviewModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='unique@gmail.com', username='unique', password='&1Ad1Ad%')
        self.trail = Trail.objects.create(name='Paramatta River', location='Sydney', distance=5.0, elevation_gain=100, difficulty_level='Beginner', trail_type='Loop', estimated_time=2.0)
        self.review = Review.objects.create(user=self.user, trail=self.trail, rating=5, comment="Testing!")

    # FIELDS TEST    
    def test_review_rating(self):
        self.assertEqual(self.review.rating, 5)
    
    # RELATIONAL TEST
    def test_review_user_relationship(self):
        self.assertEqual(self.review.user, self.user)

    def test_review_trail_relationship(self):
        self.assertEqual(self.review.trail, self.trail)
        