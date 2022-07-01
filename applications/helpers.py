# from .models import Alert


# def send_alerts_to_users(value):
#     print(value)
#     alert_objects = Alert.objects.filter(price__lt=value).exclude(status="Deleted").select_related('user')
#     for alert_object in alert_objects:
#         print("sending mail to {}".format(alert_object.user.username))
#         alert_object.status = "Triggered"
#         alert_object.save()