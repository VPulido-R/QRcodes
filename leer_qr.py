import os
from datetime import datetime
import cv2
from pyzbar.pyzbar import decode
from picamera2 import Picamera2

# Carpeta donde se guardan las fotos
OUTPUT_DIR = "scans"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Inicializa la cámara
picam2 = Picamera2()
picam2.start()

print("📷 Escaneando QR... presiona Ctrl+C para salir.")

try:
    while True:
        # Captura frame
        frame = picam2.capture_array()

        # Detecta QR en el frame
        for qr in decode(frame):
            qr_data = qr.data.decode("utf-8")
            # Dibujar rectángulo en QR
            pts = qr.polygon
            if len(pts) == 4:
                pts = [(p.x, p.y) for p in pts]
                cv2.polylines(frame, [cv2.convexHull(cv2.UMat(np.array(pts), cv2.CV_32S))], True, (0,255,0), 2)

            # Guardar imagen con timestamp
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{OUTPUT_DIR}/scan_{ts}.jpg"
            cv2.imwrite(filename, frame)

            # Mostrar resultado
            print(f"✅ QR detectado: {qr_data} - Guardado en {filename}")

except KeyboardInterrupt:
    print("✋ Escaneo terminado.")

finally:
    picam2.close()
