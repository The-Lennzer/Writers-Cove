from django.urls import path
from . import views
urlpatterns = [
    path('editor/', views.EditorView.as_view(), name="editor"),
    path('editor/<int:story_id>', views.EditorView.as_view(), name="edit-editor"),
    path('prompt/', views.PromptEngineView.as_view(), name="prompts"),
    path('delete/<int:story_id>/', views.StoryDeleteView.as_view(), name="delete_story"),
]