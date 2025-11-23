Daniel Mauricio Vallejo Enriquez
Juan David Loaiza Agudelo
1- Breve Descripción del Proyecto
Este proyecto es una aplicación desarrollada en Python que simula una parte crítica del flujo de trabajo en la Informática Médica. Su objetivo es automatizar la lectura, extracción y almacenamiento de metadatos de archivos DICOM (Digital Imaging and Communications in Medicine). Utilizando la librería pydicom, el código procesa un conjunto de estudios médicos , extrae información clave como el ID del paciente, la modalidad (CT, MR, etc.) y las dimensiones de la imagen. Finalmente, estructura esta información en un DataFrame de Pandas y realiza un análisis simple calculando la intensidad promedio de píxeles de cada imagen, demostrando una aplicación práctica en el manejo de datos clínicos.

2-Interoperabilidad en Salud: DICOM y HL7

DICOM y HL7 son estándares cruciales porque garantizan la interoperabilidad en los sistemas de salud. Sin estos estándares, los diferentes dispositivos (escáneres, laboratorios) y sistemas de información (PACS, EHR) no podrían "hablar" entre sí, lo que paralizaría la atención y la gestión de datos clínicos
--DICOM: define cómo deben estar estructuradas las imágenes para ser leídas universalmente.
--HL7: define la estructura de los mensajes de texto para el intercambio de información del flujo de trabajo (p. ej., "El paciente X fue dado de alta").


3-Relevancia Clínica o de Pre-procesamiento del Análisis de Intensidades
El análisis de la distribución de intensidades (como el valor promedio, la desviación estándar o el histograma) en una imagen médica tiene una gran relevancia:

Relevancia de Pre-procesamiento:

Normalización y Estandarización: Permite ajustar el brillo y el contraste entre imágenes tomadas por diferentes escáneres o en diferentes momentos. El valor promedio (calculado en este proyecto) es la base para esta normalización, asegurando que los algoritmos de segmentación y clasificación funcionen de manera consistente.

Segmentación por Umbral: Conocer la distribución ayuda a definir umbrales de intensidad para separar automáticamente diferentes tipos de tejido (por ejemplo, el hueso tiene intensidades mucho más altas que el tejido blando en una CT).

Relevancia Clínica:

Caracterización de Tejidos: En modalidades como la TC, la intensidad (Unidades Hounsfield) se correlaciona directamente con la densidad del tejido. Analizar la distribución o el promedio en una región específica puede ayudar a cuantificar patologías (ej., evaluar la densidad de un nódulo pulmonar o medir la mineralización ósea).




4-Dificultades y la Importancia de Python
Dificultades Encontradas

Manejo de Tags Faltantes (Anonimización): La principal dificultad fue gestionar los tags que no estaban presentes en todos los archivos DICOM. Esto sucede a menudo debido a procesos de anonimización o si el tag es opcional. Se requirió implementar el manejo de errores (try...except) o el uso de la función .get(tag, 'N/A') para evitar que el script se detuviera y, en su lugar, registrara 'N/A'.

Validación de Archivos: Distinguir entre un archivo válido y un archivo con extensión incorrecta o corrupto, lo cual se solucionó mediante la detección de pydicom.errors.InvalidDicomError durante la lectura.

Importancia de las Herramientas de Python
Las herramientas de Python son cruciales para el análisis de datos médicos debido a su eficiencia y ecosistema de librerías:

pydicom: Facilita la interacción con el complejo estándar DICOM. Sin esta librería, acceder y parsear la información de los tags sería una tarea manual y titánica.

Pandas: Permite una estructuración y organización de datos inigualable. Convierte los metadatos dispersos de múltiples estudios en un formato tabular (DataFrame) que es fácil de consultar, filtrar y analizar.

NumPy: Es esencial para el análisis numérico de la imagen. Permite acceder a los datos de píxel como matrices eficientes, haciendo que cálculos como el promedio de intensidad sean rápidos y sencillos.
