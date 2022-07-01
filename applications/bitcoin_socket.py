import json
import threading
import websocket
from .models import Alert


def send_alerts_to_users(value):
    """
    Plan A --> Directly pull the matching alerts whose price same sa value. I have implemented indexing so it the query will be faster but we can choose partition then sharding to make this happens when data going to billions
    plan B --> Decouple this send data to any message broker or redis another service can pull the data and send notifications there we can use some other services whic can be etremely fast for searching
    """
    alert_objects = Alert.objects.filter(price=value).exclude(status="Deleted").select_related('user')
    for alert_object in alert_objects:
        print("sending mail to {}".format(alert_object.user.username))
        alert_object.status = "Triggered"
        alert_object.save()


def on_message(ws, message):
    data = json.loads(message)
    if data.get('k').get("x"):
        close_value = int(float(data.get('k').get("c")))
        send_alerts_to_users(close_value)


def on_close(ws, close_status_code, close_msg):
    print("Websocket connection closed")


def on_open(ws):
    print("webscocket connection created")

def start_bitcoin_websocket_connection():
    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://stream.binance.com:9443/ws/btcusdt@kline_1m", on_open=on_open, on_message=on_message, on_close=on_close)
    wst = threading.Thread(target=ws.run_forever)
    wst.daemon = True
    wst.start()
