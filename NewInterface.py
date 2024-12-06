from Database import DatabaseMethods
from Criptografia import Criptadores
from Criptografia import FirmaDigital
from interface import Interface
import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog


LARGEFONT = ("Verdana", 35)
SMALLFONT = ("Verdana", 15)

database = DatabaseMethods()
UsuarioActual = ""

class tkinterApp(tk.Tk):

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        # creating a container
        self.geometry("800x500")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage, Page1, Page2 , Page3, Page4):
            frame = F(container, self)

            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# first window frame startpage

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        style = ttk.Style()

        # This will be adding style, and
        # naming that style variable as
        # W.Tbutton (TButton is used for ttk.Button).
        style.configure('W.TButton', font=
        ('calibri', 10, 'bold', 'underline'),
                        foreground='red')

        # label of frame Layout 2
        label = ttk.Label(self, text="Bien Benido a tu Sanitario", font=LARGEFONT)
        # putting the grid in its place by using
        # grid

        controller.update_idletasks()  # Ensure the window dimensions are updated
        label.update_idletasks()  # Ensure the label dimensions are updated


        windowswidth = parent.winfo_width()
        labelwidth = label.winfo_width()
        offset = (windowswidth - labelwidth) // 2
        label.place( x = offset, y = 10)

        button1 = ttk.Button(self, text="Registrarse",
                             command=lambda: controller.show_frame(Page1), padding= 10, width= 15
                             , style = "W.TButton" )

        # putting the button in its place by
        # using grid

        windowswidth = controller.winfo_width()
        buttonwidth = button1.winfo_width()
        offset = (windowswidth - buttonwidth) // 2
        button1.place( x = offset , y = 100)

        ## button to show frame 2 with text layout2
        button2 = ttk.Button(self, text="Inicio de Sesión",
                             command=lambda: controller.show_frame(Page2))

        # putting the button in its place by
        # using grid
        button2.place ( x = offset , y = 200)

        button3 = ttk.Button(self, text="Salir",
                             command=lambda: controller.destroy())

        # putting the button in its place by
        # using grid
        button3.place(x=offset, y=275)


