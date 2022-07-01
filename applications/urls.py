from django.urls import path
from .views import (
    sign_up_view,
    create_alert,
    get_all_alerts,
    delete_trigger
)

urlpatterns = [
    path('signup/', sign_up_view),
    path('create_alert/', create_alert),
    path('get_all_alerts/', get_all_alerts),
    path('delete_trigger/', delete_trigger)
]