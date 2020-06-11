from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.core.management import call_command
from django.urls import include, path

urlpatterns = [
                  path('', include('forum.urls')),
                  path('admin/', admin.site.urls)
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

call_command('calc_cache')  # TODO: возможно, в будущем эта команда будет вызываться не здесь
