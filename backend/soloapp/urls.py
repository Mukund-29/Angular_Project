from django.urls import path
from . import views
from .views import LogoutView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('unit/', views.unitApi),
    path('unit/<int:id>/', views.unitApi),
    path('employee/', views.employeeApi),
    path('employee/<int:id>/', views.employeeApi),
    path('SaveImage/', views.SaveImage),
    path('logout/', LogoutView.as_view(), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
