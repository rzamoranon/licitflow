from django.urls import path
from django.views.generic import TemplateView

app_name = 'pages'

urlpatterns = [
    path('',             TemplateView.as_view(template_name='pages/index.html'), name='home'),
    path('about/',       TemplateView.as_view(template_name='pages/about.html'), name='about'),
    path('blog/',        TemplateView.as_view(template_name='pages/blog.html'), name='blog'),
    path('contact/',     TemplateView.as_view(template_name='pages/contact.html'), name='contact'),
    path('faq/',         TemplateView.as_view(template_name='pages/FAQ.html'), name='faq'),
    path('feature/',     TemplateView.as_view(template_name='pages/feature.html'), name='feature'),
    path('service/',     TemplateView.as_view(template_name='pages/service.html'), name='service'),
    path('team/',        TemplateView.as_view(template_name='pages/team.html'), name='team'),
    path('testimonial/', TemplateView.as_view(template_name='pages/testimonial.html'), name='testimonial'),
]