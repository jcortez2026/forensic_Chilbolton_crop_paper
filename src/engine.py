import torch
import torch.nn as nn

class PropulsorModel(nn.Module):
    def __init__(self, res=128):
        super().__init__()
        # Definimos dos frecuencias independientes para que el 'peinado' sea más profundo
        # La f1 suele ser la estructura macro, la f2 los detalles fractales
        self.f1 = nn.Parameter(torch.tensor([12.0]))
        self.f2 = nn.Parameter(torch.tensor([25.0])) 
        
        # Parámetro de mezcla (0.0 = solo f1, 1.0 = solo f2)
        # Esto permite al algoritmo decidir qué peso tiene cada armónico
        self.mezcla = nn.Parameter(torch.tensor([0.5]))
        
        # Parámetro de fase para que las ondas puedan "moverse" y encajar mejor
        self.fase = nn.Parameter(torch.tensor([0.0]))
        
        # El lienzo (coordenadas)
        t = torch.linspace(-1, 1, res)
        x, y = torch.meshgrid(t, t, indexing='ij')
        self.register_buffer('r', torch.sqrt(x**2 + y**2))

    def forward(self):
        # Generamos ambas ondas
        onda1 = torch.cos(self.f1 * self.r + self.fase)
        onda2 = torch.cos(self.f2 * self.r)
        
        # Combinación lineal de las señales
        # Aplicamos una normalización para que el valor se mantenga en rangos de sigmoid
        combinacion = (1.0 - torch.sigmoid(self.mezcla)) * onda1 + torch.sigmoid(self.mezcla) * onda2
        
        # Binarización suave: el 10 ayuda a que el gradiente sea más fuerte en los bordes
        return torch.sigmoid(combinacion * 10)