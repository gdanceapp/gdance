from django.contrib.auth.decorators import user_passes_test, login_required
from django.conf.urls import patterns, url, include
from django.contrib.auth import views as auth_views
from gdance.utils import *
from .views import *

login_forbidden = user_passes_test(lambda u: u.is_anonymous(), '/')

user_detail_patterns = [
	url(r'^eliminar/$', login_required(group_required(['entrenador'])(DeleteUserView.as_view())), name='delete-user'),
	url(r'^detalle/$', login_required(UserDetailView.as_view()), name='detail-user'),
]

user_type_detail_patterns = [
	url(r'^$', login_required(group_required(['entrenador'])(ListUserView.as_view())), name = 'list-user'),
	url(r'^crear/$', login_required(group_required(['entrenador'])(NewUserView.as_view())), name='new-user'),
	url(r'^(?P<pk>\d+)/', include(user_detail_patterns)),
]

urlpatterns = patterns('gdance.apps.users.views',
	url(r'^ingresar/$', login_forbidden(auth_views.login), {'template_name': 'users/form_login.html', 'extra_context': {'title': 'Ingresar'}}, name = 'login'),
	url(r'^salir/$', auth_views.logout, {'next_page': '/'}, name = 'logout'),
	url(r'^(?P<tipo>[-\w]+)/', include(user_type_detail_patterns)),
	url(r'^(?P<user>\d+)/horario/$', login_required(group_required(['entrenador'])(ScheduleAddView.as_view())), name = 'add-horario'),
)