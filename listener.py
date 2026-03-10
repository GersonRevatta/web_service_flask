import json
from app.db import get_connection
from app.modbus_client import ModbusSender

# PRUEBA LOCAL
MODBUS_HOST = "127.0.0.1"
MODBUS_PORT = 5020
MODBUS_DEVICE_ID = 1
MODBUS_START_ADDRESS = 0

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
                print("Item recibido:", data)
                print(f"id: {data.get('id')}, name: {data.get('name')}, value: {data.get('value')}")

                value = float(data["value"])

                ok = sender.send_value(value)

                if ok:
                    print("[LISTENER] Envío Modbus exitoso")
                else:
                    print("[LISTENER] Falló el envío Modbus")

            except json.JSONDecodeError:
                print("[LISTENER] No se pudo parsear el payload como JSON")
            except KeyError:
                print("[LISTENER] El payload no contiene la clave 'value'")
            except ValueError as e:
                print(f"[LISTENER] Valor inválido: {e}")
            except Exception as e:
                print(f"[LISTENER] Error general: {e}")


if __name__ == "__main__":
    listen_items()