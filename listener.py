import json
from decimal import Decimal, ROUND_HALF_UP
from app.db import get_connection
from app.modbus_client import ModbusSender


MODBUS_HOSTS = [
    "172.25.26.75",
    "172.25.26.76",
]

MODBUS_PORT = 502
MODBUS_DEVICE_ID = 1
MODBUS_START_ADDRESS = 13


senders = [
    ModbusSender(
        host=host,
        port=MODBUS_PORT,
        device_id=MODBUS_DEVICE_ID,
        start_address=MODBUS_START_ADDRESS
    )
    for host in MODBUS_HOSTS
]


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

                results = []

                for sender in senders:
                    print(f"\n[LISTENER] Enviando a {sender.host}:{sender.port}")
                    ok = sender.send_value(value)
                    results.append((sender.host, ok))

                print("\n[LISTENER] Resumen de envío:")
                for host, ok in results:
                    if ok:
                        print(f"  - {host}: OK")
                    else:
                        print(f"  - {host}: FALLÓ")

            except Exception as e:
                print(f"[LISTENER] Error: {e}")


if __name__ == "__main__":
    listen_items()