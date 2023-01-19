from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror

import firma_digital

class Aplicacion():
    def __init__(self, r) -> None:
        raiz = r
        raiz.title('Práctica. Firma digital')
        
        frm_superior = ttk.Frame(raiz)
        frm_superior.pack()
        frm_inferior = ttk.Frame(raiz)
        frm_inferior.pack()

        # ----------------FRAME SUPERIOR----------------
        l_instrucciones = ttk.Label(
            frm_superior,
            text="Firme un archivo, verifique si corresponde a alguién o genere llaves."
        )
        l_instrucciones.pack(padx=5, pady=5)

        l_nombre = ttk.Label(frm_superior, text="Nombre para el archivo de llave:")
        l_nombre.pack(padx=5, pady=5)
        self.e_nombre = ttk.Entry(frm_superior, width=10)
        self.e_nombre.pack(padx=5, pady=5)

        # ----------------FRAME INFERIOR----------------
        btn_firmar_a = ttk.Button(frm_inferior, text="Firmar archivo", command=self.firmar)
        btn_firmar_a.grid(row=0, column=0)
        btn_verificar_a = ttk.Button(frm_inferior, text="Verificar archivo", command=self.verificar)
        btn_verificar_a.grid(row=0, column=1)
        btn_generar_ll = ttk.Button(frm_inferior, text="Generar llaves", command=self.generar_ll)
        btn_generar_ll.grid(row=0, column=2)

        for hijo in frm_inferior.winfo_children():
            hijo.grid_configure(padx=5, pady=5)

    def firmar(self):
        try:
            firma_digital.firmar_archivo()
            showinfo('Firmar archivo', 'Se firmó correctamente el archivo.')
        except:
            showerror('Firmar archivo', 'Ocurrió un error al tratar de firmar el archivo.')

    def verificar(self):
        firma_digital.verificacion_firma()

    def generar_ll(self):
        propietario = self.e_nombre.get()

        if propietario == '':
            showerror('Nombre', 'Debe colocar un nombre que no sea la cadena vacía.')
        else:
            try:
                firma_digital.generar_llave(propietario)
                showinfo('Llaves', 'Se generó el par de llaves correctamente.')
            except:
                showerror('LLaves', 'Ocurrió un error al tratar de generar las llaves.')

if __name__ == "__main__":
    r = Tk()
    Aplicacion(r)
    r.mainloop()