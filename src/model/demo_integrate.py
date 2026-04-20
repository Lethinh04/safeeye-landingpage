import cv2
import time
import torch
import numpy as np
import sounddevice as sd
from ultralytics import YOLO
from transformers import VitsModel, AutoTokenizer
import threading

model_yolo = YOLO("yolov8n.pt")
target_classes = [0, 56, 60, 39, 67]
names = model_yolo.names

vi_map = {
    "person": "người",
    "chair": "ghế",
    "dining table": "bàn",
    "bottle": "bình nước",
    "cell phone": "điện thoại"
}

tts_model = VitsModel.from_pretrained("facebook/mms-tts-vie")
tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-vie")

def speak(text):
    def run():
        inputs = tokenizer(text, return_tensors="pt")
        with torch.no_grad():
            output = tts_model(**inputs).waveform
        audio = output.squeeze().cpu().numpy()
        sd.stop()
        sd.play(audio, samplerate=tts_model.config.sampling_rate)

    threading.Thread(target=run, daemon=True).start()

cap = cv2.VideoCapture(0)

last_speak_time = 0
interval = 5

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_small = cv2.resize(frame, (640, 480))

    results = model_yolo(frame_small, classes=target_classes, conf=0.3)

    detected_classes = set()  

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            class_name = names[cls]
            detected_classes.add(class_name)

    current_time = time.time()
    if current_time - last_speak_time > interval:

        if detected_classes:
            parts = [vi_map.get(cls, cls) for cls in detected_classes]
            sentence = "Cảnh báo! phía trước có " + ", ".join(parts)
        else:
            sentence = "Phía trước không có vật thể đáng chú ý"

        print("TTS:", sentence)
        speak(sentence)

        last_speak_time = current_time

    cv2.imshow("Detection + TTS", frame_small)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()