# second window frame page1
class Page1(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Inicio de Sesión", font=LARGEFONT)
        label_usuario = ttk.Label( self, text = "Usuario", font =SMALLFONT)
        label_contaseña = ttk.Label(self, text="Contraseña", font=SMALLFONT)
        label_contraseña2 = ttk.Label(self, text="Repetir Contraseña", font=SMALLFONT)


        # button


        button2 = ttk.Button(self, text="Cancel",
                             command=lambda: controller.show_frame(StartPage))

        # Creación de entries
        entry_usuario = ttk.Entry(self)
        entry_contraseña = ttk.Entry(self, show= '*')
        entry_contraseña2 = ttk.Entry(self,show = '*')
        entry_usuario.grid( row = 1, column = 2,pady= 20)
        entry_contraseña.grid(row = 2, column = 2)
        entry_contraseña2.grid(row=3, column=2)



        #Boton de crear cuenta

        button1 = ttk.Button(self, text="StartPage",
                             command=lambda: checkcontraseña(entry_usuario.get()
                            , entry_contraseña.get(),entry_contraseña2.get()))

        # using grid
        label.grid(row=0, column=4, padx=10, pady=10)
        label_usuario.grid(row=1, column=1, padx=10, pady=10)
        label_contaseña.grid(row=2, column=1, padx=10, pady=10)
        label_contraseña2.grid(row=3, column=1,  padx=10, pady=10)
        button1.grid(row=5, column=2)
        button2.grid(row=6, column=2)

        #La función checkea que las contraseñas coincidan y crea la cuenta.
        def checkcontraseña(usuario, con1, con2):

            # Comprobando que no existe el usuario
            if database.username_existe(usuario, "DataBase/datos_principales.json") \
                    or database.username_existe(usuario, "DataBase/keys.json"):
                messagebox.showwarning(tittle=None, message ="Este usuario ya está registrado")
            if con1 != con2:
                messagebox.showwarning(title=None, message="Las contraseñas no coinciden")
            else:
                Interface.new_account(usuario, con1, con2)
                #pasamos a la pagina con la sesión iniciada
                controller.show_frame(Page2)





# third window Login
class Page2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Inicio de sesión", font=LARGEFONT)
        label_usuario = ttk.Label(self, text="Usuario", font=SMALLFONT)
        label_contaseña = ttk.Label(self, text="Contraseña", font=SMALLFONT)


        entry_usuario = ttk.Entry(self)
        entry_contraseña = ttk.Entry(self, show='*')

        button2 = ttk.Button(self, text="Cancel",
                             command=lambda: controller.show_frame(StartPage))
        button1 = ttk.Button(self, text="Inicio Sesión",
                             command=lambda: InicioDeSesion(entry_usuario.get(),
                                                             entry_contraseña.get()))

        label.grid(row=0, column=4, padx=10, pady=10)
        label_usuario.grid(row=1, column=1, padx=10, pady=10)
        label_contaseña.grid(row=2, column=1, padx=10, pady=10)
        entry_usuario.grid(row=1, column=2, pady=20)
        entry_contraseña.grid(row=2, column=2)
        button1.grid(row=5, column=2)
        button2.grid(row=6, column=2)

        def InicioDeSesion( usuario, contraseña) :
            if database.username_existe(usuario, "DataBase/datos_principales.json") == False \
                    or database.username_existe(usuario, "DataBase/keys.json") == False:
                messagebox.showwarning(tittle=None, message="Este usuario no está registrado")
            else:
                # Valor de salt para el usuario
                salt = database.get_salt(usuario)

                # Cifrando contraseña introducido
                new_hashed_password = Criptadores.hash_hmac_password(contraseña, bytes.fromhex(salt))
                # Recogiendo valor de contraseña en la base de datos
                old_hashed_password = database.get_main_password(usuario)

                # Comprobando que coinciden las contraseñas
                if new_hashed_password[0] == old_hashed_password:
                    database.write_json_datos_principales_key(usuario,
                                    Criptadores.generar_clave_derivada(contraseña))
                    #Mover a nueva pagina
                    global UsuarioActual
                    UsuarioActual = entry_usuario.get()
                    controller.show_frame(Page3)


                else:
                    messagebox.showwarning(tittle=None, message="Contraseña es incorrecta")

class Page3(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Bienvenido", font=LARGEFONT)
        label_data = ttk.Label(self, text ="", font =SMALLFONT )
        button_Añadir= ttk.Button(self, text="AÑADIR DATOS DE SEGURO A TU CUENTA", command=
                                  lambda: controller.show_frame(Page4))
        button_ver= ttk.Button(self, text="VER DATOS DEL SEGURO" , command= lambda : printdata())
        button_guardar = ttk.Button(self, text="GUARDAR ARCHIVO MEDICO",
                                    command=lambda: introducirarhivos())
        button_recuperar = ttk.Button(self, text="RECUPERAR ARCHIVOS MEDICOS" ,
                                      command =lambda : recuperarArchivos())

        button_borrar = ttk.Button(self, text="BORRAR CUENTA", command= lambda: borrarCuenta())
        button_firma = ttk.Button(self, text="FIRMA DIGITAL")
        button_salir = ttk.Button(self, text="SALIR",
                                  command= lambda : controller.show_frame(StartPage) + DatabaseMethods.borrar_key(UsuarioActual, "Database/datos_principales.json"))

        label.grid(row=0, column=2, padx=10, pady=10)
        button_Añadir.grid(row=1, column=1, padx=10, pady=10)
        button_ver.grid(row=3, column=1, padx=10, pady=10)
        button_guardar.grid(row=4,column=1, padx=10, pady= 10)
        button_recuperar.grid(row=5, column=1, pady=10)
        button_borrar.grid(row=6, column=1, pady=10)
        button_firma.grid(row=7, column=1, pady=10)
        button_salir.grid(row=8, column=1, pady=10)

        def printdata ():
            texto = Interface.print_data(UsuarioActual)
            if texto == -1:
                messagebox.showwarning(tittle=None, message="No hay datos para este usuario")
            else:
                label_data.config(text=texto)
                label_data.grid(row=7, column=2)

        def introducirarhivos():
            openedfile_names = filedialog.askopenfilenames()
            if not openedfile_names:
                return
            key = database.get_keyA(UsuarioActual)
            Criptadores.file_encription(bytes.fromhex(key), openedfile_names)

            filenames = []
            for file in openedfile_names:
                filenames.append(os.path.basename(file))
            print(filenames)
            DatabaseMethods.store_files(UsuarioActual,filenames)

        def recuperarArchivos():
             key = database.get_keyA(UsuarioActual)
             file_list = database.get_datos_secundarios_file(UsuarioActual)
             if len(file_list) > 0:
                 Criptadores.file_decriptor(file_list, bytes.fromhex(key))
                 print("\n ARCHIVOS RECUPERADOS")
             else:
                 print("\n NO TIENES ARCHIVOS GUARDADOS")


        def borrarCuenta():
            # Borrando en los tres base de datos
            database.borrar_datos_usuario(UsuarioActual, "DataBase/keys.json")
            database.borrar_datos_usuario(UsuarioActual, "DataBase/datos_principales.json")
            database.borrar_datos_usuario(UsuarioActual, "DataBase/datos_secundarios.json")

            print("\nCUENTA BORRADA!")


class Page4(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="Info del seguro", font=LARGEFONT)
        label_usuario = ttk.Label(self, text="NOMBRE DEL SEGURO", font=SMALLFONT)
        label_seguro = ttk.Label(self, text="NÚMERO DEL SEGURO", font=SMALLFONT)

        entry_usuario = ttk.Entry(self)
        entry_seguro = ttk.Entry(self)

        button2 = ttk.Button(self, text="CANCELAR",
                             command=lambda: controller.show_frame(Page3))
        button1 = ttk.Button(self, text="AÑADIR INFORMACIÓN",
                             command=lambda: Interface.add_data(UsuarioActual,
                                                entry_usuario.get(), entry_seguro.get())
                                        +  controller.show_frame(Page3))

        label.grid(row=0, column=4, padx=10, pady=10)
        label_usuario.grid(row=1, column=1, padx=10, pady=10)
        label_seguro.grid(row=2, column=1, padx=10, pady=10)
        entry_usuario.grid(row=1, column=2, pady=20)
        entry_seguro.grid(row=2, column=2)
        button1.grid(row=5, column=2)
        button2.grid(row=6, column=2)


# Driver Code

app = tkinterApp()
app.mainloop()
