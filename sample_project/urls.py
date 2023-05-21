from django.urls import path

from sample_project import views

urlpatterns = [
    path("protected/", views.ProtectedView.as_view(), name="protected_view"),
    path("public/", views.PublicView.as_view(), name="public_view"),
    path("public2/", views.PublicView2.as_view(), name="public_view2"),
    path("public3/", views.public_view3, name="public_view3"),
]
