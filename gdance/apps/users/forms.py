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

	def clean_email(self):
		email = self.cleaned_data.get('email').lower()
		if User.objects.filter(email = email).exists() or User.objects.filter(username = email).exists():
			raise forms.ValidationError('El email ya se ecuentra en uso.')
		return email

	def clean_numero_documento(self):
		numero_documento = self.cleaned_data.get('numero_documento').lower()
		if ProfileUser.objects.filter(numero_documento = numero_documento).exists():
			raise forms.ValidationError('El número de identificación ya se ecuentra en uso.')
		return numero_documento

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

class ModalidadPersonaForm(forms.ModelForm):

	class Meta:
		model = ModalidadPersona
		fields = '__all__'
		exclude = ('deportista', )
		widgets = {
			'fecha_ingreso': forms.TextInput(attrs = {'class': 'form-control date-only','required': True}),
		}

	def __init__(self, *args, **kwargs):
		super(ModalidadPersonaForm, self).__init__(*args, **kwargs)
		self.fields['modalidad'].widget.attrs.update({'required': True, 'class': 'form-control'})
		self.fields['nivel'].widget.attrs.update({'required': True, 'class': 'form-control'})
		self.fields['estado'].widget.attrs.update({'required': True, 'class': 'form-control'})

	def save(self):
		save_data = super(ModalidadPersonaForm, self).save(commit = False)
		data_before = ModalidadPersona.objects.filter(deportista = save_data.deportista).update(estado = 'I')
		save_data.save()
		return save_data

class UserNameForm(forms.ModelForm):

	class Meta:
		model = User
		fields = ('first_name', 'last_name')
		widgets = {
			'first_name': forms.TextInput(attrs = {'class': 'form-control','required': True}),
			'last_name': forms.TextInput(attrs = {'class': 'form-control','required': True}),
		}
		labels = {
			'first_name': 'Nombres',
			'last_name': 'Apellidos',
		}

class UserProfileForm(forms.ModelForm):

	class Meta:
		model = ProfileUser
		fields = '__all__'
		exclude = ('user', 'foto')
		widgets = {
			'numero_documento': forms.TextInput(attrs = {'class': 'form-control', 'required': True}),
			'numero_telefono': forms.TextInput(attrs = {'class': 'form-control', 'required': True}),
			'direccion_residencia': forms.TextInput(attrs = {'class': 'form-control', 'required': True}),
			'descripcion_persona': forms.TextInput(attrs = {'class': 'form-control', 'required': True}),
			'estatura': forms.TextInput(attrs = {'class': 'form-control', 'required': True}),
			'peso': forms.TextInput(attrs = {'class': 'form-control', 'required': True}),
		}

	def __init__(self, *args, **kwargs):
		super(UserProfileForm, self).__init__(*args, **kwargs)
		self.fields['tipo_documento'].widget.attrs.update({'required': True, 'class': 'form-control'})