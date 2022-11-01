from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo, showerror

from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes

class Aplicacion():
    def __init__(self, raiz):
        plt_raiz = raiz
        plt_raiz.title('Práctica 1')

        # Variable que servirá para recuperarse en los métodos de la clase
        self.ruta_archivo = StringVar()

        # Contenedor del objeto Label
        frm_superior = ttk.Frame(plt_raiz)
        frm_superior.pack()

        ttk.Label(
            frm_superior,
            text="Para cifrar el contenido de un archivo seleccione un documento con extensión txt.\n" \
            "Si desea descifrar el contenido de un archivo debe elegir el documento con extensión " \
            "txt,\ny luego seleccionar el archivo donde se encuentra la llave para descifrarlo.\n" \
            "Nota. Los archivos de cifrado, llave y descifrado se guardan en la ruta del archivo " \
            "original\nseleccionado."
        ).pack(padx=5, pady=5)

        # Contenedor de los botones
        frm_inferior = ttk.Frame(plt_raiz)
        frm_inferior.pack()

        btn_cifrar = ttk.Button(frm_inferior, text='Cifrar', command=self.cifrar)
        btn_cifrar.grid(row=0, column=0)
        btn_descifrar = ttk.Button(frm_inferior, text='Descifrar', command=self.descifrar)
        btn_descifrar.grid(row=0, column=1)

        # Dar padding a los elementos que pertenecen a frm_inferior
        for hijo in frm_inferior.winfo_children():
            hijo.grid_configure(padx=5, pady=5)

    def cifrar(self):
        # Lectura del archivo a cifrar
        dir_archivo = askopenfilename(
            title='Archivo a cifrar',
            filetypes=(('Archivo de texto', '*.txt'), )
        )

        archivo = open(dir_archivo, 'r')
        nombre_archivo = archivo.name.split('.')[0]
        contenido = archivo.read()
        archivo.close()

        # Cifrado del contenido
        llave = get_random_bytes(8)
        cifrador = DES.new(llave, DES.MODE_OFB)
        contenido_cifrado = cifrador.encrypt(contenido.encode('utf-8'))

        # Escritura del archivo con la llave y el iv
        archivo_llave = open(nombre_archivo + '_llave.txt', 'wb')
        archivo_llave.write(llave + b"\n" + cifrador.iv)
        archivo_llave.close()

        # Escritura del archivo con contenido cifrado
        archivo_cifrado = open(nombre_archivo + '_C.txt', 'wb')
        archivo_cifrado.write(contenido_cifrado)
        archivo_cifrado.close()

        showinfo(
            'Archivo cifrado',
            'Se ha cifrado el contenido del archivo y se ha almacenado en la ruta ' + nombre_archivo + '_C.txt'
        )

    def descifrar(self):
        # Lectura del archivo a cifrar
        dir_archivo = askopenfilename(
            title='Archivo a descifrar',
            filetypes=(('Archivo de texto', '*.txt'), )
        )

        # Lectura del contenido cifrado
        archivo = open(dir_archivo, 'rb')
        nombre_archivo = archivo.name.split('.')[0]
        contenido = archivo.read()
        archivo.close()

        # Lectura de la llave
        dir_archivo_llave = askopenfilename(
            title='Llave para descifrar',
            filetypes=(('Archivo de texto', '*.txt'), )
        )

        archivo_llave = open(dir_archivo_llave, 'rb')
        # Separamos la cadena de bytes de la llave y el vector de inicialización
        llave, iv = archivo_llave.read().split(b"\n")
        archivo_llave.close()

        try:
            # Descifrado del contenido
            cifrador = DES.new(llave, DES.MODE_OFB, iv=iv)
            contenido_descifrado = cifrador.decrypt(contenido)

            # Escritura del archivo con contenido cifrado
            archivo_descifrado = open(nombre_archivo + '_D.txt', 'w')
            archivo_descifrado.write(contenido_descifrado.decode('utf-8'))
            archivo_descifrado.close()

            showinfo(
                'Archivo descifrado',
                'Se ha descifrado el contenido del archivo y se ha almacenado en la ruta ' + nombre_archivo + '_D.txt'
            )
        except:
            showerror('Error', 'No se pudo descifrar el archivo elegido.')

#------------------------------MAIN------------------------------#
# Iniciamos el objeto interfaz y lo ciclamos de manera infinita
raiz = Tk()
# Llamamos a la clase Aplicacion
Aplicacion(raiz)
raiz.mainloop()