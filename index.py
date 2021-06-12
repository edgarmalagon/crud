from os import name
from tkinter import ttk
from tkinter import *

import sqlite3

class Product:
    
    db_name = 'database.db'
    
    def __init__(self, window):
        self.wind = window
        self.wind.title('Aplicacion ejercicio productos')
        
        #creando un Frame
        frame = LabelFrame(self.wind, text = 'Registrar un nuevo producto')
        frame.grid(row=0, column=0, columnspan=3, pady=20)
        
        #input de Nombre
        Label(frame, text='Nombre: ').grid(row=1, column=0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row=1, column=1)
        
        #input de Precio
        Label(frame, text='Precio: ').grid(row=2, column=0)
        self.price = Entry(frame)
        self.price.grid(row=2, column=1)
        
        #boton agregar producto
        ttk.Button(frame, text= 'Guardar producto', command=self.add_product).grid(row=3, columnspan=2, sticky=W+E)
        
        #mensajes de salida
        self.message = Label(text='', fg='red')
        self.message.grid(row=3, column=0, columnspan=2, sticky=W+E)
        
        #tabla
        self.tree = ttk.Treeview(height=10, columns=2)
        self.tree.grid(row=4, column=0, columnspan=2)
        self.tree.heading("#0", text='Nombre', anchor=CENTER)
        self.tree.heading("#1", text='Precio', anchor=CENTER)
        
        #botones para borrado y edicion
        ttk.Button(text= 'Borrar producto', command=self.delete_product).grid(row=5, column=0, sticky=W+E)
        ttk.Button(text= 'Editar producto', command=self.edit_product).grid(row=5, column=1, sticky=W+E)
        
        #carga los datos
        self.get_products()
    
    def run_query(self, query, parametros=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            resultados = cursor.execute(query, parametros)
            conn.commit()
        return resultados
    
    def get_products(self):
        query = 'SELECT * FROM products ORDER BY nombre DESC'
        db_rows = self.run_query(query)
        records = self.tree.get_children()
        for element in records:
            """limpia la tabla"""
            self.tree.delete(element)
        for row in db_rows:
            print(row)
            self.tree.insert('',0,text=row[1], values=row[2])
    
    def add_product(self):
        if self.validation():
            print(self.name.get())
            print(self.price.get())
            query = 'INSERT INTO products VALUES(NULL, ?, ?)'
            parametros = (self.name.get(), self.price.get())
            self.run_query(query, parametros)
            print('Datos guardados')
            self.message['text']='Producto {} ha sido agregado satisfactoriamente'.format(self.name.get())
            self.name.delete(0, END)
            self.price.delete(0, END)
        else:
            print("Precio y nombre requeridos")
            self.message['text']='Precio y nombre requeridos'
        
        self.get_products()
    
    def delete_product(self):
        self.message['text'] =''
        print(self.tree.item(self.tree.selection()))
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Selecciona un registro'
            return
        name =  self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM products WHERE nombre=?'
        self.run_query(query, (name,))
        self.message['text'] = 'El registro {} ha sido eliminado'.format(name)
        self.get_products()
    
    def edit_product(self):
        self.message['text']=''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Selecciona un registro'
            return
        name =   self.tree.item(self.tree.selection())['text']
        old_price =  self.tree.item(self.tree.selection())['values'][0]
        self.edit_wind = Toplevel()
        self.edit_wind.geometry("300x300")
        self.edit_wind.title = 'Editar producto'
        
        #old name
        Label(self.edit_wind, text="Nombre actual: ").grid(row=0, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value= name), state='readonly').grid(row=0, column=2)
        #new name
        Label(self.edit_wind, text="Nombre nuevo: ").grid(row=1, column=1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row=1, column=2)
        
        #old price
        Label(self.edit_wind, text="Precio actual: ").grid(row=2, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value= old_price), state='readonly').grid(row=2, column=2)
        #new price
        Label(self.edit_wind, text="Precio nuevo: ").grid(row=3, column=1)
        new_price = Entry(self.edit_wind)
        new_price.grid(row=3, column=2)
              
        Button(self.edit_wind, text="Actualizar", command = lambda : self.edit_records(new_name.get(), name, new_price.get(), old_price)).grid(row=4, column=2, sticky=W)

        
    def edit_records(self, new_name, name, new_price, old_price):
        query = 'UPDATE products SET nombre=?, precio=? WHERE nombre = ? AND precio = ?'
        parametros = (new_name, new_price, name, old_price)
        self.run_query(query, parametros)
        self.edit_wind.destroy()
        self.message['text'] = 'Producto {} actualizado a {}'.format(name, new_name)
        self.get_products()
        
        
    def validation(self):
        return len(self.name.get())!=0 and len(self.price.get())!=0
    
if __name__ == '__main__':
    window = Tk()
    window.geometry("400x400")
    application = Product(window)
    
    window.mainloop()