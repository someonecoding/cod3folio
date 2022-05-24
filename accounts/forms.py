from email.mime import image
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Profile, ProfileSkill, Project
from .validators import email_user_exists
from .tasks import confirm_email



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = '__all__'



class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    username = forms.CharField(required=True, max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}))

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password1', 'password2')



class ResendEmailForm(forms.Form):
    email = forms.EmailField(max_length=100, validators=[email_user_exists], widget=forms.TextInput(attrs={'placeholder': 'Email'}))

    def resend_email(self):
        confirm_email.delay(CustomUser.objects.get(email=self.cleaned_data['email']).pk)



class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))


class CreateSkillForm(forms.ModelForm):
    
    level = forms.ChoiceField(choices=[(i,i) for i in range(1,6)])
    
    class Meta:
        model = ProfileSkill
        exclude = ('profile',)


class UpdateSkillForm(forms.ModelForm):
    
    level = forms.ChoiceField(choices=[(i,i) for i in range(1,6)])
    
    class Meta:
        model = ProfileSkill
        fields = ('level',)



class OnlyInputImageWidget(forms.widgets.ClearableFileInput):
    template_name = "accounts/image_widget.html"



class UpdateProfileForm(forms.ModelForm):

    image = forms.ImageField(widget=OnlyInputImageWidget(attrs={'class': 'imgs'}))

    class Meta:

        model = Profile
        exclude = ('user',)



class CreateProjectForm(forms.ModelForm):

    title = forms.CharField(min_length=5)   

    class Meta:
        model = Project
        exclude = ('user', 'slug')