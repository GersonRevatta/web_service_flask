import logging
import uuid
import time
from logging.handlers import RotatingFileHandler
from decimal import Decimal, ROUND_HALF_UP

from app.db import get_connection
from app.modbus_client import ModbusSender


# =========================
# CONFIGURACIÓN DE LOGS PRO
# =========================
log_handler = RotatingFileHandler(
    "listener.log",
    maxBytes=5 * 1024 * 1024,  # 5MB
    backupCount=5
)

log_formatter = logging.Formatter(
    "%(asctime)s.%(msecs)03d | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

log_handler.setFormatter(log_formatter)

logger = logging.getLogger("listener")
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)
logger.addHandler(logging.StreamHandler())  # consola opcional


# =========================
# CONFIG MODBUS / PG
# =========================
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


# =========================
# LISTENER
# =========================
def listen_alam_rend():
    conn = get_connection()
    conn.autocommit = True

    with conn.cursor() as cur:
        cur.execute(f"LISTEN {PG_CHANNEL};")
        logger.info(f"[INIT] Escuchando canal: {PG_CHANNEL}")

        for notify in conn.notifies():

            event_id = str(uuid.uuid4())[:8]  # identificador corto
            start_time = time.time()

            logger.info(f"[{event_id}] ===== NUEVO EVENTO =====")
            logger.info(f"[{event_id}] Canal: {notify.channel}")
            logger.info(f"[{event_id}] Payload crudo: {notify.payload}")

            try:
                if notify.payload is None:
                    logger.warning(f"[{event_id}] Payload nulo → ignorado")
                    continue

                # =========================
                # PROCESAMIENTO
                # =========================
                value = Decimal(notify.payload).quantize(
                    Decimal("0.01"),
                    rounding=ROUND_HALF_UP
                )

                logger.info(f"[{event_id}] Valor procesado: {value}")

                # =========================
                # ENVÍO A MODBUS
                # =========================
                results = []

                for sender in senders:
                    send_start = time.time()

                    logger.info(
                        f"[{event_id}] Enviando → {sender.host}:{sender.port}"
                    )

                    ok = sender.send_value(value)

                    duration = round((time.time() - send_start) * 1000, 2)

                    results.append((sender.host, ok, duration))

                    if ok:
                        logger.info(
                            f"[{event_id}] OK → {sender.host} ({duration} ms)"
                        )
                    else:
                        logger.error(
                            f"[{event_id}] FALLÓ → {sender.host} ({duration} ms)"
                        )

                # =========================
                # RESUMEN
                # =========================
                total_time = round((time.time() - start_time) * 1000, 2)

                logger.info(f"[{event_id}] ---- RESUMEN ----")
                for host, ok, duration in results:
                    status = "OK" if ok else "FAIL"
                    logger.info(
                        f"[{event_id}] {host} → {status} ({duration} ms)"
                    )

                logger.info(
                    f"[{event_id}] Tiempo total evento: {total_time} ms"
                )

            except Exception as e:
                logger.exception(f"[{event_id}] ERROR CRÍTICO: {e}")


if __name__ == "__main__":
    listen_alam_rend()