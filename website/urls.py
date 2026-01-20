# website/urls.py
from django.urls import path
from .views import views
from .views import views_branch
from .views import views_campus
from .views import views_library
from .views import views_space


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
    # Library routes
    path("library/list/", views_library.library_list, name="library_list"),
    path("library/create/", views_library.library_create, name="library_create"),
    path("library/delete/<str:library_code>/", views_library.library_delete, name="library_delete"),
    path("campus/api/by-branch/", views_campus.campus_by_branch_api, name="campus_by_branch_api",),
    path("library/edit/<str:library_code>/", views_library.library_edit, name="library_edit"),
    path("library/<str:library_code>/", views_library.library_detail, name="library_detail"),
    # Space routes
    path("space/list/", views_space.space_list, name="space_list"),
    path("space/create/", views_space.space_create, name="space_create"),
    path("space/<int:space_id>/", views_space.space_detail, name="space_detail"),
    path("space/edit/<int:space_id>/", views_space.space_edit, name="space_edit"),
    path("space/delete/<int:space_id>/", views_space.space_delete, name="space_delete"),




]
