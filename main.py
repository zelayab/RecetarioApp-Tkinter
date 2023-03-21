import json
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import tkinter.messagebox as mb
import os
#para la fecha usamos datetime
import datetime

ruta = os.path.join(os.path.dirname(__file__), 'recetas.json')


class Recetario:
    def __init__(self, master):
        self.master = master
        self.master.title("Recetario")
        self.master.geometry("600x400")

        self.categorias = []
        self.recetas = []
        self.recetas_listbox = None
        # Creamos un Entry para el nombre de la receta en el método agregar_receta()
        self.nombre_entry = None
        #cargamos las recetas
        
        #creamos un menu con varias opciones
        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)
        #creamos un submenu para el menu
        self.submenu = tk.Menu(self.menu)
        #hacemos que el submenu no pueda clickar
        self.submenu.config(tearoff=0)
        #agregamos el submenu al menu
        self.menu.add_cascade(label="Archivo", menu=self.submenu)
        self.submenu.add_command(label="Acerca de", command=self.acerca_de)
        self.submenu.add_command(label="Salir", command=self.master.quit)

        #Creamos un labelFrame para mostrar las recetas
        self.recetas_frame = tk.LabelFrame(self.master, text="Recetas")
        self.recetas_frame.pack()

        #Creamos un Treeview para mostrar las recetas que sean solo 2 columnas
        self.recetas_tree = ttk.Treeview(self.recetas_frame, columns=("nombre", "categoria","fecha"), show="headings")
        #Creamos las columnas del Treeview
        self.recetas_tree.heading("nombre", text="Nombre de la Receta")
        self.recetas_tree.heading("categoria", text="Categoria")
        self.recetas_tree.heading("fecha", text="Fecha")
        #Ajustamos el ancho de las columnas
        self.recetas_tree.column("nombre", width=200)
        self.recetas_tree.column("categoria", width=200)
        self.recetas_tree.column("fecha", width=200)
        self.recetas_tree.pack()
        #le damos estilos a las filas
        self.recetas_tree.tag_configure("oddrow", background="white")
        self.recetas_tree.tag_configure("evenrow", background="lightblue")
        #Creamos un scrollbar para el Treeview
        self.recetas_scrollbar = tk.Scrollbar(self.recetas_frame, orient="vertical", command=self.recetas_tree.yview)
        self.recetas_scrollbar.pack(side="right", fill="y")
        self.recetas_tree.configure(yscrollcommand=self.recetas_scrollbar.set)
        self.cargar_recetas()
        

        #creamos un frame label para los botones
        self.botones_frame = tk.LabelFrame(self.master, text="Botones")
        self.botones_frame.pack()
        #creamos un boton para agregar recetas
        self.agregar_receta_button = tk.Button(self.botones_frame, text="Agregar Receta", command=self.abrir_agregar_receta)
        self.agregar_receta_button.pack(side="left")
        #creamos un boton para eliminar recetas
        self.eliminar_receta_button = tk.Button(self.botones_frame, text="Eliminar Receta", command=self.eliminar_receta)
        self.eliminar_receta_button.pack(side="left")
        #creamos un boton para editar recetas
        self.editar_receta_button = tk.Button(self.botones_frame, text="Editar Receta", command=self.editar_receta)
        self.editar_receta_button.pack(side="left")
        #creamos un boton para ver las recetas
        self.ver_receta_button = tk.Button(self.botones_frame, text="Ver Receta", command=self.ver_receta)
        self.ver_receta_button.pack(side="left")
        #creamos un boton para actualizar las recetas
        self.actualizar_receta_button = tk.Button(self.botones_frame, text="Actualizar Receta", command=self.actualizar_lista_recetas)
        self.actualizar_receta_button.pack(side="left")
        
        #le damos estilos a los botones
        self.agregar_receta_button.config(bg="green", fg="white")
        self.eliminar_receta_button.config(bg="red", fg="white")
        self.editar_receta_button.config(bg="blue", fg="white")
        self.ver_receta_button.config(bg="yellow", fg="black")
        self.actualizar_receta_button.config(bg="orange", fg="black")


    def acerca_de(self):
        messagebox.showinfo("Acerca de", "Recetario de recetas hecho por Bernardo Zelaya para upateco - Proyecto Final")


