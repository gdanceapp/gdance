from django.contrib.auth.decorators import user_passes_test, login_required
from django.conf.urls import patterns, url, include
from django.contrib.auth import views as auth_views
from gdance.utils import *
from .views import *

login_forbidden = user_passes_test(lambda u: u.is_anonymous(), '/')

user_detail_patterns = [
	url(r'^eliminar/$', login_required(group_required('entrenador')(DeleteUserView.as_view())), name='delete-user'),
	url(r'^detalle/$', UserDetailView.as_view(), name='detail-user'),
	url(r'^agregar-modalidad/$', login_required(group_required('entrenador')(AddModalidadUserView.as_view())), name='add-modalidad-user'),
]

user_type_detail_patterns = [
	url(r'^$', login_required(group_required('entrenador')(ListUserView.as_view())), name = 'list-user'),
	url(r'^crear/$', login_required(group_required('entrenador')(NewUserView.as_view())), name='new-user'),
	url(r'^(?P<pk>\d+)/', include(user_detail_patterns)),
]

user_pk_url_patterns = [
	url(r'^editar-nombre-usuario/$', login_required(EditNameUserView.as_view()), name='edit-name-user'),
	url(r'^editar-perfil-usuario/$', login_required(EditProfileUserView.as_view()), name='edit-profile-user'),
	url(r'^eliminar-horario/$', UserDetailScheduleView, name='delete-horario-user'),
	url(r'^(?P<user>[-\w]+)/eliminar-modalidad-usuario/$', login_required(group_required('entrenador')(DeleteModalidadPersonaView.as_view())), name='delete-modalidad-user'),
]

urlpatterns = patterns('gdance.apps.users.views',
	url(r'^ingresar/$', login_forbidden(auth_views.login), {'template_name': 'users/form_login.html', 'extra_context': {'title': 'Ingresar'}}, name = 'login'),
	url(r'^salir/$', auth_views.logout, {'next_page': '/'}, name = 'logout'),
	url(r'^perfil/$', login_required(UserProfileView.as_view()), name = 'profile'),
	url(r'^change-password/$', 'change_password', name = 'edit-password'),
	url(r'^(?P<tipo>[-\w]+)/', include(user_type_detail_patterns)),
	url(r'^(?P<user>\d+)/horario/$', login_required(group_required('entrenador')(ScheduleAddView.as_view())), name = 'add-horario'),
	url(r'^(?P<pk>[-\w]+)/', include(user_pk_url_patterns)),
)