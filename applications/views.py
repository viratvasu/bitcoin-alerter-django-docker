import json
from django.contrib.auth.models import User
from django.conf import settings
import math
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from .models import Alert
from .redis_helper import set_data, get_data

# starting websocket connection
from applications.bitcoin_socket import start_bitcoin_websocket_connection
start_bitcoin_websocket_connection()


def send_data_to_cache(user_obj):
    print("cache miss")
    alert_objects = Alert.objects.filter(user=user_obj)
    alert_data = [alert_object.get_data() for alert_object in alert_objects]
    alert_data = json.dumps(alert_data)
    set_data(str(user_obj.id), alert_data)
    return alert_data


def paginate_results(data, page_no):
    page_size = settings.PAGE_SIZE
    length = len(data)
    max_page_size = math.ceil(length/page_size)
    if page_no > max_page_size or page_no <= 0:
        return False, []
    else:
        if page_no == 1:
            alert_objects = data[:page_size]
        else:
            alert_objects = data[(page_no-1)*page_size:page_no*page_size]
        return True, alert_objects


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def sign_up_view(request):
    data = request.data
    username = data.get("username")
    password = data.get("password")
    if username and password:
        u = User.objects.create_user(username, password=password)
        u.save()
        return Response({"message": "Account created succesfully"}, status=status.HTTP_201_CREATED)
    return Response({"message": "username or password is missing"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def create_alert(request):
    data = request.data
    price = data.get("price")
    if price:
        Alert.objects.create(user=request.user, price=price)
        send_data_to_cache(request.user)
        return Response({"message": "Alert created succesfully"}, status=status.HTTP_201_CREATED)
    return Response({"message": "Price required to set alert"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def delete_trigger(request):
    data = request.data
    alert_id = data.get("id")
    if alert_id:
        alerts = Alert.objects.filter(id=alert_id)
        if alerts:
            alerts[0].status = "Deleted"
            alerts[0].save()
            send_data_to_cache(request.user)
            return Response({"message": "Alert deleted succesfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Alert not found with given id"}, status=status.HTTP_204_NO_CONTENT)
    return Response({"message": "id should be present"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def get_all_alerts(request):
    page_number = request.GET.get("page", 1)
    data = request.data
    alert_status = data.get("status")
    data = get_data(str(request.user.id))  # Cace Hit case
    if not data:  # Cache Miss case
        data = send_data_to_cache(request.user)
    alert_objects = json.loads(data)
    if not alert_status:
        alert_objects = alert_objects
    elif alert_status in settings.ALLOWED_ALERT_STATUS:
        alert_objects = [alert_obejct for alert_obejct in alert_objects if alert_obejct.get("status") == alert_status]
    else:
        return Response({"message": "Status sould be either Created or Deleted or Triggered"}, status=status.HTTP_400_BAD_REQUEST)

    is_sucess, response_data = paginate_results(alert_objects, int(page_number))
    if is_sucess:
        return Response({"count": len(alert_objects), "data": response_data}, status=status.HTTP_200_OK)
    else:
        return Response({"count": len(alert_objects), "message": "page_no is not valid"}, status=status.HTTP_400_BAD_REQUEST)
