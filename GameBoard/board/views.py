from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .models import Ad, Feedback
from .forms import AdForm
from .filters import AdFilter
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from .models import BaseRegisterForm
import random
import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_users'] = not self.request.user.groups.filter(name='Users').exists()
        return context


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'

class AdList(ListView):
    model = Ad
    ordering = 'user'
    template_name = 'ads.html'
    context_object_name = 'ads'
    paginate_by = 3

class FeedList(ListView):
    model = Feedback
    ordering = 'author'
    template_name = 'private_page.html'
    context_object_name = 'feeds'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = AdFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

    @login_required
    def get_feedback(request, pk):
        user = request.user
        feedback = Feedback.objects.get(id=pk)
        feedback.authors.add(user)

        message = 'На ваше объявление появился новый отклик'
        return render(request, 'private_page.html', {'feedback': feedback, 'message': message})

class AdCreate(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
    form_class = AdForm
    model = Ad
    template_name = 'ads_create.html'


class AdUpdate(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
    form_class = AdForm
    model = Ad
    template_name = 'ads_edit.html'


class AdDetail(DetailView):
    model = Ad
    template_name = 'ads_detail.html'
    context_object_name = 'ad'


def generate_code():
    random.seed()
    return str(random.randint(10000,99999))

def register(request):
    if not request.user.is_authenticated:
        if request.POST:
            form = UserCreationForm(request.POST or None)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                email = form.cleaned_data.get('email')
                my_password1 = form.cleaned_data.get('password1')
                u_f = User.objects.get
                code = generate_code()
                if User.objects.filter(code=code):
                    code = generate_code()

                message = code
                user = authenticate(username=username, password=my_password1)
                now = datetime.datetime.now()

                User.objects.create(user=u_f, code=code, date=now)

                if user.is_active:
                    login(request, user)
                    return redirect('/privatepage/')
                else:
                    form.add_error(None, 'Аккаунт не активирован')
                    return redirect('/')

            else:
                return render(request, '/signup.html', {'form': form})
        else:
            return render(request, 'signup.html', {'form':
            UserCreationForm()})
    else:
        return redirect('/privatepage/')

def endreg(request):
    if  request.user.is_authenticated:
        return redirect('/privatepage/')
    else:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                code_use = form.cleaned_data.get("code")
                if User.objects.filter(code=code_use):
                    profile = User.objects.get(code=code_use)
                else:
                    form.add_error(None, "Код подтверждения не совпадает.")
                    return render(request, 'registration/activation_code_form.html', {'form': form})
                if User.is_active == False:
                    User.is_active = True
                    User.save()

                    login(request, profile.user)
                    profile.delete()
                    return redirect('/privatepage/')
                else:
                    form.add_error(None, '1Unknown or disabled account')
                    return render(request, '/', {'form': form})
            else:
                return render(request, '/', {'form': form})
        else:
            form = UserCreationForm()
            return render(request, '/', {'form': form})

