# -*- encoding: utf-8 -*-
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import FormMixin
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic import *
from django.db.models import Q
from .models import *
from .forms import *

TYPE_USER = (
	('entrenador', 'Entrenadores'),
	('deportista', 'Deportistas'),
	('none', 'Administradores'),
)

template_dir = 'users/'

class NewUserView(SuccessMessageMixin, FormView):
	template_name = template_dir+'form_signup.html'
	success_message = 'Usuario registrador con éxito'
	form_class = NewUserForm

	def get_context_data(self, **kwargs):
		context = super(NewUserView, self).get_context_data(**kwargs)
		context['title'] = 'Nuevo '+self.kwargs['tipo']
		context['tipo'] = self.kwargs['tipo']
		return context

	def form_valid(self, form):
		form.new_user(self.kwargs['tipo'])
		return super(NewUserView, self).form_valid(form)

	def get_success_url(self):
		return reverse('list-user', kwargs = {'tipo': self.kwargs['tipo']})

class ListUserView(FormMixin, ListView):
	model = User
	paginate_by = 10
	form_class = UserSearchForm
	template_name = template_dir+'list_user.html'

	def get_context_data(self, **kwargs):
		context = super(ListUserView, self).get_context_data(**kwargs)
		context['title'] = 'Lista de '+dict(TYPE_USER)[self.kwargs['tipo']]
		context['type_user'] = dict(TYPE_USER)[self.kwargs['tipo']]
		context['tipo'] = self.kwargs['tipo']
		return context

	def get_form_kwargs(self):
		kwargs = super(ListUserView, self).get_form_kwargs()
		kwargs['buscar_por'] = self.request.GET.get('buscar_por')
		return kwargs

	def get_queryset(self):
		queryset = super(ListUserView, self).get_queryset()
		if self.request.GET.get('buscar_por') is not None:
			find_by = self.request.GET.get('buscar_por')
			queryset = queryset.filter(Q(first_name__icontains = find_by) | Q(last_name__icontains = find_by) | Q(profileuser__numero_documento__icontains = find_by) | Q(profileuser__numero_telefono__icontains = find_by) | Q(profileuser__direccion_residencia__icontains = find_by) | Q(profileuser__descripcion_persona__icontains = find_by))
		if self.kwargs['tipo'] != 'none':
			queryset = queryset.filter(groups__name = self.kwargs['tipo'])
		return queryset

class DeleteUserView(DeleteView):
	model = User
	template_name = 'elements/form_delete.html'

	def get_context_data(self, **kwargs):
		context = super(DeleteUserView, self).get_context_data(**kwargs)
		context['title'] = 'Confirmación'
		context['url'] = reverse('delete-user', kwargs = {'pk': self.kwargs['pk'], 'tipo': self.kwargs['tipo']})
		return context

	def get_success_url(self):
		return reverse('list-user', kwargs = {'tipo': self.kwargs['tipo']})

class UserDetailView(DetailView):
	model = User
	template_name = template_dir+'detail_usuario.html'

	def get_context_data(self, **kwargs):
		context = super(UserDetailView, self).get_context_data(**kwargs)
		context['title'] = 'Detalle del usuario'
		return context

class ScheduleAddView(SuccessMessageMixin, CreateView):
	template_name = 'elements/form_general.html'
	success_message = 'Horario agregado correctamente'
	form_class = ScheduleForm

	def get_context_data(self, **kwargs):
		context = super(ScheduleAddView, self).get_context_data(**kwargs)
		context['title'] = 'Agregar horario'
		context['url'] = reverse('add-horario', kwargs = {'user': self.kwargs['user']})
		return context

	def form_valid(self, form):
		form.instance.entrenador = User.objects.get(pk = self.kwargs['user']).profileuser
		return super(ScheduleAddView, self).form_valid(form)

	def get_success_url(self):
		user = User.objects.get(pk = self.kwargs['user'])
		return reverse('detail-user', kwargs = {'tipo': user.groups.all()[0].name, 'pk': user.pk})