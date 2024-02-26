from django.urls import path
from .views import AdList, FeedList, AdCreate, AdUpdate, AdDetail
from django.contrib.auth.views import LoginView, LogoutView
from .views import BaseRegisterView


urlpatterns = [
   path('', AdList.as_view()),
   path('privatepage/', FeedList.as_view(), name='private_page'),
   path('create/', AdCreate.as_view(), name='ads_create'),
   path('<int:pk>/edit/', AdUpdate.as_view(), name='ads_update'),
   path('<int:pk>/', (AdDetail.as_view()), name='ads_detail'),
   path('login/', LoginView.as_view(template_name = 'login.html'),name='login'),
   path('logout/', LogoutView.as_view(template_name = 'logout.html'),name='logout'),
   path('signup/', BaseRegisterView.as_view(template_name = 'signup.html'), name='signup'),
]
