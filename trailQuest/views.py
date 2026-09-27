from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction
from .models import Trail, Review
from decimal import Decimal
import re
from django.utils import timezone
from decimal import Decimal, InvalidOperation

# Create your views here.

def home(request):
    trails = Trail.objects.filter(status="approved")
    print(trails)

    current_time = timezone.now()

    return render(request, "trailQuest/home.html", {'trails': trails, 'current_time': current_time})

def is_admin(user):
    return user.is_staff or user.is_superuser

def login_view(request):
    username_error = None
    password_error = None
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            username_error = "The username does not exist."
            return render(request, "registration/login.html", {"username_error": username_error})

        else:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)  # create session
                # Check if user is admin and redirect accordingly
                if is_admin(user):
                    return redirect('admin-dashboard')
                else:
                    return redirect('home')
            else:
                password_error = "The password is incorrect."
                return render(request, "registration/login.html", {"password_error": password_error})
    
    return render(request, "registration/login.html", {"username_error": username_error, "password_error": password_error})

def view_trail(request, trail_id):
    trail = get_object_or_404(Trail, id=trail_id)

    if not trail.photos:
        trail.photos =  "trail_photos/No_Preview_image_2.png"

    reviews = Review.objects.filter(trail=trail).select_related('user')


    return render(request, "trailQuest/html-trail/view-trail.html", {'trail': trail, 'reviews': reviews})

def register(request):
    # username_error = None
    register_error = []

    if request.method == 'POST':
        email = request.POST.get('email')
        # username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            register_error = "Please enter a valid email address."
            return render(request, "trailQuest/html-user/register.html", {"register_error": register_error})
        
        password_errors = []

        if len(password) < 8:
            password_errors.append("Minimum 8 characters.")
        if not re.search(r"[a-z]", password):
            password_errors.append("At least one lowercase letter.")
        if not re.search(r"[A-Z]", password):
            password_errors.append("At least one uppercase letter.")
        if not re.search(r"[0-9]", password):
            password_errors.append("At least one number.")
        if not re.search(r"[!@#$%^&*()_+={}\[\].,?\-]", password):
            password_errors.append("At least one special character (!@#$%^&* etc.).")

        # IF WEEAK
        if password_errors:
            return render(request, "trailQuest/html-user/register.html", {
                "register_error": " ".join(password_errors)
            })
        
        # IF MISMATCHED
        if password != confirm_password:
            return render(request, "trailQuest/html-user/register.html", {
                "register_error": "Passwords do not match."
            })
            
        # if User.objects.filter(username=username).exists():
        #     username_error = "This username already exist."
        #     return render(request, "trailQuest/html-user/register.html", {"username_error": username_error})

        try:
            user = User.objects.create_user(username =email, password=password)
        except Exception as e:
            register_error = "This email already exists."
            print(f"User creation failed: {e}")
            return render(request, "trailQuest/html-user/register.html", {"register_error": register_error})

        try:
            user.save()
            login(request, user)
            return redirect('home')
        except Exception as e:
            register_error = "User creation failed."
            print(f"User creation failed: {e}")
            return render(request, "trailQuest/html-user/register.html", {"register_error": register_error})
        
    return render(request, "trailQuest/html-user/register.html")

@login_required
def profile(request):
    return render(request, "trailQuest/html-user/profile.html")

@login_required
def review_trail(request, trail_id):
    if request.user.is_staff or request.user.is_superuser:
        messages.error(request, "Administrators are not allowed to review trails.")
        return redirect('home')
    
    trail = get_object_or_404(Trail, id=trail_id)

    if request.method == "POST":
        rating = request.POST.get('rating')

        if not rating or not rating.isdigit() or not (1 <= int(rating) <= 5):
            messages.error(request, "Rating must be between 1 and 5.")
            return render(request, "trailQuest/html-user/review-trail.html", {"trail": trail})

        Review.objects.create(
            user=request.user,
            trail=trail,
            rating=rating,
            comment=request.POST.get('reviewComment'),
        )
        messages.success(request, f"Review of '{trail.name}' was submitted successfully and is pending admin approval.")
        return redirect('view-trail', trail_id=trail.id)

    return render(request, "trailQuest/html-user/review-trail.html", {"trail": trail})

@login_required
def comment(request):
    return render(request, "trailQuest/html-user/comment.html")

