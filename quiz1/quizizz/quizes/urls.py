from django.urls import path
from .views import handle_400, handle_403, handle_404, handle_500
from .views import (
    QuizListView,
    quiz_view,
    quiz_data_view,
    save_quiz_view
)

app_name = 'quizes'

urlpatterns = [
    path('', QuizListView.as_view(), name='main-view'),
    path('quiz/<slug:slug>/', quiz_view, name='quiz-view'),
    path('quiz/<slug:slug>/save/', save_quiz_view, name='save-view'),
    path('quiz/<slug:slug>/data/', quiz_data_view, name='quiz-data-view'),
]

handler400 = handle_400
handler403 = handle_403
handler404 = handle_404
handler500 = handle_500
