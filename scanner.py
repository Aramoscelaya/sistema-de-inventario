from pyzbar.pyzbar import decode
import cv2

def scan_code(frame):
    codes = decode(frame)
    if codes:
        barcode_text = codes[0].data.decode('utf-8')
        x, y, w, h = codes[0].rect
        cv2.rectangle(frame, (x, y), 
                      (x + w, y + h), 
                      (0, 255, 0), 3)
        cv2.putText(frame, barcode_text, 
                    (x, y), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, 
                    (0, 255, 0), 3)
        return barcode_text,
    return None
