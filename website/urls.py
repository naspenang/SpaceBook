from django.urls import path
from . import views
from . import views_branch


urlpatterns = [
    path("", views.home, name="home"),
    path("profile/", views.profile, name="profile"),
    path("about/", views.about, name="about"),
    path("blank/", views.blank, name="blank"),
    # Branch routes
    path("branch/create/", views_branch.branch_create, name="branch_add"),
    path("branch/edit/<str:code>/", views_branch.branch_edit, name="branch_edit"),
    path("branch/delete/<str:code>/", views_branch.branch_delete, name="branch_delete"),
]
