from django.urls import path

from . import views

urlpatterns = [
    path("create_dag", views.CreateDagAPIView.as_view()),
    path("trigger_dag", views.TriggerDagAPIView.as_view()),
    path("run_dag_list/<str:dagId>", views.DagRunsListAPIView.as_view()),
    path("pause_dag/<str:dagId>/paused/<str:pause>", views.DagPauseAPIView.as_view()),
]
