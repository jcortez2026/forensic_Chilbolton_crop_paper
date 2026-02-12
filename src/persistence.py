import h5py
import numpy as np
import datetime
import torch 

def exportar_fase_motor(model, coherencia, nombre_seccion="ADN_Azul"):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    path = f"output/firma_{nombre_seccion}_{timestamp}.h5"
    
    with h5py.File(path, "w") as f:
        # Metadatos del Paper de Juan Marcelo Diaz Cortez
        f.attrs['author'] = "Juan Marcelo Diaz Cortez"
        f.attrs['theory'] = "Phase-Torsion Propulsion via Photonic Heterostructures"
        f.attrs['coherencia_pico'] = coherencia
        
        # Parámetros de la simulación
        params = f.create_group("propulsion_metrics")
        params.create_dataset("f1_fundamental", data=model.f1.item())
        params.create_dataset("f2_armonica", data=model.f2.item())
        params.create_dataset("relacion_sintoniza", data=model.f2.item() / model.f1.item())
        params.create_dataset("mezcla_phi", data=torch.sigmoid(model.mezcla).item())
        
        # La huella dactilar (Tensor de interferencia)
        f.create_dataset("interferometria_map", data=model().detach().numpy())
        
    print(f"📦 HDF5 Generado: {path}")
    return path