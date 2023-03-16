from django.urls import path
from . import views

urlpatterns = [
    path("password_reset/", views.password_reset, name="password_reset_form"),
    path("password_reset_confirm/<int:id>/<token>/", views.password_reset_confirm, name="password_reset_confirm",),
    path("confirm_correctness/<str:model_name>/<int:id>/<token>/", views.confirm_correctness, name="confirm_correctness"),
]
