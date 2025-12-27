from django.urls import path
from .views import views
from .views import views_branch
from .views import views_campus


urlpatterns = [
    path("", views.home, name="home"),
    path("profile/", views.profile, name="profile"),
    path("about/", views.about, name="about"),
    path("blank/", views.blank, name="blank"),
    # Branch routes
    path("branch/embed/", views_branch.branch_list_embed, name="branch_list_embed"),
    path("branch/list/", views_branch.branch_list, name="branch_list"),
    path("branch/create/", views_branch.branch_create, name="branch_create"),
    path("branch/api", views_branch.branch_list_api, name="branch_list_api"),
    path("branch/<str:code>/", views_branch.branch_detail, name="branch_detail"),
    path("branch/edit/<str:code>/", views_branch.branch_edit, name="branch_edit"),
    path("branch/delete/<str:code>/", views_branch.branch_delete, name="branch_delete"),
    # Campus routes
    path("campus/list/", views_campus.campus_list, name="campus_list"),
    path("campus/create/", views_campus.campus_create, name="campus_create"),
    path("campus/edit/<str:campus_code>/", views_campus.campus_edit, name="campus_edit"),
    path("campus/delete/<str:campus_code>/", views_campus.campus_delete, name="campus_delete"),

]
