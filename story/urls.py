from django.urls import path
from . import views
urlpatterns = [
    path('editor/', views.EditorView.as_view(), name="editor")
]