from django.shortcuts import render
from django.views.generic import TemplateView,FormView
from django.core.mail import send_mail
from django.conf import settings
from .models import *
from .froms import *

class HomePageView(FormView):
    template_name = 'home.html'
    form_class = ContactForm
    success_url = '/'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['about'] = AboutMe.objects.latest('-id')
        context['skills'] = Skill.objects.all().order_by('-id')
        context['jobs'] = Jobs.objects.all().order_by('-id')
        context['services'] = Service.objects.all().order_by('-id')
        context['statistics'] = Statistics.objects.all()
        context['portfolio'] = Portfolio.objects.all()
        return context

    def form_valid(self, form):
        Name = form.cleaned_data.get('name')
        Email = form.cleaned_data.get('email')
        Subject = form.cleaned_data.get('subject')
        Message = form.cleaned_data['message']
        msg = f"""
        Hello Sir,

        I am {Name} and my email is {Email} .

        All Details is {Message}.

        Thank You!
        """
        send_mail( 
            Subject,
            msg,
            Email,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
        return super().form_valid(form)
          


class ProjectDetailView(TemplateView):
    template_name = 'project-details.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['about'] = AboutMe.objects.latest('id')
        context['jobs'] = Jobs.objects.all().order_by('-id')
        context['portfolio'] = Portfolio.objects.get(id = self.kwargs['pk'])
        return context
        