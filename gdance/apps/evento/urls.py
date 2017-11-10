from django.contrib.auth.decorators import login_required
from django.conf.urls import patterns, url, include
from gdance.utils import *
from .views import *

evento_detail_patterns = [
	url(r'^actualizar/$', login_required(group_required('entrenador')(EventoUpdateView.as_view())), name='edit-evento'),
	url(r'^eliminar/$', login_required(group_required('entrenador')(EventoDeleteView.as_view())), name='delete-evento'),
]

urlpatterns = patterns('gdance.apps.evento.views',
	url(r'^$', EventoListView.as_view(), name = 'list-evento'),
	url(r'^agregar/$', login_required(group_required('entrenador')(EventoAddView.as_view())), name = 'add-evento'),
	url(r'^(?P<pk>\d+)/', include(evento_detail_patterns)),
)