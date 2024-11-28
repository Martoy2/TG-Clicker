from django.contrib import admin
from .models import TelegramUser, Pool, History
import logging
from django.http import HttpResponse
import io

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('export.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def export_as_log(modeladmin, request, queryset):
    log_output = io.StringIO()

    for obj in queryset:
        log_entry = ', '.join([f"{field.name}: {getattr(obj, field.name)}" for field in obj._meta.fields])
        log_output.write(f"{log_entry}\n")

    log_output.seek(0)
    response = HttpResponse(log_output.getvalue(), content_type='text/plain; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename=export.log'
    return response


export_as_log.short_description = "Скачать в виде лога"


class HistoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in History._meta.fields]
    list_filter = ['time_now', 'action', 'user_id']
    actions = [export_as_log]


admin.site.register(TelegramUser)
admin.site.register(Pool)
admin.site.register(History, HistoryAdmin)