# -*- encoding: utf-8 -*-
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic.edit import FormMixin
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib import messages
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

def UserDetailScheduleView(self, pk):
	schedule = Schedule.objects.get(id = pk)
	user = schedule.entrenador.user
	schedule.delete()
	return HttpResponseRedirect(reverse('detail-user', kwargs = {'tipo': user.groups.all()[0].name, 'pk': user.pk}))

class DeleteModalidadPersonaView(DeleteView):
	model = ModalidadPersona
	template_name = 'elements/form_delete.html'

	def get_context_data(self, **kwargs):
		context = super(DeleteModalidadPersonaView, self).get_context_data(**kwargs)
		context['title'] = 'Confirmación'
		context['url'] = reverse('delete-modalidad-user', kwargs = {'pk': self.kwargs['pk'], 'user': self.kwargs['user']})
		return context

	def get_success_url(self):
		user = User.objects.get(pk = self.kwargs['user'])
		return reverse('detail-user', kwargs = {'tipo': user.groups.all()[0].name, 'pk': user.pk})

class AddModalidadUserView(SuccessMessageMixin, CreateView):
	template_name = 'elements/form_general.html'
	success_message = 'Modalidad agregada exitosamente'
	form_class = ModalidadPersonaForm

	def get_context_data(self, **kwargs):
		context = super(AddModalidadUserView, self).get_context_data(**kwargs)
		context['title'] = 'Agregar modalidad a usuario'
		context['url'] = reverse('add-modalidad-user', kwargs = self.kwargs)
		return context

	def form_valid(self, form):
		form.instance.deportista = User.objects.get(pk = self.kwargs['pk']).profileuser
		return super(AddModalidadUserView, self).form_valid(form)

	def get_success_url(self):
		return reverse('detail-user', kwargs = self.kwargs)

class EditNameUserView(SuccessMessageMixin, UpdateView):
	model = User
	template_name = 'elements/form_general.html'
	success_message = 'Nombre actualizado correctamente'
	form_class = UserNameForm

	def get_context_data(self, **kwargs):
		context = super(EditNameUserView, self).get_context_data(**kwargs)
		context['title'] = 'Actualizar nombre'
		context['url'] = reverse('edit-name-user', kwargs = {'pk': self.kwargs['pk']})
		return context

	def get_success_url(self):
		user = User.objects.get(pk = self.kwargs['pk'])
		return reverse('detail-user', kwargs = {'tipo': user.groups.all()[0].name, 'pk': user.pk}) if self.request.user.groups.all()[0].name == 'entrenador' else reverse('profile')

class EditProfileUserView(SuccessMessageMixin, UpdateView):
	model = ProfileUser
	template_name = 'elements/form_general.html'
	success_message = 'Perfil actualizado correctamente'
	form_class = UserProfileForm

	def get_context_data(self, **kwargs):
		context = super(EditProfileUserView, self).get_context_data(**kwargs)
		context['title'] = 'Actualizar perfil'
		context['url'] = reverse('edit-profile-user', kwargs = {'pk': self.kwargs['pk']})
		return context

	def get_success_url(self):
		profile = ProfileUser.objects.get(pk = self.kwargs['pk'])
		return reverse('detail-user', kwargs = {'tipo': profile.user.groups.all()[0].name, 'pk': profile.user.pk}) if self.request.user.groups.all()[0].name == 'entrenador' else reverse('profile')

class UserProfileView(TemplateView):
	template_name = template_dir+'profile.html'

	def get_context_data(self, **kwargs):
		context = super(UserProfileView, self).get_context_data(**kwargs)
		context['title'] = 'Mi perfil'
		return context

def change_password(request):
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)
			messages.success(request, 'La contraseña ha sido actualizada')
			return redirect('profile')
		else:
			messages.error(request, 'Ha ocurrido un error.')
	else:
		form = PasswordChangeForm(request.user)
	return render(request, 'elements/form_general.html', {
		'form': form,
		'url': reverse('edit-password')
	})