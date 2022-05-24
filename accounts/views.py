from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.contrib.auth import login, logout


from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from .tokens import account_activation_token


from .models import CustomUser, ProfileSkill, Project, ProjectImage, Skill
from django.views import View
from django.views.generic import TemplateView, CreateView, DetailView, ListView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from .forms import SignUpForm, ResendEmailForm, UpdateProfileForm, UpdateSkillForm, CreateProjectForm, CreateSkillForm
from django.forms import modelformset_factory
from .tasks import confirm_email
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import *
from .permissions import *



class SignupView(LogoutRequiredMixin, CreateView):
    
    form_class = SignUpForm
    success_url = reverse_lazy('accounts:resend-email')
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
        user = form.save(commit=True)
        confirm_email.delay(user.pk)  
        return redirect(self.success_url + f'?email={form.cleaned_data.get("email")}')



class ResendActivationView(LogoutRequiredMixin, FormView):

    form_class = ResendEmailForm
    template_name = 'accounts/resend.html'
    success_url = reverse_lazy('accounts:resend-email')


    def get_initial(self):
        initial = super().get_initial()
        initial['email'] = self.request.GET.get('email')
        return initial

    def form_valid(self, form):
        form.resend_email()
        return super().form_valid(form)



class AccountActivateView(LogoutRequiredMixin, TemplateView):

    template_name = 'accounts/activate.html'
    context_object_name = 'context'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        
        try:
            uid = force_text(urlsafe_base64_decode(kwargs['uidb64']))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        try:
            if user is not None and account_activation_token.check_token(user, kwargs['token']) and user.email_verified == False:
                user.email_verified = True
                user.save()
                login(request, user)
            
                return redirect(reverse_lazy('home'))
            
            elif user.email_verified:
                kwargs['message'] = 'Your email is already verified!'
                return super().get(request, *args, **kwargs)
            
            else:
                kwargs['message'] = 'Invalid link or link expired!'
                return super().get(request, *args, **kwargs)

        except:
            return redirect(reverse_lazy('home'))
            


class CLoginView(LogoutRequiredMixin, LoginView):
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('home')
    


class CLogoutView(LoginRequiredMixin, LogoutView):
    login_url = reverse_lazy('accounts:login')

    def get(self, request):
        logout(request)
        return redirect('home')



class UserProfileView(DetailView):
    model = CustomUser
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['skills'] = ProfileSkill.objects.filter(profile=kwargs.get('object').profile).order_by('skill__title')
        return context

 
class UserProfileUpdateView(IsProfileOwnerMixin, View):
    template_name = 'accounts/profile_edit.html'
    skills_formset = modelformset_factory(ProfileSkill, extra=0, form=UpdateSkillForm)
    
    def get_context_data(self, **kwargs):
        if 'profile_form' not in kwargs:
            kwargs['profile_form'] = UpdateProfileForm(instance=self.request.user.profile)
        if 'skills_form' not in kwargs:
            kwargs['skills_form'] = self.skills_formset(queryset=ProfileSkill.objects.filter(profile=self.request.user.profile))
        if 'skill_create_form' not in kwargs:
            kwargs['skill_create_form'] = CreateSkillForm()
            kwargs['skill_create_form'].fields['skill'].queryset = Skill.objects.exclude(id__in=[obj.skill.id for obj in self.request.user.profile.profileskills.all()])

        return kwargs


    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())


    def post(self, request, *args, **kwargs):
        req_forms = {}

        if 'add_skill' in request.POST:
            #processing skill creation form
            skill_create_form = CreateSkillForm(request.POST)
            skill_create_instance = skill_create_form.save(commit=False)
            skill_create_instance.profile = request.user.profile
            skill_create_instance.save()

            
        else:
            #processing profile form
            profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
            if profile_form.is_valid():
                profile_form.save(commit=True)
            else:
                req_forms['profile_form'] = profile_form
        
            # processing skills formset
            skills_form = self.skills_formset(request.POST, queryset=ProfileSkill.objects.filter(profile=self.request.user.profile))
            if skills_form.is_valid():
                skills_form.save()
            else:
                req_forms['skills_form'] = skills_form

        return render(request, self.template_name, self.get_context_data(**req_forms))



class ProjectCreateView(IsProfileOwnerMixin, CreateView):
    form_class = CreateProjectForm
    success_url = reverse_lazy('home')
    template_name = 'accounts/project_create.html'

    def get_context_data(self, **kwargs):
        kwargs['pk'] = self.kwargs.get('pk')
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        project = form.save(commit=False)
        project.user = CustomUser.objects.get(pk=self.kwargs.get('pk'))
        project.save()

        project_img_list = []
        for img in self.request.FILES.getlist('imgs'):
            project_img_list.append(ProjectImage(project=project, image=img))

        ProjectImage.objects.bulk_create(project_img_list)

        return redirect(self.success_url)



class ProjectListView(ListView):
    model = Project
    template_name = 'accounts/projects_list.html'
    context_object_name = 'projects'
    
    def get_context_data(self, **kwargs):
        kwargs['pk'] = int(self.kwargs.get('pk'))
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return Project.objects.filter(user=CustomUser.objects.get(pk=self.kwargs.get('pk')))



class ProjectDetailView(DetailView):
    model = Project
    template_name = 'accounts/project_detail.html'
    context_object_name = 'project'
    
    def get_object(self):
        return get_object_or_404(Project, user=CustomUser.objects.get(pk=self.kwargs.get('pk')), slug=self.kwargs.get('slug'))



class ProjectEditView(IsProfileOwnerMixin, UpdateView):
    model = Project
    form_class = CreateProjectForm
    template_name = 'accounts/project_edit.html'

    def get_context_data(self, **kwargs):
        kwargs['slug'] = self.kwargs.get('slug')
        return super().get_context_data(**kwargs)

    def get_object(self):
        return get_object_or_404(Project, user=CustomUser.objects.get(pk=self.kwargs.get('pk')), slug=self.kwargs.get('slug'))

    def form_valid(self, form):
        project = form.save(commit=False)
        project.user = CustomUser.objects.get(pk=self.kwargs.get('pk'))
        project.save()

        project_img_list = []
        for img in self.request.FILES.getlist('imgs'):
            project_img_list.append(ProjectImage(project=project, image=img))

        ProjectImage.objects.bulk_create(project_img_list)

        print(project.slug)

        return redirect(reverse_lazy('accounts:project-edit', kwargs={'pk': self.request.user.pk, 'slug': project.slug}))



class ProjectImgDeleteView(IsProfileOwnerMixin, DeleteView):
    model = ProjectImage

    def get_object(self):
        return ProjectImage.objects.get(pk=self.kwargs.get('img_pk'))

    def get(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('accounts:project-edit', kwargs={
            'pk': self.kwargs.get('pk'),
            'slug': self.kwargs.get('slug')
            })



class ProjectDeleteView(IsProfileOwnerMixin, DeleteView):
    model = Project

    def get_object(self):
        return Project.objects.get(slug=self.kwargs.get('slug'))

    def get(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('accounts:projects', kwargs={
            'pk': self.request.user.pk
        })



class ProfileSkillDeleteView(IsProfileOwnerMixin, DeleteView):
    model = ProfileSkill

    def get_object(self):
        return ProfileSkill.objects.get(
            profile=self.request.user.profile,
            skill=Skill.objects.get(title=self.kwargs.get('skill_name'))
        )

    def get(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('accounts:profile-update', kwargs={
            'pk': self.request.user.pk
        })