#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#                FUNCIONES PARA EL MENU ARCHIVO                   #
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    #Funcion para agregar recetas
    def abrir_agregar_receta(self):
        self.agregar_receta_window = tk.Toplevel(self.master)
        self.agregar_receta_window.title("Agregar Receta")
        self.agregar_receta_window.geometry("400x600")
        
        self.nombre_label = tk.Label(self.agregar_receta_window, text="Nombre:")
        self.nombre_label.pack()
        self.nombre_entry = tk.Entry(self.agregar_receta_window)
        self.nombre_entry.pack()

        self.categoria_label = tk.Label(self.agregar_receta_window, text="Categoria:")
        self.categoria_label.pack()
        self.categoria_entry = tk.Entry(self.agregar_receta_window)
        self.categoria_entry.pack()
        
        self.ingredientes_label = tk.Label(self.agregar_receta_window, text="Ingredientes(poner con cantidad y unidad de medida)")
        self.ingredientes_label.pack()
        self.ingredientes_text = tk.Text(self.agregar_receta_window, height=5, width=30)
        self.ingredientes_text.pack()
        
        self.instrucciones_label = tk.Label(self.agregar_receta_window, text="Instrucciones (separar en guiones - )")
        self.instrucciones_label.pack()
        self.instrucciones_text = tk.Text(self.agregar_receta_window, height=5, width=30)
        self.instrucciones_text.pack()
        
        #creamos un frame label para el tiempo de coccion y preparacion
        self.tiempo_frame = tk.LabelFrame(self.agregar_receta_window, text="Tiempo")
        self.tiempo_frame.pack()

        #creamos un label para el tiempo de coccion
        self.tiempo_coccion_label = tk.Label(self.tiempo_frame, text="Cocción (en minutos)")
        self.tiempo_coccion_label.pack()
        #creamos un entry para el tiempo de coccion
        self.tiempo_coccion_entry = tk.Entry(self.tiempo_frame)
        self.tiempo_coccion_entry.pack()
        #creamos un label para el tiempo de preparacion
        self.tiempo_preparacion_label = tk.Label(self.tiempo_frame, text="Preparación (en minutos)")
        self.tiempo_preparacion_label.pack()
        #creamos un entry para el tiempo de preparacion
        self.tiempo_preparacion_entry = tk.Entry(self.tiempo_frame)
        self.tiempo_preparacion_entry.pack()
        #el label de la fecha se tiene que poner automatico
        self.fecha_label = tk.Label(self.agregar_receta_window, text="Fecha: " + str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
        self.fecha_label.pack()
        


        #creamos un espacio entre los frames
        self.espacio_label = tk.Label(self.agregar_receta_window, text="")
        self.espacio_label.pack()

        #creamos un frame label para agrupar los botones
        self.botones_frame = tk.LabelFrame(self.agregar_receta_window, text="Botones")
        self.botones_frame.pack()

        #creamos un boton para guardar la receta
        self.guardar_button = tk.Button(self.agregar_receta_window, text="Guardar", command=self.guardar_receta)
        self.guardar_button.pack()

        #creamos un boton para cancelar la receta
        self.cancelar_button = tk.Button(self.agregar_receta_window, text="Cancelar", command=self.agregar_receta_window.destroy)
        self.cancelar_button.pack()

        #creamos un boton para ver las categorias existentes
        self.ver_categorias_button = tk.Button(self.agregar_receta_window, text="Ver Categorias", command=self.ver_categorias)
        self.ver_categorias_button.pack()

    # Función para ver las categorías existentes
    def ver_categorias(self):
        #cargamos el json
        with open(ruta, 'r') as file:
            recetas_dict = json.load(file)

        #creamos una lista para guardar las categorias
        categorias = []

        #para recorrer el diccionario
        for receta in recetas_dict:
            #sacamos la categoria de la receta
            categoria = receta['categoria']
            #si la categoria no esta en la lista de categorias
            if categoria not in categorias:
                #la agregamos a la lista
                categorias.append(categoria)

           

        #mostramos las categorias en un infobox con un mensaje que diga: las categorias existentes son:
        messagebox.showinfo("Categorias", "Las categorias existentes son: " + str(categorias))

    #Funcion para actualizar las recetas
    def actualizar_categorias(self):
        self.categorias_text.delete("1.0", tk.END)
        self.categorias_text.insert("1.0", "Categorias:\n")
        #sacamos la categoria de las recetas 
        for receta in self.recetas:
            print(receta[1])
            self.categorias_text.insert(tk.END, receta[1] + " ")

    #Funcion para cargar las recetas
    def ver_receta(self):
        #si no se ha seleccionado ninguna receta
        if not self.recetas_tree.selection():
            messagebox.showerror("Error", "No se ha seleccionado ninguna receta")
            return
        # obtenemos el nombre de la receta seleccionada
        seleccion = self.recetas_tree.selection()[0]
        #obtenemos el nombre de la receta
        nombre_receta = self.recetas_tree.item(seleccion)['values']
        #ahora vamos a obtener el nombre de la receta partiendo de nombre_receta con un slice
        nombre_receta = nombre_receta[0]
        #para convertir en str el nombre de la receta porque es un objeto de tipo tuple
        nombre_receta = str(nombre_receta)

        #ahora necesitamos leer el json para obtener los datos de la receta con utf-8
        with open(ruta, 'r', encoding='utf-8') as file:
            recetas = json.load(file)

            for receta in recetas:
                #si el nombre de la receta es igual al nombre de la receta seleccionada
                if receta['nombre'] == nombre_receta:
                    #obtenemos los datos de la receta
                    nombre = receta['nombre']
                    categoria = receta['categoria']
                    ingredientes = receta['ingredientes']
                    instrucciones = receta['instrucciones']
                    tiempo_coccion = receta['tiempo_coccion']
                    tiempo_preparacion = receta['tiempo_preparacion']
                    fecha_creacion = receta['fecha_creacion']


        #creamos un infobox con los datos de la receta con saltos de linea para poner debajo de cada dato
        messagebox.showinfo("Receta", "Nombre: " + nombre + " \n\nCategoria: " + categoria + " \n\nIngredientes: " + ingredientes + " \n\ninstrucciones ( separado con guiones ) " + instrucciones + " \n\nTiempo de coccion ( en minutos ) " + tiempo_coccion + " \n\nTiempo de preparacion ( en minutos ) " + tiempo_preparacion + "\n\nFecha de creacion: " + fecha_creacion)
    
    #Funcion para guardar la receta
    def guardar_receta(self):
        #obtenemos los datos de la receta
        nombre = self.nombre_entry.get()
        categoria = self.categoria_entry.get()
        ingredientes = self.ingredientes_text.get("1.0", "end-1c")
        instrucciones = self.instrucciones_text.get("1.0", "end-1c")
        tiempo_coccion = self.tiempo_coccion_entry.get()
        tiempo_preparacion = self.tiempo_preparacion_entry.get()
        fecha_creacion = str(datetime.datetime.now().strftime("%A %d. %B %Y"))
        print(fecha_creacion)

        # Creamos un diccionario con los datos de la receta
        nueva_receta = {
            "nombre": nombre,
            "categoria": categoria,
            "ingredientes": ingredientes,
            "instrucciones": instrucciones,
            "tiempo_coccion": tiempo_coccion,
            "tiempo_preparacion": tiempo_preparacion,
            "fecha_creacion": fecha_creacion
        }

        # Agregamos la receta al diccionario
        self.recetas.append(nueva_receta)

        #cargamos todas las recetas existentes desde el archivo json
        with open(ruta, 'r') as archivo:
            recetas_dict = json.load(archivo)

        #agregamos la nueva receta al diccionario
        recetas_dict.append(nueva_receta)

        #guardamos todas las recetas nuevamente en el archivo json con el utf-8
        with open(ruta, 'w', encoding='utf-8') as archivo:
            json.dump(recetas_dict, archivo, indent=4)

        #agregamos la receta al treeview colocandolo centrado en las row y column
        self.recetas_tree.insert("", tk.END, text="", values=(nombre, categoria, tiempo_coccion, tiempo_preparacion), iid=nombre, anchor=tk.CENTER)
        self.recetas_tree.column("#0", width=0, stretch=tk.NO)


        #limpiamos los campos
        self.nombre_entry.delete(0, "end")
        self.categoria_entry.delete(0, "end")
        self.ingredientes_text.delete("1.0", "end")
        self.instrucciones_text.delete("1.0", "end")
        self.tiempo_coccion_entry.delete(0, "end")
        self.tiempo_preparacion_entry.delete(0, "end")

        #mostramos un mensaje de que la receta se guardo correctamente
        messagebox.showinfo("Recetario", "Receta guardada correctamente.")
        #cerramos la ventana
        self.agregar_receta_window.destroy()

    #Funcion para eliminar las recetas
    def guardar_recetas(self, seleccion):
        # cargamos las recetas desde el archivo json
        with open(ruta, 'r') as archivo:
            recetas_dict = json.load(archivo)

        # eliminamos las recetas seleccionadas del diccionario
        for item in seleccion:
            receta = self.recetas_tree.item(item)['values']
            if receta[0] in recetas_dict:
                del recetas_dict[receta[0]]

        # agregamos las recetas no eliminadas al diccionario
        for receta in self.recetas:
            if receta['nombre'] not in recetas_dict:
                #la receta se guarda como un diccionario dentro del diccionario 
                recetas_dict[receta['nombre']] = {
                    'nombre': receta['nombre'],
                    'categoria': receta['categoria'],
                    'ingredientes': receta['ingredientes'],
                    'preparacion': receta['preparacion'],
                    'tiempo': receta['tiempo']
                }
        #para corroborar que se guardo como diccionario dentro del diccionario
        print(recetas_dict)
        print(type(recetas_dict))


        # guardamos el diccionario actualizado en el archivo json con el utf-8
        with open(ruta, 'w') as archivo:
            json.dump(recetas_dict, archivo, indent=4, ensure_ascii=False)
        
        print('Recetas guardadas exitosamente!')

    #Funcion para eliminar las recetas
    def eliminar_receta(self):
        #si no se selecciono ninguna receta, mostramos un mensaje de error
        if not self.recetas_tree.selection():
            messagebox.showerror("Error", "Seleccione una receta para eliminar.")
            return
        # creamos una ventana para confirmar la eliminación
        self.confirmar_eliminar_window = tk.Toplevel()
        self.confirmar_eliminar_window.title("Eliminar receta")
        self.confirmar_eliminar_window.geometry("300x100")

        # creamos un frame para los botones
        self.confirmar_eliminar_frame = tk.Frame(self.confirmar_eliminar_window)
        self.confirmar_eliminar_frame.pack()

        # creamos un label para el mensaje
        self.confirmar_eliminar_label = tk.Label(self.confirmar_eliminar_frame, text="¿Está seguro de eliminar la receta?")
        self.confirmar_eliminar_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        # creamos un botón para confirmar la eliminación
        self.confirmar_eliminar_button = tk.Button(self.confirmar_eliminar_frame, text="Confirmar", command=self.eliminar_receta_confirmar)
        self.confirmar_eliminar_button.grid(row=1, column=0, padx=5, pady=5)

        # creamos un botón para cancelar la eliminación
        self.cancelar_eliminar_button = tk.Button(self.confirmar_eliminar_frame, text="Cancelar", command=self.confirmar_eliminar_window.destroy)
        self.cancelar_eliminar_button.grid(row=1, column=1, padx=5, pady=5)

    #Funcion para eliminar las recetas
    def eliminar_receta_confirmar(self):
        # cerramos la ventana de confirmación
        self.confirmar_eliminar_window.destroy()

        # obtenemos el nombre de la receta seleccionada
        seleccion = self.recetas_tree.selection()[0]  # solo se puede seleccionar una receta
        nombre_receta = self.recetas_tree.item(seleccion)['values']

        # eliminamos la receta del treeview y del archivo json
        self.recetas_tree.delete(seleccion)


        # eliminamos la receta del archivo json
        with open(ruta, 'r') as archivo:
            recetas_dict = json.load(archivo)

        print('recetas_dict: ', recetas_dict)
        print('Receta a eliminar: ', nombre_receta)
        # da false porque nombre_receta es una lista y recetas_dict.values() es un diccionario, para compararlo debemos convertirlo en un diccionario a traves de un for

        #convertimos la lista en un diccionario
        receta = {}
        # recorremos la lista para obtener el nombre de la receta
        for item in nombre_receta:
            receta['nombre'] = item
            break
    
        # comprobamos si la receta existe en el diccionario
        if receta['nombre'] in recetas_dict:
            print('receta encontrada')
            # eliminamos la receta del diccionario
            del recetas_dict[receta['nombre']]
            # guardamos el diccionario actualizado en el archivo json
            with open(ruta, 'w') as archivo:
                json.dump(recetas_dict, archivo, indent=4)

            # mensaje de que la receta se elimino correctamente
            messagebox.showinfo("Recetario", "Receta eliminada correctamente.")

        #comprobamos si recetas_dict es una lista o un diccionario
        elif isinstance(recetas_dict, list):
            # si es una lista, recorremos la lista para buscar la receta
            for item in recetas_dict:
                if item['nombre'] == receta['nombre']:
                    # eliminamos la receta de la lista
                    recetas_dict.remove(item)
                    # guardamos la lista actualizada en el archivo json
                    with open(ruta, 'w') as archivo:
                        json.dump(recetas_dict, archivo, indent=4)
                    # mensaje de que la receta se elimino correctamente
                    messagebox.showinfo("Recetario", "Receta eliminada correctamente.")
                    break
            else:
                #no es una lista ni un diccionario, por lo tanto para eliminarla debemos eliminarla de la lista de recetas
                for receta in self.recetas:
                    if receta['nombre'] == nombre_receta[0]:
                        self.recetas.remove(receta)
                        messagebox.showinfo("Recetario", "Receta eliminada correctamente.")
                        break
                else:
                    # si no se encontró la receta en la lista es porque es una receta nueva
                    messagebox.showinfo("Recetario", "Receta no encontrada.")
        else:
            print('Receta no encontrada')
    
    #Funcion para cargar las recetas
    def cargar_recetas(self):
        # cargamos las recetas desde el archivo json con el utf-8
        with open(ruta, 'r', encoding='utf-8') as archivo:
            recetas_dict = json.load(archivo)

        # agregamos las recetas al treeview y al diccionario de recetas
        for receta in recetas_dict:
            # para saber si la receta en el diccionario es una lista o un diccionario
            if isinstance(receta, list):
                for item in receta:
                    self.recetas_tree.insert("", "end", values=(item['nombre'], item['categoria'],item['fecha_creacion']))
            # si no es una lista, es un diccionario
            elif isinstance(receta, dict):
                self.recetas_tree.insert("", "end", values=(receta['nombre'], receta['categoria'],receta['fecha_creacion']))
                self.recetas.append(receta)
    
    #Funcion para actualizar las recetas
    def actualizar_lista_recetas(self):
        # limpiamos el treeview
        self.recetas_tree.delete(*self.recetas_tree.get_children())
        # cargamos las recetas desde el archivo json con utf-8
        with open(ruta, 'r', encoding='utf-8') as archivo:
            recetas_dict = json.load(archivo)

        #si la receta es una lista la agregamos al treeview
        if isinstance(recetas_dict, list):
            for item in recetas_dict:
                self.recetas_tree.insert("", "end", values=(item['nombre'], item['categoria'],item['fecha_creacion']))
        
    #Funcion de editar receta
    def editar_receta(self):
        # Obtenemos el nombre de la receta seleccionada
        seleccion = self.recetas_tree.selection()[0]
        nombre_receta = self.recetas_tree.item(seleccion)['values'][0]
 
        # Buscamos la receta en el diccionario de recetas y en el archivo json con utf-8
        with open(ruta, 'r', encoding='utf-8') as archivo:
            recetas_dict = json.load(archivo)

        # recetas_dict es un diccionario, por lo tanto debemos convertirlo en una lista para poder compararlo
        for receta in recetas_dict:
            #lo convertimos en diccionario
            receta = dict(receta)
            #accedemos al nombre de la receta
            nombre = receta['nombre']
            #comparamos el nombre de la receta con el nombre de la receta seleccionada
            if nombre == nombre_receta:
                print('receta encontrada')
                # llamamos a la funcion para editar la ventana
                self.editar_ventana_receta(receta)
                break

    #Funcion de editar ventana receta
    def editar_ventana_receta(self, nombre_receta):
         # Creamos una ventana para editar la receta
            self.editar_receta_window = tk.Toplevel()
            self.editar_receta_window.title("Editar receta")
            self.editar_receta_window.geometry("500x400")
            self.editar_receta_window.resizable(0, 0)

            # Creamos las entrys para editar los datos de la receta
            tk.Label(self.editar_receta_window, text="Nombre de la receta: ").grid(row=0, column=0, padx=10, pady=10)
            nombre_entry = tk.Entry(self.editar_receta_window, width=30)
            nombre_entry.insert(0, nombre_receta['nombre'])
            nombre_entry.grid(row=0, column=1)

            tk.Label(self.editar_receta_window, text="Ingredientes (cantidad y unidad de medida)").grid(row=1, column=0, padx=10, pady=10)
            ingredientes_entry = tk.Entry(self.editar_receta_window, width=30)
            ingredientes_entry.insert(0, nombre_receta['ingredientes'])
            ingredientes_entry.grid(row=1, column=1)

            tk.Label(self.editar_receta_window, text="Instrucciones:").grid(row=2, column=0, padx=10, pady=10)
            pasos_entry = tk.Entry(self.editar_receta_window, width=30)
            pasos_entry.insert(0, nombre_receta['instrucciones'])
            pasos_entry.grid(row=2, column=1)

            tk.Label(self.editar_receta_window, text="Categoria: ").grid(row=3, column=0, padx=10, pady=10)
            categoria_entry = tk.Entry(self.editar_receta_window, width=30)
            categoria_entry.insert(0, nombre_receta['categoria'])
            categoria_entry.grid(row=3, column=1)

            #label para los tiempos de preparacion y coccion
            tk.Label(self.editar_receta_window, text="Tiempo de preparación (en minutos)").grid(row=4, column=0, padx=10, pady=10)
            tk.Label(self.editar_receta_window, text="Tiempo de cocción (en minutos)").grid(row=5, column=0, padx=10, pady=10)
            #entry para los tiempos de preparacion y coccion
            tiempo_preparacion_entry = tk.Entry(self.editar_receta_window, width=30)
            tiempo_preparacion_entry.insert(0, nombre_receta['tiempo_preparacion'])
            tiempo_preparacion_entry.grid(row=4, column=1)
            tiempo_coccion_entry = tk.Entry(self.editar_receta_window, width=30)
            tiempo_coccion_entry.insert(0, nombre_receta['tiempo_coccion'])
            tiempo_coccion_entry.grid(row=5, column=1)
            
            #label fecha
            tk.Label(self.editar_receta_window, text="Fecha de creación: ").grid(row=6, column=0, padx=10, pady=10)
            #entry fecha
            fecha_entry = tk.Entry(self.editar_receta_window, width=30)
            fecha_entry.insert(0, nombre_receta['fecha_creacion'])
            fecha_entry.grid(row=6, column=1)


            # Creamos un botón para guardar los cambios
            tk.Button(self.editar_receta_window, text="Guardar cambios", command=lambda: self.guardar_cambios(nombre_entry.get(), ingredientes_entry.get(), pasos_entry.get(), categoria_entry.get(), tiempo_preparacion_entry.get(), tiempo_coccion_entry.get(), nombre_receta, fecha_entry.get())).grid(row=7, column=0, columnspan=2, padx=10, pady=10)
            # Creamos un botón para cancelar los cambios
            tk.Button(self.editar_receta_window, text="Cancelar", command=self.editar_receta_window.destroy).grid(row=7, column=0, columnspan=2, padx=10, pady=10)

    #funcion para guardar los cambios
    def guardar_cambios(self, nombre, ingredientes, pasos, categoria, tiempo_preparacion, tiempo_coccion, fecha_creacion, receta):
        # Creamos un diccionario con los datos de la receta
        receta_editada = {
            'nombre': nombre,
            'ingredientes': ingredientes,
            'instrucciones': pasos,
            'categoria': categoria,
            'tiempo_preparacion': tiempo_preparacion,
            'tiempo_coccion': tiempo_coccion,
            'fecha_creacion': fecha_creacion
        }

        # Buscamos la receta en el diccionario de recetas
        for receta in self.recetas:
            if receta['nombre'] == nombre:
                # Reemplazamos la receta por la receta editada
                self.recetas[self.recetas.index(receta)] = receta_editada
                break

        # Actualizamos el archivo json
        with open(ruta, 'w') as archivo:
            json.dump(self.recetas, archivo, indent=4)

        # Actualizamos el treeview
        self.actualizar_lista_recetas()

        # Cerramos la ventana de editar receta
        self.editar_receta_window.destroy()





#inicio de la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = Recetario(root)
    root.mainloop()


## un diccionario ejemplo de receta
# receta = {
#     'nombre': 'Tortilla de patatas',
#     'ingredientes': '4 huevos, 2 patatas, 1 cebolla, 1 pimiento verde, 1 pimiento rojo, 1 tomate, 1 cucharada de aceite de oliva, sal, pimienta',
#     'instrucciones': 'Cortar las patatas en rodajas finas, la cebolla en juliana, los pimientos en tiras y el tomate en rodajas. Salpimentar y freír en una sartén con aceite de oliva. Batir los huevos y salpimentar. Añadir la mezcla de patatas y freír la tortilla.',
#     'categoria': 'Desayuno',
#     'tiempo_preparacion': '30',
#     'tiempo_coccion': '15'
# }
# una lista ejemplo de recetas
# recetas = [r
#     receta,
#     {
#         'nombre': 'Ensalada de pasta',
#         'ingredientes': '1 paquete de pasta, 1 tomate, 1 cebolla, 1 pimiento verde, 1 pimiento rojo, 1 cucharada de aceite de oliva, sal, pimienta',


