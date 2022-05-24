import time
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from django.utils.text import slugify



class CustomUser(AbstractUser):
    email_verified = models.BooleanField(default=False)



class Skill(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title



class Profile(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    position = models.CharField(max_length=100, default='Developer')
    image = models.ImageField(upload_to='avatars', default='../static/img/defaultuser.jpg', blank=True)
    name = models.CharField(max_length=100, default='', blank=True)
    surname = models.CharField(max_length=100, default='', blank=True)
    bio = models.TextField(max_length=500, default='', blank=True)
    linkedin = models.CharField(max_length=100, default='', blank=True)
    github = models.CharField(max_length=100, default='', blank=True)


    def get_absolute_url(self):
        return reverse("accounts:profile", kwargs={"pk": self.pk})
    
    def get_full_name(self):
        return f'{self.name} {self.surname}'

    def __str__(self):
        return f'profile: {self.user.username}'



class ProfileSkill(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profileskills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    level = models.IntegerField(choices=[(i,i) for i in range(1,6)], validators=[MinValueValidator(limit_value=0, message='0 to 5'), MaxValueValidator(limit_value=5, message='0 to 5')])

    class Meta:
        unique_together = ('profile', 'skill')

    def __str__(self):
        return f'{self.profile.user.username} | {self.skill.title} | {self.level}'

    def get_delete_url(self):
        return reverse("accounts:skill-delete", kwargs={"pk": self.profile.user.pk, "skill_name": self.skill.title})




class Project(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=500, validators=[
        MinLengthValidator(50, 'Description must contain at least 50 characters.')
    ])
    source = models.URLField(max_length=200, blank=True)
    slug = models.SlugField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title) + str(time.time_ns())
        return super(Project, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("accounts:project-detail", kwargs={"pk": self.user.pk, "slug": self.slug})
    



class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='project_images')

# SIGNALS

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=CustomUser)