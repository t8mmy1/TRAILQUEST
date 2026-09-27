from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from trailQuest.models import Trail, Review

# Create your tests here.
class TrailSubmissionFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_valid_trail_submission(self):
        valid_data = {
            'trailName': 'Sunset Trail',
            'location': 'Hillside',
            'distance': '5.5',
            'elevationGain': '200',
            'difficultyLevel': 'Intermediate',
            'trailType': 'Loop',
            'estimatedTime': '2.5'
        }
        response = self.client.post(reverse('submit-trail'), valid_data)
        self.assertEqual(response.status_code, 302)  # Redirect on success
        self.assertTrue(Trail.objects.filter(name='Sunset Trail').exists())

    def test_invalid_missing_required_fields(self):
        invalid_data = {
            'trailName': '',
            'location': '',
            'distance': '',
            'elevationGain': '',
            'difficultyLevel': '',
            'trailType': '',
            'estimatedTime': ''
        }
        response = self.client.post(reverse('submit-trail'), invalid_data)
        self.assertEqual(response.status_code, 200) # should render page again
        self.assertContains(response, "Trail name is required.")
        self.assertFalse(Trail.objects.filter(name='').exists())


    def test_invalid_negative_distance_and_elevation(self):
        invalid_data = {
            'trailName': 'Bad Trail',
            'location': 'Nowhere',
            'distance': '-10',
            'elevationGain': '-50',
            'difficultyLevel': 'Beginner',
            'trailType': 'Loop',
            'estimatedTime': '1.5'
        }
        response = self.client.post(reverse('submit-trail'), invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Distance must be greater than 0 kilometers.")
        self.assertContains(response, "Elevation gain cannot be negative.")
        self.assertFalse(Trail.objects.filter(name='Bad Trail').exists())

class LoginFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_valid_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)  

    def test_invalid_username(self):
        response = self.client.post(reverse('login'), {
            'username': 'wronguser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200) 
        self.assertContains(response, "The username does not exist.")

    def test_invalid_password(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200) 
        self.assertContains(response, "The password is incorrect.")

class AdminTrailApprovalFormTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username='adminuser', password='adminpass', is_staff=True, is_superuser=True)
        self.trail = Trail.objects.create(
            name="Pending Trail",
            location="Test Park",
            distance=5.0,
            elevation_gain=100,
            difficulty_level="Beginner",
            trail_type="Loop",
            estimated_time=2.0,
            status='pending'
        )
        self.client.login(username='adminuser', password='adminpass')

    def test_valid_approval(self):
        response = self.client.post(reverse('approve-trail-detail', kwargs={'trail_id': self.trail.id}), {
            'trail_name': 'Approved Trail',
            'location': 'Updated Park',
            'latitude': '',
            'longitude': '',
            'start_point': '',
            'end_point': '',
            'distance': '5.0',
            'elevation_gain': '100.0',
            'difficulty_level': 'Beginner',
            'trail_type': 'Loop',
            'estimated_time': '2.0',
            'trail_conditions': '',
            'accessibility': '',
            'user_notes': '',
            'approval_status': 'approved',
            'admin_comments': 'Looks good.'
        })
        self.assertEqual(response.status_code, 302)
        updated_trail = Trail.objects.get(id=self.trail.id)
        self.assertEqual(updated_trail.status, 'approved')
        self.assertEqual(updated_trail.admin_comments, 'Looks good.')
        self.assertEqual(updated_trail.approved_by, self.admin)

    def test_missing_approval_status(self):
        response = self.client.post(reverse('approve-trail-detail', kwargs={'trail_id': self.trail.id}), {
            'approval_status': '',
            'admin_comments': 'Missing status'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please select an approval status.")

    def test_invalid_admin_comment(self):
        response = self.client.post(reverse('approve-trail-detail', kwargs={'trail_id': self.trail.id}), {
            'approval_status': 'rejected',
            'admin_comments': 'Invalid comment @$%^&*'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Comments can only include letters, numbers, spaces, periods, commas, and hyphens.")

class RegistrationFormTests(TestCase):
    def test_valid_form_submission(self):
        form_data = {
            'email' : 'testemail@gmail.com',
            'password' : '&1Ad1Ad%',
            'confirmPassword' : '&1Ad1Ad%'
        }
        response = self.client.post(reverse('register'), data = form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testemail@gmail.com').exists()) # Email becomes username in models

    def test_invalid_email(self):
        form_data = {
            'email' : 'invalidemail',
            'password' : '&1Ad1Ad%',
            'confirmPassword' : '&1Ad1Ad%'
        }
        response = self.client.post(reverse('register'), data = form_data)
        self.assertNotEqual(response.status_code, 302)
        self.assertContains(response, "Please enter a valid email address.")

    def test_invalid_weak_password(self):
        form_data = {
            'email': 'weakpass@example.com',
            'password': 'weak',  
            'confirmPassword': 'weak'
        }
        response = self.client.post(reverse('register'), data=form_data)
        self.assertNotEqual(response.status_code, 302)
        self.assertContains(response, "Minimum 8 characters.")
        self.assertContains(response, "At least one uppercase letter.")
        self.assertContains(response, "At least one number.")
        self.assertContains(response, "At least one special character")

class TrailReviewFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testemail@gmail.com', password='&1Ad1Ad%')
        self.trail = Trail.objects.create(
            name='Sunset Trail',
            location='Hillside',
            distance=5.5,
            elevation_gain=200,
            difficulty_level='Intermediate',
            trail_type='Loop',
            estimated_time=2.5,
            status='approved'
            )
        self.client.login(username='testemail@gmail.com', password='&1Ad1Ad%')

    def test_valid_rating(self):
            response = self.client.post(reverse('review-trail', kwargs={'trail_id': self.trail.id}), {
                'rating': '5'
            })
            self.assertEqual(response.status_code, 302)
            self.assertTrue(Review.objects.filter(user=self.user, trail=self.trail).exists())

    def test_invalid_rating_zero(self):
        response = self.client.post(reverse('review-trail', kwargs={'trail_id': self.trail.id}), {
            'rating': '0'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Review.objects.filter(user=self.user, trail=self.trail).exists())
        self.assertContains(response, "Rating must be between 1 and 5.")

    def test_invalid_rating_above_five(self):
        response = self.client.post(reverse('review-trail', kwargs={'trail_id': self.trail.id}), {
            'rating': '6'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Review.objects.filter(user=self.user, trail=self.trail).exists())
        self.assertContains(response, "Rating must be between 1 and 5.")

class TrailSearchFilteringFormTests(TestCase):
    def setUp(self):
        Trail.objects.create(
            name="Forest Path",
            location="Mountain View",
            difficulty_level="Beginner",
            distance=2.5,
            elevation_gain=100,
            trail_type="Loop",
            estimated_time=1.5,
            status="approved"
        )
        Trail.objects.create(
            name="Rocky Road",
            location="Desert Edge",
            difficulty_level="Advanced",
            distance=8.0,
            elevation_gain=300,
            trail_type="Point-to-Point",
            estimated_time=4.0,
            status="approved"
        )

    def test_filter_by_location_and_difficulty(self):
        response = self.client.get(reverse('search-trail-form'), {
            'location': 'Mountain',
            'difficultyLevel': 'Beginner'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Forest Path")
        self.assertNotContains(response, "Rocky Road")

    def test_filter_by_distance_range(self):
        response = self.client.get(reverse('search-trail-form'), {
            'minDist': '1.0',
            'maxDist': '3.0'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Forest Path")
        self.assertNotContains(response, "Rocky Road")

    def test_invalid_distance_inputs(self):
        response = self.client.get(reverse('search-trail-form'), {
            'minDist': '-5',
            'maxDist': 'abc'
        })
        self.assertEqual(response.status_code, 200)  