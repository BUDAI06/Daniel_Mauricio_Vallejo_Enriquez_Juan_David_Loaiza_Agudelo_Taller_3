import os
import pydicom
import pandas as pd
import numpy as np
from pydicom.errors import InvalidDicomError



class ProcesadorDICOM:
    """
    Clase para automatizar la lectura, extracción y análisis
    de metadatos de archivos DICOM, siguiendo los estándares de la 
    informática médica.
    """
    def __init__(self, dicom_dir):
        """
        Inicializa el procesador con la ruta del directorio DICOM.
        """
        self.dicom_dir = dicom_dir
        self.metadata_list = []
        self.dataframe = None

    def cargar_archivos_dicom(self):
        """
        Escanea el directorio e identifica/carga archivos DICOM válidos
        utilizando pydicom.dcmread().
        """
        archivos_cargados = []
        search_dir = os.path.normpath(self.dicom_dir) 
        
        print(f"Iniciando escaneo del directorio: {search_dir}...")
        
        for root, _, files in os.walk(search_dir):
            for file_name in files:
                full_path = os.path.join(root, file_name)
                
                try:
                    ds = pydicom.dcmread(full_path) 
                    
                    if 'PatientName' in ds: 
                         archivos_cargados.append(ds)
                    
                except InvalidDicomError:
                    pass
                
                except Exception as e:
                    print(f"Error inesperado al leer {file_name}: {e}")

        print(f"Carga completa. Se encontraron {len(archivos_cargados)} archivos DICOM válidos.")
        return archivos_cargados


    def extraer_metadatos(self, dataset):
        """
        Extrae la información solicitada investigando el tag correspondiente 
        en el estándar DICOM. Maneja tags ausentes.
        """
        
        tags_map = {
            'PatientID': 'Identificador del paciente',
            'PatientName': 'Nombre del paciente',
            'StudyInstanceUID': 'Identificador único del estudio',
            'StudyDescription': 'Descripción del estudio',
            'StudyDate': 'Fecha del estudio',
            'Modality': 'Modalidad de la imagen',
            'Rows': 'Número de filas de la imagen',
            'Columns': 'Número de columnas de la imagen',
        }
        
        metadata = {}
        for tag_keyword, description in tags_map.items():
            value = dataset.get(tag_keyword, 'N/A')
            
            final_value = str(value.value).strip() if value != 'N/A' and hasattr(value, 'value') else str(value).strip()
            if final_value == '':
                 final_value = 'N/A'

            metadata[description] = final_value
            
        return metadata

    def analizar_imagen(self, dataset):
        """
        Calcula el valor de intensidad promedio de los píxeles.
        """
        try:
            pixel_array = dataset.pixel_array
            intensidad_promedio = np.mean(pixel_array)
            return float(intensidad_promedio)
        except AttributeError:
            return 'N/A'
        except Exception:
            return 'Error de análisis'


    def procesar(self):
        """
        Ejecuta el flujo completo de procesamiento.
        """
        datasets = self.cargar_archivos_dicom()
        
        if not datasets:
            print("\n Proceso abortado. No se encontraron archivos DICOM válidos para procesar.")
            return

        for ds in datasets:
            metadata = self.extraer_metadatos(ds)
            intensidad_promedio = self.analizar_imagen(ds)
            metadata['Intensidad Promedio'] = intensidad_promedio 
            self.metadata_list.append(metadata)

        self.dataframe = pd.DataFrame(self.metadata_list)
        
        print("\n---  Estructura de Datos (Dataframe de Pandas) Creada con Éxito ---")
        
       
        print("A continuación se muestran todos los datos extraídos:")
        print(self.dataframe.to_string()) 
        
        print(f"\nTotal de entradas en el DataFrame: {len(self.dataframe)}")
        
        return self.dataframe



if __name__ == "__main__":
    

    while True:
        input_path = input("\n Por favor, ingrese la ruta COMPLETA de la carpeta con sus archivos DICOM: ")
        
        if not os.path.isdir(input_path):
            print(f" Error: La ruta '{input_path}' no es un directorio válido o no existe.")
            print("Inténtelo de nuevo. Asegúrese de que la ruta esté bien escrita.")
        else:
            DICOM_DIR_PATH = input_path
            break
            

    procesador = ProcesadorDICOM(dicom_dir=DICOM_DIR_PATH)
    df_resultados = procesador.procesar()
    
    if df_resultados is not None and not df_resultados.empty:
        
   
        
        OUTPUT_DIR = 'resultados_dicom'
        output_file_name = 'metadata_dicom_results.csv'
        
  
        try:
            os.makedirs(OUTPUT_DIR, exist_ok=True)
            print(f"\n Se ha asegurado la existencia de la carpeta: '{OUTPUT_DIR}'")
        except Exception as e:
            print(f" Error al crear la carpeta de salida: {e}")
            OUTPUT_DIR = '.' 
        
       
        output_path = os.path.join(OUTPUT_DIR, output_file_name)
        
        # 3. Guardar el resultado en el archivo CSV dentro de la carpeta
        df_resultados.to_csv(output_path, index=False)
        print(f"Datos guardados con éxito en el archivo: {output_path}")