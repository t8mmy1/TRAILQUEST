from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from trailQuest.models import Trail
from decimal import Decimal
from django.utils import timezone

# Create your tests here.
class HomeViewTests(TestCase):
    def test_home(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "trailQuest/home.html")

    def test_home_logout(self):
        User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Logout")  

class LoginViewTests(TestCase):
    def test_login(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_login_success(self):
        User.objects.create_user(username='testuser', password='testpassword')
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302) 

class RegisterViewTests(TestCase):
    def test_register(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "trailQuest/html-user/register.html")

    def test_register_success(self):
        response = self.client.post(reverse('register'), {
            'email': 'unique@example.com',
            'password': '&1Ad1Ad%',
            'confirmPassword': '&1Ad1Ad%'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='unique@example.com').exists())

class ProfileViewTests(TestCase):
    def test_profile(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "trailQuest/html-user/profile.html")
    
    def test_unauthenticated_profile(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('profile'))

class CommentViewTests(TestCase):
    def test_comment(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('comment'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "trailQuest/html-user/comment.html")

    def test_unauthenticated_comment(self):
        response = self.client.get(reverse('comment'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('comment'))

class ReviewTrailViewTests(TestCase):
    def setUp(self):
        self.trail = Trail.objects.create(
            name="Test Trail",
            location="Blue Mountains",
            latitude=Decimal("-33.712345"),
            longitude=Decimal("150.312345"),
            start_point="Echo Point",
            end_point="Scenic World",
            distance=Decimal("5.50"),
            elevation_gain=Decimal("120.25"),
            difficulty_level="Intermediate",
            trail_type="Loop",
            estimated_time=Decimal("2.00"),
            trail_conditions="Rocky, Steep",
            accessibility="child-friendly, dog-friendly",
            user_notes="Scenic walk with great views.",
            date_submitted=timezone.now(),
            status="pending"
        )

    def test_review_trail(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(reverse('review-trail', kwargs={'trail_id': self.trail.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "trailQuest/html-user/review-trail.html")

    def test_unauthenticated_review_trail(self):
        response = self.client.get(reverse('review-trail', kwargs={'trail_id': self.trail.id}))
        self.assertEqual(response.status_code, 302)
        expected_redirect_url = reverse('login') + '?next=' + reverse('review-trail', kwargs={'trail_id': self.trail.id})
        self.assertRedirects(response, expected_redirect_url)

class SearchTrailViewTests(TestCase):
    def test_search_by_difficulty(self):
        Trail.objects.create(
            name="Easy Walk",
            location="Park",
            difficulty_level="Beginner",
            distance=2.0,
            elevation_gain=50,
            trail_type="Loop",
            estimated_time=1.0,
            status="approved"
        )
        Trail.objects.create(
            name="Tough Hike",
            location="Mountain",
            difficulty_level="Advanced",
            distance=10.0,
            elevation_gain=600,
            trail_type="Point-to-Point",
            estimated_time=5.0,
            status="approved"
        )

        response = self.client.get(reverse('search-trail-form'), {'difficultyLevel': 'Beginner'})
        self.assertContains(response, "Easy Walk")
        self.assertNotContains(response, "Tough Hike")

    def test_search_by_name(self):
        Trail.objects.create(name="Blue Ridge", location="Valley", difficulty_level="Intermediate",
                            distance=4.0, elevation_gain=150, trail_type="Loop", estimated_time=2.0,
                            status="approved")

        response = self.client.get(reverse('search-trail-form'), {'trailName': 'blue'})
        self.assertContains(response, "Blue Ridge")

class SubmitTrailViewTests(TestCase):
    def test_submit_trail(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('submit-trail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "trailQuest/html-trail/submit-trail.html")

    def test_unauthenticated_submit_trail(self):
        response = self.client.get(reverse('submit-trail'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('submit-trail'))

    def test_admin_cannot_submit_trail(self):
        admin = User.objects.create_user(username='admin', password='adminpass', is_staff=True, is_superuser=True)
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('submit-trail'))
        self.assertEqual(response.status_code, 302)  
        self.assertRedirects(response, reverse('home'))

class ViewTrailViewTests(TestCase):
    def test_view_specific_trail(self):
        trail = Trail.objects.create(
            name="Scenic Trail",
            location="Forest",
            latitude=Decimal("34.000000"),
            longitude=Decimal("150.000000"),
            start_point="Start",
            end_point="End",
            distance=Decimal("5.0"),
            elevation_gain=Decimal("100.0"),
            difficulty_level="Intermediate",
            trail_type="Loop",
            estimated_time=Decimal("2.0"),
            trail_conditions="Dry",
            accessibility="child-friendly",
            user_notes="Nice walk.",
            date_submitted=timezone.now(),
            status="approved"
        )
        response = self.client.get(reverse('view-trail', kwargs={'trail_id': trail.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Scenic Trail")
    
    def test_view_nonexistent_trail(self):
        response = self.client.get(reverse('view-trail', kwargs={'trail_id': 9999})) 
        self.assertEqual(response.status_code, 404)


class AdminDashboardViewTests(TestCase):
    def test_admin_dashboard(self):
        user = User.objects.create_user(username='adminuser', password='adminpassword', is_staff=1, is_superuser=1)
        self.client.login(username='adminuser', password='adminpassword')
        response = self.client.get(reverse('admin-dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "trailQuest/html-admin/admin-dashboard.html")

    def test_unauthenticated_admin_dashboard(self):
        response = self.client.get(reverse('admin-dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('admin-dashboard'))

class PendingTrailsViewTests(TestCase):
    def test_pending_trails(self):
        user = User.objects.create_user(username='adminuser', password='adminpassword', is_staff=1, is_superuser=1)
        self.client.login(username='adminuser', password='adminpassword')
        response = self.client.get(reverse('pending-trails'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "trailQuest/html-admin/pending-trails.html")

    def test_unauthenticated_pending_trails(self):
        response = self.client.get(reverse('pending-trails'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('pending-trails'))

class ManageUserViewTests(TestCase):
    def test_manage_user(self):
        user = User.objects.create_user(username='adminuser', password='adminpassword', is_staff=1, is_superuser=1)
        self.client.login(username='adminuser', password='adminpassword')
        response = self.client.get(reverse('manage-user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "trailQuest/html-admin/manage-user.html")

    def test_unauthenticated_manage_user(self):
        response = self.client.get(reverse('manage-user'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('manage-user'))

class ReviewReportViewTests(TestCase):
    def test_review_report(self):
        user = User.objects.create_user(username='adminuser', password='adminpassword', is_staff=1, is_superuser=1)
        self.client.login(username='adminuser', password='adminpassword')
        response = self.client.get(reverse('review-report'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "trailQuest/html-admin/review-report.html")

    def test_unauthenticated_review_report(self):
        response = self.client.get(reverse('review-report'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('review-report'))

class ApproveTrailViewTests(TestCase):
    def test_approve_trail(self):
        user = User.objects.create_user(username='adminuser', password='adminpassword', is_staff=1, is_superuser=1)
        self.client.login(username='adminuser', password='adminpassword')
        trail = Trail.objects.create(
            id=1,
            name="Test Trail",
            location="Blue Mountains",
            latitude=Decimal("-33.712345"),
            longitude=Decimal("150.312345"),
            start_point="Echo Point",
            end_point="Scenic World",
            distance=Decimal("5.50"),
            elevation_gain=Decimal("120.25"),
            difficulty_level="Intermediate",
            trail_type="Loop",
            estimated_time=Decimal("2.00"),
            trail_conditions="Rocky, Steep",
            accessibility="child-friendly, dog-friendly",
            user_notes="Scenic walk with great views.",
            date_submitted=timezone.now(),
            status="pending"
        )
        response = self.client.get(reverse('approve-trail-detail', kwargs={'trail_id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "trailQuest/html-admin/approve-trail.html")

    def test_approve_trail_not_found(self):
        user = User.objects.create_user(username='adminuser', password='adminpassword', is_staff=True, is_superuser=True)
        self.client.login(username='adminuser', password='adminpassword')
        response = self.client.get(reverse('approve-trail-detail', kwargs={'trail_id': 999}))
        self.assertEqual(response.status_code, 404)