def search_trail_direct(request):
    trails = Trail.objects.filter(status="approved")

    name = request.GET.get('trailName')
    if name:
        trails = trails.filter(name__icontains=name)

    return render(request, "trailQuest/home.html", {'trails': trails})

def search_trail_form(request):
    trails = Trail.objects.filter(status="approved")

    name = request.GET.get('trailName')
    location = request.GET.get('location')
    difficulty_level = request.GET.get('difficultyLevel')
    min_distance = request.GET.get('minDist')
    max_distance = request.GET.get('maxDist')
    trail_type = request.GET.get('trailType')

    if name:
        trails = trails.filter(name__icontains=name)

    if location:
        trails = trails.filter(location__icontains=location)

    if difficulty_level:
        trails = trails.filter(difficulty_level=difficulty_level)

    if min_distance:
        try:
            min_val = Decimal(min_distance)
            trails = trails.filter(distance__gte=min_val)
        except (InvalidOperation, ValueError):
            pass  # Ignore invalid min value

    if max_distance:
        try:
            max_val = Decimal(max_distance)
            trails = trails.filter(distance__lte=max_val)
        except (InvalidOperation, ValueError):
            pass  # Ignore invalid max value

    if trail_type:
        trails = trails.filter(trail_type=trail_type)

    return render(request, "trailQuest/home.html", {'trails': trails})

@login_required
def submit_trail(request):
    if request.user.is_staff or request.user.is_superuser:
        messages.error(request, "Administrators are not allowed to submit trails.")
        return redirect('home')
    
    if request.method == 'POST':
        # Collect all form variables
        trail_name = request.POST.get('trailName')
        location = request.POST.get('location')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        start_point = request.POST.get('startPoint')
        end_point = request.POST.get('endPoint')
        distance = request.POST.get('distance')
        elevation_gain = request.POST.get('elevationGain')
        difficulty_level = request.POST.get('difficultyLevel')
        trail_type = request.POST.get('trailType')
        estimated_time = request.POST.get('estimatedTime')
        trail_conditions = request.POST.get('trailConditions')
        accessibility = request.POST.get('accessibility')
        user_notes = request.POST.get('userNotes')
        photos = request.FILES.get('photos')
        
        # Initialize error variables
        errors = {}
        
        # Required fields validation:

        if not trail_name:
            errors['name_error'] = "Trail name is required."
        elif not re.match(r'^[a-zA-Z0-9\s-]+$', trail_name):
            errors['name_error'] = "Trail name can only contain letters, numbers, spaces, and hyphens."
            
        if not location:
            errors['location_error'] = "Location is required."
        elif not re.match(r'^[a-zA-Z0-9\s-]+$', location):
            errors['location_error'] = "Location can only contain letters, numbers, spaces, and hyphens."
        
        # Distance validation
        try:
            dist_val = float(distance)
            if dist_val <= 0:
                errors['distance_error'] = "Distance must be greater than 0 kilometers."
        except (ValueError, TypeError):
            errors['distance_error'] = "Valid distance is required."
            
        # Elevation validation
        try:
            elev_val = float(elevation_gain)
            if elev_val < 0:
                errors['elevation_gain_error'] = "Elevation gain cannot be negative."
        except (ValueError, TypeError):
            errors['elevation_gain_error'] = "Valid elevation gain is required."

        # Difficulty level validation
        if not difficulty_level:
            errors['difficulty_level_error'] = "Difficulty level is required."
            
        # Trail type validation
        if not trail_type:
            errors['trail_type_error'] = "Trail type is required."
            
        # Estimated time validation
        try:
            time_val = float(estimated_time)
            if time_val <= 0:
                errors['estimated_time_error'] = "Estimated time must be greater than 0 hours."
        except (ValueError, TypeError):
            errors['estimated_time_error'] = "Valid estimated time is required."
        
        # Optional fields validation:

        # Coordinates validation
        if latitude:  # user entered something
            try:
                latitude = float(latitude)
                if latitude < -90 or latitude > 90:
                    errors['latitude_error'] = "Latitude must be between -90 and 90 degrees."
            except (ValueError, TypeError):
                errors['latitude_error'] = "Please enter a valid latitude."

        if longitude:  
            try:
                longitude = float(longitude)
                if longitude < -180 or longitude > 180:
                    errors['longitude_error'] = "Longitude must be between -180 and 180 degrees."
            except (ValueError, TypeError):
                errors['longitude_error'] = "Please enter a valid longitude."
        
        # Start point validation 
        if start_point and not re.match(r'^[a-zA-Z0-9\s-]+$', start_point):
            errors['start_point_error'] = "Start point can only contain letters, numbers, spaces, and hyphens."
            
        # End point validation 
        if end_point and not re.match(r'^[a-zA-Z0-9\s-]+$', end_point):
            errors['end_point_error'] = "End point can only contain letters, numbers, spaces, and hyphens."
            
        # Trail conditions validation 
        if trail_conditions and not re.match(r'^[a-zA-Z0-9\s-]+$', trail_conditions):
            errors['trail_conditions_error'] = "Trail conditions can only contain letters, numbers, spaces, and hyphens."
            
        # Accessibility validation (if provided)
        if accessibility and not re.match(r'^[a-zA-Z0-9\s-]+$', accessibility):
            errors['accessibility_error'] = "Accessibility info can only contain letters, numbers, spaces, and hyphens."
            
        # User notes validation (if provided)
        if user_notes and not re.match(r'^[a-zA-Z0-9\s,.-]+$', user_notes):
            errors['user_notes_error'] = "Notes can only contain letters, numbers, spaces, periods, commas, and hyphens."
        
        # Photo validation (if provided)
        if photos:
            if not photos.content_type.startswith('image/'):
                errors['photos_error'] = "Only image files are allowed."
        
        # If there are validation errors, return the form with errors
        if errors:
            return render(request, "trailQuest/html-trail/submit-trail.html", {
                **errors,  
            })

            
        # If no validation errors, save the trail to the database
        try:
            # Create a new Trail object
            new_trail = Trail(
                name=trail_name,
                location=location,
                latitude=Decimal(latitude) if latitude else None, # convert only if
                longitude=Decimal(longitude) if longitude else None,
                start_point=start_point,
                end_point=end_point,
                distance=Decimal(distance),
                elevation_gain=Decimal(elevation_gain),
                difficulty_level=difficulty_level,
                trail_type=trail_type,
                estimated_time=Decimal(estimated_time),
                trail_conditions=trail_conditions,
                accessibility=accessibility,
                photos=photos,
                user_notes=user_notes,
                status='pending',  # Set default status to pending
                date_submitted=timezone.now()
            )
                
            # Save the trail to the database
            new_trail.save()
            
            # Redirect to success page or trail details page
            messages.success(request, f"Trail '{trail_name}' was submitted successfully and is pending admin approval.")
            return redirect('home')  # Or redirect to a trail detail page
            
        except Exception as e:
            # If there's an error saving to the database
            print("Error saving trail:", str(e))
            messages.error(request, "There was an error submitting your trail. Please try again.")
            return render(request, "trailQuest/html-trail/submit-trail.html")
            
    return render(request, "trailQuest/html-trail/submit-trail.html")

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, "trailQuest/html-admin/admin-dashboard.html")

