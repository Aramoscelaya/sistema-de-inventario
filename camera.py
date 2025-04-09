import cv2
import base64
import threading
import cv2
import time
import pygame
from scanner import scan_code
from database import create_product
import config

scanning = False
result_text = None
page = None
data_global_camera = None
action = None

pygame.mixer.init()
sound = pygame.mixer.Sound('beep.mp3')

def set_global_variable(value):
    config.global_variable_test = value

def get_global_variable():
    return config.global_variable_test

def get_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise Exception("No se puso abrir la camara.")
    return cap

def close_camera():
    cap = get_camera()
    # Liberar recursos
    cap.release()
    cv2.destroyAllWindows()
    print("❌ Camara cerrada")

def get_frame(cap):
    ret, frame = cap.read()
    if not ret:
        raise Exception("No se pudo leer el frame.")
    return frame

def encode_frame_to_base64(frame):
    _, buffer = cv2.imencode('.jpg', frame)
    return base64.b64encode(buffer).decode('utf-8')

def start_scan(p, rs, act, e):
    global scanning, page, result_text, action
    action = act
    page = p
    result_text = rs
    scanning = True
    threading.Thread(target=(scan_loop)).start()

def scan_loop():
    cap = get_camera()
    global scanning
    code_count = {}
    frames_checked = 0

    while scanning:
        frame = get_frame(cap)
        code = scan_code(frame)

        if code:
            if code in code_count:
                code_count[code] += 1
            else:
                code_count[code] = 1
            frames_checked += 1 

            height, width, _ = frame.shape
            cv2.rectangle(frame, (50, height - 60), 
                        (width - 50, height - 10), 
                        (0, 255, 0), -1)
            cv2.putText(frame, f"Detected: {code}", 
                        (60, height - 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, 
                        (255, 255, 255), 2)

            if frames_checked >= 10:
                for c, count in code_count.items():
                    if count >= 10:
                        #result_text.value = f"Resultado: {c}"
                        set_global_variable(c)
                        #getCode(c)
                        sound.play()
                        time.sleep(0.5)
                        break

                code_count.clear()
                frames_checked = 0

        page.image.src_base64 = encode_frame_to_base64(frame)
        page.update()

def getCode(code):
    codes = code[0]
    datos = codes.split(',')
    items = []

    #datos = ['id_producto-PF4HD0K', 'hostname-WPHI002']
    for i in datos:
        try:
            item = {}

            name = i.split('-')[0]
            item["name"] = name

            if name == 'hostname':
                item["value"] = i.split('-')[1].replace("/", "-")
            else:
                item["value"] = i.split('-')[1]

            items.append(item)
        except IndexError:
            items = "Codigo ilegible"
            print("Error: Intentaste acceder a una posición que no existe en la lista")
    
    result_text.value = f"Resultado: {items}"
    print(items)
    '''
    match action:
        case 'add_items':
            response = create_product(items)
            return response
        case 'assignment':
            response = create_product(items)
            return response
        case _:
            return "Otro número"
    '''