from django.conf.urls import url

from . import views


app_name = 'example_labeller'
urlpatterns = [
    # Examples:
    # url(r'^$', 'labelling_aas.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.home, name='home'),
    url(r'^labelling_tool_api$', views.LabellingToolAPI.as_view(), name='labelling_tool_api'),
    url(r'^visualizer$', views.visualizer, name='visualizer'),
]
