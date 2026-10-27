from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('register/user/', views.register_user, name='register_user'),
    path('login/', views.signin, name='login'),
    path('logout/', views.signout, name='logout'),

    path('view_case/', views.view_case, name='view_case'),
    path('user_case_history/', views.user_case_history, name='user_case_history'),
    path('upload_case/', views.upload_case, name='upload_case'),

    path('view_evidence/<int:id>/', views.view_evidence, name='view_evidence'),
    path('upload_evidence/', views.upload_evidence, name='upload'),
    path('update_evidence/<int:id>/', views.update_evidence, name='update_evidence'),
    path('verify/', views.verify_evidence, name='verify'),

    path('view/officers/', views.view_officers, name='view_officers'),
    path('view/users/', views.view_users, name='view_users'),

    path('add_complaint/', views.add_complaint, name='add_complaint'),
    path('view_complaint/', views.view_complaint, name='view_complaint'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)