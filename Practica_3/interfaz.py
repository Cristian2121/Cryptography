from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror

from Crypto.Cipher import DES
from Crypto.Util.Padding import pad

from modo import ModoDeOperacion

class Aplicacion():
    def __init__(self, gui):
        raiz = gui
        raiz.title('Práctica 3')
        raiz.resizable(False, False)

        #-------------------------- VARIABLES GLOBALES ---------------------------#
        self.modo = IntVar()
        self.nombre_imagen = ''
        
        #-------------------------- MODOS DE OPERACIÓN ---------------------------#
        frame_superior = ttk.Frame(raiz)
        frame_superior.pack()

        l_modo_op = ttk.Label(frame_superior, text='Seleccione el Modo de operación', justify='center')
        l_modo_op.pack()

        ttk.Radiobutton(frame_superior, text='ECB', variable=self.modo, value=1, command=lambda: self.cifrar).pack()
        ttk.Radiobutton(frame_superior, text='CBC', variable=self.modo, value=2, command=lambda: self.cifrar).pack()
        ttk.Radiobutton(frame_superior, text='CFB', variable=self.modo, value=3, command=lambda: self.cifrar).pack()
        ttk.Radiobutton(frame_superior, text='OFB', variable=self.modo, value=4, command=lambda: self.cifrar).pack()

        for child in frame_superior.winfo_children():
            child.pack_configure(padx=5, pady=5)

        #-------------------------- IV y LLAVE ---------------------------#
        frame_inferior = ttk.Frame(raiz)
        frame_inferior.pack()

        l_llave = ttk.Label(frame_inferior, text='Llave: ', justify='left')
        l_llave.grid(row=0, column=0)
        l_iv = ttk.Label(frame_inferior, text='IV: ', justify='left')
        l_iv.grid(row=1, column=0)

        self.e_llave = ttk.Entry(frame_inferior, justify='center')
        self.e_llave.grid(row=0, column=1)
        self.e_iv = ttk.Entry(frame_inferior, justify='center')
        self.e_iv.grid(row=1, column=1)

        #-------------------------- BOTONES ---------------------------#
        btn_cifrar = ttk.Button(frame_inferior, text='Cifrar', command=self.img_a_cifrar)
        btn_cifrar.grid(row=2, column=0)

        btn_descifrar = ttk.Button(frame_inferior, text='Descifrar', command=self.img_a_descifrar)
        btn_descifrar.grid(row=2, column=1)

        for child in frame_inferior.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def img_a_cifrar(self):
        dir_imagen = askopenfilename(
            title='Imagen a cifrar',
            filetypes=(('Archivo BMP', '*.bmp'), )
        )

        img = open(dir_imagen, 'rb')

        # Para obtener sólo el nombre del archivo
        ultima_coincidencia = img.name.rfind('/')
        self.nombre_imagen = img.name[ultima_coincidencia + 1:-4]

        datos_img = img.read()
        img.close()

        self.cifrar(datos_img)

    def cifrar(self, datos_img):
        modo_op_elegido = self.modo.get()
        llave = bytes(self.e_llave.get(), 'utf-8')
        iv = bytes(self.e_iv.get(), 'utf-8')

        # Para saber la longitud en bytes de los parmetros
        len_llave = len(llave)
        len_iv = len(iv)

        if modo_op_elegido == 1:
            modo_elegido = DES.MODE_ECB
        elif modo_op_elegido == 2:
            modo_elegido = DES.MODE_CBC
        elif modo_op_elegido == 3:
            modo_elegido = DES.MODE_CFB
        else:
            modo_elegido = DES.MODE_OFB

        if modo_elegido == DES.MODE_ECB:
            iv_ajustado = iv

            if len_llave == 8:
                llave_ajustada = llave
            elif len_llave < 8:
                llave_ajustada = pad(llave, DES.block_size)
            elif len_llave > 8: 
                llave_ajustada = llave

                showerror('Llave', 'La longitud de la llave debe ser de máximo 16 caracteres.') 
        else:
            if len_llave == 8:
                llave_ajustada = llave
            elif len_llave < 8:
                llave_ajustada = pad(llave, DES.block_size)
            elif len_llave > 8: 
                llave_ajustada = llave

                showerror('Llave', 'La longitud de la llave debe ser de máximo 8 caracteres.') 

            if len_iv == 8:
                iv_ajustado = iv
            elif len_iv < 8:
                iv_ajustado = pad(iv, DES.block_size)
            elif len_iv > 8: 
                iv_ajustado = iv

                showerror('IV', 'La longitud del IV debe ser de máximo 8 caracteres.') 

        """llave_ajustada = pad(llave, DES.block_size)
        iv_ajustado = pad(iv, DES.block_size)"""

        encabezado_img = datos_img[:64]
        bytes_imagen = datos_img[64:-2]
        pie_img = datos_img[-2:]

        objeto = ModoDeOperacion(modo_elegido, llave_ajustada, iv_ajustado, bytes_imagen)
        bytes_img_cifrada = objeto.cifrar_datos()

        if bytes_img_cifrada == bytes_imagen:
            print('No se cifro debido a un error en la longitud de la llave o el iv.')
        else:
            self.escribir_img(encabezado_img, bytes_img_cifrada, pie_img, 1, modo_elegido)

    def img_a_descifrar(self):
        dir_imagen = askopenfilename(
            title='Imagen a descifrar',
            filetypes=(('Archivo BMP', '*.bmp'), )
        )

        img = open(dir_imagen, 'rb')
        
        ultima_coincidencia = img.name.rfind('/')
        self.nombre_imagen = img.name[ultima_coincidencia + 1:-4]

        datos_img = img.read()
        img.close()

        self.descifrar(datos_img)

    def descifrar(self, datos_img):
        modo_op_elegido = self.modo.get()
        llave = bytes(self.e_llave.get(), 'utf-8')
        iv = bytes(self.e_iv.get(), 'utf-8')

        len_llave = len(llave)
        len_iv = len(iv)

        if modo_op_elegido == 1:
            modo_elegido = DES.MODE_ECB
        elif modo_op_elegido == 2:
            modo_elegido = DES.MODE_CBC
        elif modo_op_elegido == 3:
            modo_elegido = DES.MODE_CFB
        else:
            modo_elegido = DES.MODE_OFB

        if modo_elegido == DES.MODE_ECB:
            iv_ajustado = iv

            if len_llave == 8:
                llave_ajustada = llave
            elif len_llave < 8:
                llave_ajustada = pad(llave, DES.block_size)
            elif len_llave > 8: 
                llave_ajustada = llave

                showerror('Llave', 'La longitud de la llave debe ser de máximo 16 caracteres.') 
        else:
            if len_llave == 8:
                llave_ajustada = llave
            elif len_llave < 8:
                llave_ajustada = pad(llave, DES.block_size)
            elif len_llave > 8: 
                llave_ajustada = llave

                showerror('Llave', 'La longitud de la llave debe ser de máximo 8 caracteres.') 

            if len_iv == 8:
                iv_ajustado = iv
            elif len_iv < 8:
                iv_ajustado = pad(iv, DES.block_size)
            elif len_iv > 8: 
                iv_ajustado = iv

                showerror('IV', 'La longitud del IV debe ser de máximo 8 caracteres.') 

        """llave_ajustada = pad(llave, DES.block_size)
        iv_ajustado = pad(iv, DES.block_size)"""

        encabezado_img = datos_img[:64]
        bytes_imagen = datos_img[64:-2]
        pie_img = datos_img[-2:]

        objeto = ModoDeOperacion(modo_elegido, llave_ajustada, iv_ajustado, bytes_imagen)
        bytes_img_cifrada = objeto.descifrar_datos()

        if bytes_img_cifrada == bytes_imagen:
            print('No se descifró debido a un error de la llave o el IV.')
        else:
            self.escribir_img(encabezado_img, bytes_img_cifrada, pie_img, 2, modo_elegido)

    def escribir_img(self, encabezado, bytes_img, pie, operacion, modo):
        img_salida = encabezado + bytes_img + pie

        if modo == DES.MODE_CBC:
            if operacion == 1:
                nombre_img_salida = self.nombre_imagen + '_eCBC.bmp'
            elif operacion == 2:
                nombre_img_salida = self.nombre_imagen + '_dCBC.bmp'
        elif modo == DES.MODE_CFB:
            if operacion == 1:
                nombre_img_salida = self.nombre_imagen + '_eCFB.bmp'
            elif operacion == 2:
                nombre_img_salida = self.nombre_imagen + '_dCFB.bmp'
        elif modo == DES.MODE_ECB:
            if operacion == 1:
                nombre_img_salida = self.nombre_imagen + '_eECB.bmp'
            elif operacion == 2:
                nombre_img_salida = self.nombre_imagen + '_dECB.bmp'
        elif modo == DES.MODE_OFB:
            if operacion == 1:
                nombre_img_salida = self.nombre_imagen + '_eOFB.bmp'
            elif operacion == 2:
                nombre_img_salida = self.nombre_imagen + '_dOFB.bmp'

        with open(nombre_img_salida, 'wb') as imagen:
            imagen.write(img_salida)

            imagen.close()

#-------------------------- MAIN ---------------------------#
gui = Tk()
print(DES.block_size)
Aplicacion(gui)
gui.mainloop()