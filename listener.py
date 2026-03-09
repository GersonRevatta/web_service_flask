import json
from app.db import get_connection

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
                print(f"id: {data.get('id')}, name: {data.get('name')}")
            except json.JSONDecodeError:
                print("No se pudo parsear el payload como JSON")

if __name__ == "__main__":
    listen_items()