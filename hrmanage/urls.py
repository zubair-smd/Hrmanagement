from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth.views import LogoutView
from employees.views import CustomLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),  # Added proper name
    path('employees/', include('employees.urls')),
    path('', RedirectView.as_view(url='/login/', permanent=False)),
]