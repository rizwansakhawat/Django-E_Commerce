from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

# Create your views here.

class AboutUsView(TemplateView):
    template_name = 'about_us.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'About Us'
        return context


class ContactUsView(TemplateView):
    template_name = 'contact_us.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Contact Us'
        return context


class FAQView(TemplateView):
    template_name = 'faq.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'FAQ'
        return context


class PolicyView(TemplateView):
    template_name = 'policy.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Privacy Policy'
        return context