@login_required
@user_passes_test(is_admin)
def pending_trails(request):
    # Get all pending trails
    pending_trails = Trail.objects.filter(status='pending').order_by('-date_submitted')
    return render(request, "trailQuest/html-admin/pending-trails.html", {'pending_trails': pending_trails})

@login_required
@user_passes_test(is_admin)
def approve_trail_detail(request, trail_id):
    trail = get_object_or_404(Trail, id=trail_id)

    if request.method == 'POST':
        # Collect form inputs
        trail_name = request.POST.get('trail_name')
        location = request.POST.get('location')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        start_point = request.POST.get('start_point')
        end_point = request.POST.get('end_point')
        distance = request.POST.get('distance')
        elevation_gain = request.POST.get('elevation_gain')
        difficulty_level = request.POST.get('difficulty_level')
        trail_type = request.POST.get('trail_type')
        estimated_time = request.POST.get('estimated_time')
        trail_conditions = request.POST.get('trail_conditions')
        accessibility = request.POST.get('accessibility')
        user_notes = request.POST.get('user_notes')
        status = request.POST.get('approval_status')
        admin_comments = request.POST.get('admin_comments')

        errors = {}

        # Required field validation
        if not trail_name:
            errors['name_error'] = "Trail name is required."
        elif not re.match(r'^[a-zA-Z0-9\s-]+$', trail_name):
            errors['name_error'] = "Trail name can only contain letters, numbers, spaces, and hyphens."

        if not location:
            errors['location_error'] = "Location is required."
        elif not re.match(r'^[a-zA-Z0-9\s-]+$', location):
            errors['location_error'] = "Location can only contain letters, numbers, spaces, and hyphens."

        try:
            dist_val = float(distance)
            if dist_val <= 0:
                errors['distance_error'] = "Distance must be greater than 0 kilometers."
        except (ValueError, TypeError):
            errors['distance_error'] = "Valid distance is required."

        try:
            elev_val = float(elevation_gain)
            if elev_val < 0:
                errors['elevation_gain_error'] = "Elevation gain cannot be negative."
        except (ValueError, TypeError):
            errors['elevation_gain_error'] = "Valid elevation gain is required."

        if not difficulty_level:
            errors['difficulty_level_error'] = "Difficulty level is required."

        if not trail_type:
            errors['trail_type_error'] = "Trail type is required."

        try:
            time_val = float(estimated_time)
            if time_val <= 0:
                errors['estimated_time_error'] = "Estimated time must be greater than 0 hours."
        except (ValueError, TypeError):
            errors['estimated_time_error'] = "Valid estimated time is required."

        # Optional fields
        if latitude:
            try:
                latitude = float(latitude)
                if latitude < -90 or latitude > 90:
                    errors['latitude_error'] = "Latitude must be between -90 and 90 degrees."
            except (ValueError, TypeError):
                errors['latitude_error'] = "Please enter a valid latitude."

        if longitude:
            try:
                longitude = float(longitude)
                if longitude < -180 or longitude > 180:
                    errors['longitude_error'] = "Longitude must be between -180 and 180 degrees."
            except (ValueError, TypeError):
                errors['longitude_error'] = "Please enter a valid longitude."

        if start_point and not re.match(r'^[a-zA-Z0-9\s-]+$', start_point):
            errors['start_point_error'] = "Start point can only contain letters, numbers, spaces, and hyphens."

        if end_point and not re.match(r'^[a-zA-Z0-9\s-]+$', end_point):
            errors['end_point_error'] = "End point can only contain letters, numbers, spaces, and hyphens."

        if trail_conditions and not re.match(r'^[a-zA-Z0-9\s-]+$', trail_conditions):
            errors['trail_conditions_error'] = "Trail conditions can only contain letters, numbers, spaces, and hyphens."

        if accessibility and not re.match(r'^[a-zA-Z0-9\s-]+$', accessibility):
            errors['accessibility_error'] = "Accessibility info can only contain letters, numbers, spaces, and hyphens."

        if user_notes and not re.match(r'^[a-zA-Z0-9\s,.-]+$', user_notes):
            errors['user_notes_error'] = "Notes can only contain letters, numbers, spaces, periods, commas, and hyphens."

        # Admin-only fields
        if not status:
            errors['status_error'] = "Please select an approval status."

        if admin_comments and not re.match(r'^[a-zA-Z0-9\s.,-]+$', admin_comments):
            errors['comment_error'] = "Comments can only include letters, numbers, spaces, periods, commas, and hyphens."

        if errors:
            return render(request, "trailQuest/html-admin/approve-trail.html", {
                'trail': trail,
                **errors
            })

        # All validated, update trail
        trail.name = trail_name
        trail.location = location
        trail.latitude = Decimal(latitude) if latitude else None
        trail.longitude = Decimal(longitude) if longitude else None
        trail.start_point = start_point
        trail.end_point = end_point
        trail.distance = Decimal(dist_val)
        trail.elevation_gain = Decimal(elev_val)
        trail.difficulty_level = difficulty_level
        trail.trail_type = trail_type
        trail.estimated_time = Decimal(time_val)
        trail.trail_conditions = trail_conditions
        trail.accessibility = accessibility
        trail.user_notes = user_notes
        trail.status = status
        trail.admin_comments = admin_comments
        trail.approved_by = request.user

        trail.save()

        messages.success(request, f"Trail '{trail.name}' has been {status}.")
        return redirect('pending-trails')

    return render(request, "trailQuest/html-admin/approve-trail.html", {'trail': trail})


@login_required
@user_passes_test(is_admin)
def manage_user(request):
    return render(request, "trailQuest/html-admin/manage-user.html")

@login_required
@user_passes_test(is_admin)
def review_report(request):
    return render(request, "trailQuest/html-admin/review-report.html")