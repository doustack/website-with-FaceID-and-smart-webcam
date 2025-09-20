from pages import views
from django.urls import path

app_name='pages'

urlpatterns = [
    path('matrix/', views.home_matrix,name='matrix'),
    path('neon/', views.home_neon, name='neon'),
    path("hand-admin-login/", views.hand_admin_login, name="hand_admin_login"),
    path('', views.home_grid, name='grid'),
]
