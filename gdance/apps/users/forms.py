# -*- encoding: utf-8 -*-
from django.contrib.auth.models import User, Group
from gdance.apps.base.models import *
from django import forms
from .models import *

class NewUserForm(forms.Form):
	first_name = forms.CharField(label = 'Nombres', widget = forms.TextInput(attrs = {'class': 'form-control','required': True}))
	last_name = forms.CharField(label = 'Apellidos', widget = forms.TextInput(attrs = {'class': 'form-control','required': True}))
	tipo_documento = forms.ChoiceField(choices = TIPO_DOCUMENTO_CHOICES, label = 'Tipo de documento', widget = forms.Select(attrs = {'class': 'form-control', 'required': True}))
	numero_documento = forms.CharField(label = 'Número de identificación', widget = forms.TextInput(attrs = {'maxlength': 10, 'class': 'form-control','required': True}))
	direccion_residencia = forms.CharField(label = 'Dirección de residencia', widget = forms.TextInput(attrs = {'class': 'form-control','required': True}))
	estatura = forms.CharField(label = 'Estatura', widget = forms.TextInput(attrs = {'class': 'form-control','required': True}))
	peso = forms.CharField(label = 'Peso (kg)', widget = forms.TextInput(attrs = {'class': 'form-control','required': True}))
	email = forms.CharField(label = 'Correo electrónico', widget = forms.EmailInput(attrs = {'class': 'form-control'}))
	numero_telefono = forms.CharField(label = 'Número telefónico', widget = forms.TextInput(attrs = {'class': 'form-control', 'required': False}))
	descripcion_persona = forms.CharField(label = 'Descripción', widget = forms.TextInput(attrs = {'class': 'form-control', 'required': False}))
	foto = forms.FileField(required = False)

	def new_user(self, tipo):
		first_name = self.cleaned_data['first_name']
		last_name = self.cleaned_data['last_name']
		tipo_documento = self.cleaned_data['tipo_documento']
		numero_documento = self.cleaned_data['numero_documento']
		direccion_residencia = self.cleaned_data['direccion_residencia']
		email = self.cleaned_data['email']
		numero_telefono = self.cleaned_data['numero_telefono']
		descripcion_persona = self.cleaned_data['descripcion_persona']
		estatura = self.cleaned_data['estatura']
		peso = self.cleaned_data['peso']
		foto = self.cleaned_data['foto']
		user = User.objects.create_user(email, '', numero_documento)
		user.first_name = first_name
		user.last_name = last_name
		user.save()
		user.groups.add(Group.objects.get(name = tipo))
		profile_user = ProfileUser(
			user = user,
			foto = foto,
			numero_documento = numero_documento,
			tipo_documento = tipo_documento,
			numero_telefono = numero_telefono,
			direccion_residencia = direccion_residencia,
			descripcion_persona = descripcion_persona,
			estatura = estatura,
			peso = peso,
		)
		profile_user.save()

class UserSearchForm(forms.Form):
	buscar_por = forms.CharField(label = 'Buscar por:', widget = forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Digite palabra a buscar'}))

	def __init__(self, *args, **kwargs):
		buscar_por = kwargs.pop('buscar_por', None)
		super(UserSearchForm, self).__init__(*args, **kwargs)
		if buscar_por: self.fields['buscar_por'].initial = buscar_por

class ScheduleForm(forms.ModelForm):

	class Meta:
		model = Schedule
		fields = '__all__'
		exclude = ('entrenador', )
		widgets = {
			'hora_inicio': forms.TextInput(attrs = {'class': 'form-control time','required': True}),
			'hora_final': forms.TextInput(attrs = {'class': 'form-control time','required': True})
		}
		labels = {
			'dia_semana': 'Día de la semana',
			'hora_inicio': 'Hora de inicio',
			'hora_final': 'Hora final'
		}

	def __init__(self, *args, **kwargs):
		super(ScheduleForm, self).__init__(*args, **kwargs)
		self.fields['dia_semana'].widget.attrs.update({'required': True, 'class': 'form-control'})