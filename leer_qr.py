import cv2
from pyzbar.pyzbar import decode

# Abre la cámara (0 = cámara principal)
cap = cv2.VideoCapture(0)

print("📷 Escaneando QR... Presiona 'q' para salir.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Error al acceder a la cámara")
        break

    # Detectar códigos en el frame
    for codigo in decode(frame):
        data = codigo.data.decode('utf-8')   # Extraer contenido
        x, y, w, h = codigo.rect             # Coordenadas del QR

        # Dibujar rectángulo alrededor del QR
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

        # Mostrar texto decodificado
        cv2.putText(frame, data, (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

        print("✅ QR detectado:", data)

    # Mostrar cámara en ventana
    cv2.imshow("Lector QR", frame)

    # Salir con la tecla q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
