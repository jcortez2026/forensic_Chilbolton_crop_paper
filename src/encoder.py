import cv2
import torch
import numpy as np

def encode_image_to_tensor(path, target_color='violet'):
    # Leer imagen con OpenCV
    img = cv2.imread(path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Si queremos enfocarnos en la sección violeta (la base del mensaje)
    # Definimos el rango del color violeta en RGB
    if target_color == 'violet':
        lower = np.array([100, 0, 100])
        upper = np.array([255, 100, 255])
        mask = cv2.inRange(img_rgb, lower, upper)
    else:
        # Por defecto, blanco y negro
        mask = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)

    # Convertir a tensor de flotantes (0.0 a 1.0)
    tensor = torch.from_numpy(mask).float() / 255.0
    
    # IMPORTANTE: Reescalamos a una potencia de 2 (ej. 128x128) 
    # para que la FFT y los tensores sean más eficientes
    tensor = tensor.unsqueeze(0).unsqueeze(0) # Añadir dimensiones (B, C, H, W)
    tensor = torch.nn.functional.interpolate(tensor, size=(128, 128), mode='nearest')
    
    return tensor.squeeze()