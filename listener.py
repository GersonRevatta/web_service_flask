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
PG_CHANNEL = "alam_rend_channel"


senders = [
    ModbusSender(
        host=host,
        port=MODBUS_PORT,
        device_id=MODBUS_DEVICE_ID,
        start_address=MODBUS_START_ADDRESS
    )
    for host in MODBUS_HOSTS
]


def listen_alam_rend():
    conn = get_connection()
    conn.autocommit = True

    with conn.cursor() as cur:
        cur.execute(f"LISTEN {PG_CHANNEL};")
        print(f"Escuchando canal: {PG_CHANNEL}")

        for notify in conn.notifies():
            print("\n--- Notificación recibida ---")
            print("Canal:", notify.channel)
            print("Payload crudo:", notify.payload)

            try:
                if notify.payload is None:
                    print("[LISTENER] Payload nulo, se ignora")
                    continue

                value = Decimal(notify.payload).quantize(
                    Decimal("0.01"),
                    rounding=ROUND_HALF_UP
                )

                print(f"[SERVER] rendimiento_new exacto: {value}")

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
    listen_alam_rend()