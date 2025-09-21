from ultralytics import YOLO
import cv2

# Cargar modelo YOLOv8 preentrenado (puede usar modelos pequeños para GUI como yolov8n)
model = YOLO("yolov8n.pt")  # Puedes usar otro modelo entrenado si tienes uno específico para UI


# Cargar imagen
image_path = "screenshot.png"
image = cv2.imread(image_path)

# Detección
results = model(image)

# Mostrar resultados
for result in results:
    for box in result.boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        cls = int(box.cls[0])
        conf = float(box.conf[0])
        label = model.names[cls]

        print(f"{label}: ({int(x1)}, {int(y1)}) - ({int(x2)}, {int(y2)}), Confianza: {conf:.2f}")

        # Dibujar caja en la imagen
        cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        cv2.putText(image, label, (int(x1), int(y1)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

# Guardar o mostrar imagen
cv2.imshow("Detecciones", image)
cv2.waitKey(0)
cv2.destroyAllWindows()