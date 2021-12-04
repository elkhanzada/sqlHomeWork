from django.conf.urls import url
from . import views
from django.views.generic.list import ListView
from django.urls import include
from django.urls import path
from employee.models import Employee

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

info_dict = {
     'queryset': Employee.objects.all(),
}
employee_info = {'model' : Employee}

urlpatterns = [
     path('', views.index, name='index'),
     # url('',
     # (r'^employees/$', 'django.views.generic.list_detail.object_list',
     #      dict(info_dict, template_name='employees/employee_list.html')),
     # (r'^employees/create/$', 'django.views.generic.create_update.create_object', dict(employee_info,
     #      template_name='employees/employee_form.html', post_save_redirect='/employees/')),
     # (r'^employees/update/(?P<object_id>\d+)/$', 'django.views.generic.create_update.update_object',
     #      dict(employee_info, template_name='employees/employee_form.html', post_save_redirect='/employees/')),
     # (r'^employees/delete/(?P<object_id>\d+)/$', 'django.views.generic.create_update.delete_object',
     # dict(employee_info, template_name='employees/employee_confirm_delete.html',
     #      post_delete_redirect='/employees/')),

     # (r'^admin/', include(admin.site.urls)),

     # (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
     #      {'document_root': '/home/pythonhol/mysite/python_hol/static'}),
     # )

]