import tkinter as tk
from tkinter import ttk
import serial
import time

# Configuración de UART
ser = serial.Serial('COM3', 9600, timeout=1)

# Función para enviar comando "1," y recibir listado
def solicitar_lista():
    ser.write(b'1,')  # Enviar comando "1,"
    time.sleep(1)
    data = ser.readline().decode('utf-8')  # Leer respuesta
    if data:
        archivos = data.strip().split(';')  # Separar las palabras por ';'
        lista_desplegable['values'] = archivos  # Actualizar el desplegable
        lista_desplegable.current(0)  # Seleccionar el primer elemento

# Función para enviar el archivo seleccionado
def enviar_archivo():
    archivo_seleccionado = lista_desplegable.get()
    if archivo_seleccionado:
        comando = f'2{archivo_seleccionado},'.encode('utf-8')
        ser.write(comando)  # Enviar comando "2archivo,"
        time.sleep(1)
        recibir_datos()  # Leer los datos recibidos

# Función para recibir datos después de enviar el archivo
def recibir_datos():
    data = ''
    while True:
        parte = ser.readline().decode('utf-8')  # Leer porciones de datos
        if 'A' in parte:  # Si llega la letra "A" que indica el final
            data += parte.split('A')[0]  # Tomar solo el contenido antes de la "A"
            break
        data += parte  # Agregar a la cadena de datos
    
    # Mostrar los datos recibidos en la caja de texto
    if data:
        caja_texto.delete(1.0, tk.END)  # Limpiar la caja de texto
        caja_texto.insert(tk.END, data)  # Insertar los datos recibidos

# Interfaz Tkinter
ventana = tk.Tk()
ventana.title("Terminal UART con Tkinter")

# Botón para solicitar la lista
boton_lista = tk.Button(ventana, text="Lista", command=solicitar_lista)
boton_lista.pack(pady=10)

# Lista desplegable
lista_desplegable = ttk.Combobox(ventana, values=[])
lista_desplegable.pack(pady=10)

# Botón para enviar el archivo seleccionado
boton_enviar = tk.Button(ventana, text="Enviar", command=enviar_archivo)
boton_enviar.pack(pady=10)

# Caja de texto para mostrar la respuesta del STM32
caja_texto = tk.Text(ventana, height=40, width=130)
caja_texto.pack(pady=10)

# Iniciar la ventana Tkinter
ventana.mainloop()
