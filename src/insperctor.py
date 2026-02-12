import h5py
import os 

def inspeccionar_firma2(file_path):
    with h5py.File(file_path, "r") as f:
        print(f"\n--- LECTURA DE FIRMA: {f.attrs.get('author')} ---")
        print(f"Teoría: {f.attrs.get('theory')}")
        print(f"Coherencia de Sintonización: {f.attrs.get('coherencia_pico'):.4%}")
        
        metrics = f['propulsion_metrics']
        f1 = metrics['f1_fundamental'][()]
        f2 = metrics['f2_armonica'][()]
        relacion = f2 / f1
        
        print(f"Frecuencia Base (Minkowski): {f1:.4f}")
        print(f"Frecuencia de Torsión (N-Slices): {f2:.4f}")
        print(f"Relación de Salto (f2/f1): {relacion:.4f}")
        
        # El número de Slices (N) según tu paper
        print(f"Slices Fotónicos Estimados: {int(abs(relacion))}")

def inspector_multifirma():
    archivos = [f for f in os.listdir('output') if f.endswith('.h5')]
    print(f"--- COMPARATIVA DE SINTONIZACIÓN (Autor: {archivos[0].split('_')[1] if archivos else 'Cortez'}) ---")
    
    for arc in sorted(archivos):
        path = os.path.join('output', arc)
        with h5py.File(path, "r") as f:
            f1 = f['propulsion_metrics/f1_fundamental'][()]
            f2 = f['propulsion_metrics/f2_armonica'][()]
            coh = f.attrs['coherencia_pico']
            rel = f2 / f1
            print(f"\nArchivo: {arc}")
            print(f" > Coherencia: {coh:.4%} | Relación f2/f1: {rel:.4f}")
            print(f" > Modo Operativo: {'Alta Torsión' if abs(rel) > 30 else 'Armónico de Control'}")

if __name__ == "__main__":
    inspector_multifirma()
# if __name__ == "__main__":
#     # Cambia esto al nombre de tu archivo más reciente
#     inspeccionar_firma("output/firma_ADN_Azul_Chilbolton_20260121_143100.h5")