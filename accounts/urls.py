from django.urls import path
from .views import *
from .forms import CustomAuthForm

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('signup/resend-email', ResendActivationView.as_view(), name='resend-email'),
    path('login/', CLoginView.as_view(authentication_form=CustomAuthForm), name='login'),
    path('logout/', CLogoutView.as_view(), name='logout'),
    path('activate/<uidb64>/<token>/', AccountActivateView.as_view(), name='activate'),
    path('profile/<pk>/', UserProfileView.as_view(), name='profile'),
    path('profile/<pk>/edit/<skill_name>/delete', ProfileSkillDeleteView.as_view(), name='skill-delete'),
    path('profile/<pk>/edit', UserProfileUpdateView.as_view(), name='profile-update'),
    path('profile/<pk>/projects', ProjectListView.as_view(), name='projects'),
    path('profile/<pk>/projects/create', ProjectCreateView.as_view(), name='project-create'),
    path('profile/<pk>/projects/<slug:slug>/edit', ProjectEditView.as_view(), name='project-edit'),
    path('profile/<pk>/projects/<slug:slug>/delete', ProjectDeleteView.as_view(), name='project-delete'),
    path('profile/<pk>/projects/<slug:slug>/edit/delete-img/<img_pk>', ProjectImgDeleteView.as_view(), name='project-delete-img'),
    path('profile/<pk>/projects/<slug:slug>', ProjectDetailView.as_view(), name='project-detail'),
]