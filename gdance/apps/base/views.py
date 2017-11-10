# -*- encoding: utf-8 -*-
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic import *

template_dir = 'home/'

class InicioTemplateView(TemplateView):
	template_name = template_dir+'index.html'

	def get_context_data(self, **kwargs):
		context = super(InicioTemplateView, self).get_context_data(**kwargs)
		context['title'] = 'Bienvenido'
		return context

class NosotrosTemplateView(TemplateView):
	template_name = template_dir+'nosotros.html'

	def get_context_data(self, **kwargs):
		context = super(NosotrosTemplateView, self).get_context_data(**kwargs)
		context['title'] = 'Nosotros'
		return context

class HorariosTemplateView(TemplateView):
	template_name = template_dir+'horarios.html'

	def get_context_data(self, **kwargs):
		context = super(HorariosTemplateView, self).get_context_data(**kwargs)
		context['title'] = 'Horarios'
		context['entrenadores'] = User.objects.filter(groups__name = 'entrenador')
		return context