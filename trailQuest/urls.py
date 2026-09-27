from django.urls import path
from trailQuest import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("login/register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    path("review-trail/<int:trail_id>", views.review_trail, name="review-trail"),
    path("comment/", views.comment, name="comment"),

    path("search-trail-form/", views.search_trail_form, name="search-trail-form"),
    path("search-trail-direct/", views.search_trail_direct, name="search-trail-direct"),
    path("submit-trail/", views.submit_trail, name="submit-trail"),
    path("view-trail/<int:trail_id>", views.view_trail, name="view-trail"),

    path("admin-dashboard/", views.admin_dashboard, name="admin-dashboard"),
    path("pending-trails/", views.pending_trails, name="pending-trails"),
    path("approve-trail/<int:trail_id>/", views.approve_trail_detail, name="approve-trail-detail"),
    path("manage-user/", views.manage_user, name="manage-user"),
    path("review-report/", views.review_report, name="review-report"),
]
