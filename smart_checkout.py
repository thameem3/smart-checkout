import cv2
from ultralytics import YOLO
import datetime
import qrcode
import json
import time

# Predefined product-price mapping
prices = {
    "bottle": 20, "book": 50, "apple": 30, "banana": 10,
    "cell phone": 1000, "toothbrush": 15, "laptop": 50000,
    "cup": 25, "chair": 1200, "pizza": 80, "cake": 150,
    "donut": 40, "teddy bear": 300, "remote": 150,
    "keyboard": 1000, "mouse": 500, "orange": 20,
    "sandwich": 40, "clock": 200, "scissors": 30,
    "microwave": 4000, "oven": 3500, "sink": 2500
}

# Load YOLOv8n model
model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture(0)

product_counts = {}
total = 0
last_detection_time = {}
last_product_time = time.time()
TIMER_DURATION = 5  # seconds

# Receipt file with timestamp
receipt_file = f"receipt_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

# Start the receipt
with open(receipt_file, "w") as f:
    f.write("SMART CHECKOUT RECEIPT\n")
    f.write(f"Date: {datetime.datetime.now()}\n")
    f.write("-" * 30 + "\n")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)
    new_detection = False

    for result in results:
        for box in result.boxes:
            cls = int(box.cls[0])
            label = model.names[cls]

            if label in prices:
                current_time = time.time()
                cooldown = 2  # seconds between repeated detections

                if label not in last_detection_time or current_time - last_detection_time[label] > cooldown:
                    product_counts[label] = product_counts.get(label, 0) + 1
                    total += prices[label]
                    last_detection_time[label] = current_time
                    last_product_time = current_time
                    new_detection = True

                    with open(receipt_file, "a") as f:
                        f.write(f"{label.capitalize()} - Rs.{prices[label]}\n")

                    # Update checkout_data.json
                    item_list = []
                    for item, count in product_counts.items():
                        for _ in range(count):
                            item_list.append({"name": item, "price": prices[item]})
                    with open("checkout_data.json", "w") as f:
                        json.dump(item_list, f)

            # Draw bounding box and label
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Show total price on screen
    cv2.putText(frame, f"Total: ₹{total}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Smart Checkout", frame)

    # Timer logic: if no new product for 5 seconds, generate bill
    if not new_detection and time.time() - last_product_time > TIMER_DURATION:
        break

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Finalize receipt
with open(receipt_file, "a", encoding="utf-8") as f:
    f.write("-" * 30 + "\n")
    for item, count in product_counts.items():
        f.write(f"{item.capitalize()} x{count} = Rs.{prices[item] * count}\n")
    f.write("-" * 30 + f"\nTotal: ₹{total}\nThank you!\n")

# Generate UPI QR Code (replace merchant@upi with your UPI ID)
upi_link = f"upi://pay?pa=merchant@upi&pn=SmartStore&am={total}&cu=INR"
qr = qrcode.make(upi_link)
qr_filename = f"payment_qr_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
qr.save(qr_filename)

# Show QR code
qr_image = cv2.imread(qr_filename)
cv2.imshow("Scan to Pay", qr_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Append QR info to receipt
with open(receipt_file, "a", encoding="utf-8") as f:
    f.write(f"\nScan the QR to Pay: {qr_filename}\n")

# Cleanup
cap.release()
cv2.destroyAllWindows()


#new things are added in the file so check it and corret it
cap.release()

