import json
from decimal import Decimal, ROUND_HALF_UP
from app.db import get_connection
from app.modbus_client import ModbusSender


MODBUS_HOST = "192.168.1.125"
MODBUS_PORT = 502
MODBUS_DEVICE_ID = 2
MODBUS_START_ADDRESS = 4502


sender = ModbusSender(
    host=MODBUS_HOST,
    port=MODBUS_PORT,
    device_id=MODBUS_DEVICE_ID,
    start_address=MODBUS_START_ADDRESS
)


def listen_items():

    conn = get_connection()
    conn.autocommit = True

    with conn.cursor() as cur:

        cur.execute("LISTEN items_channel;")
        print("Escuchando canal: items_channel")

        for notify in conn.notifies():

            print("\n--- Notificación recibida ---")
            print("Canal:", notify.channel)
            print("Payload crudo:", notify.payload)

            try:

                data = json.loads(notify.payload)

                value = Decimal(str(data["value"])).quantize(
                    Decimal("0.01"),
                    rounding=ROUND_HALF_UP
                )

                print(f"[SERVER] id: {data.get('id')}")
                print(f"[SERVER] name: {data.get('name')}")
                print(f"[SERVER] value exacto: {value}")

                ok = sender.send_value(value)

                if ok:
                    print("[LISTENER] Envío Modbus exitoso")
                else:
                    print("[LISTENER] Falló el envío Modbus")

            except Exception as e:
                print(f"[LISTENER] Error: {e}")


if __name__ == "__main__":
    listen_items()