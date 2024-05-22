from tkinter import *

import tkintermapview

users:list=[]

class User:
    def __init__(self,name,surname,posts,location):
        self.name=name
        self.surname=surname
        self.posts=posts
        self.location=location


def add_new_user():
    user=User(name=entry_name.get(),surname=entry_surname.get(),posts=entry_posts.get(),location=entry_location.get())
    users.append(user)
    display_users()
    entry_name.delete(0,END)
    entry_surname.delete(0,END)
    entry_posts.delete(0,END)
    entry_location.delete(0,END)
    entry_name.focus()

def display_users():
    listbox_lista_uzytkownikow.delete(0,END)
    for idx,user in enumerate(users):
        listbox_lista_uzytkownikow.insert(idx, f'{idx+1}. {user.name} {user.surname}')

def delete_user():

    print(listbox_lista_uzytkownikow.index(ACTIVE))
    users.pop(listbox_lista_uzytkownikow.index(ACTIVE))
    display_users()

def show_user_details():
    i=listbox_lista_uzytkownikow.index(ACTIVE)
    label_opis_name_uzytkownika_wartosc.config(text=users[i].name)
    label_opis_surname_uzytkownika_wartosc.config(text=users[i].surname)
    label_opis_posts_uzytkownika_wartosc.config(text=users[i].posts)
    label_opis_location_uzytkownika_wartosc.config(text=users[i].location)


def edit_user():
    entry_name.delete(0, END)
    entry_surname.delete(0, END)
    entry_posts.delete(0, END)
    entry_location.delete(0, END)
    i=listbox_lista_uzytkownikow.index(ACTIVE)
    entry_name.insert(END,users[i].name)

    button_dodaj_uztykownika.config(text='Zapisz zmiany',command=lambda: update_user(i))




def update_user(i):
    users[i].name = entry_name.get()
    users[i].surname = entry_surname.get()
    users[i].posts = entry_posts.get()
    users[i].location = entry_location.get()
    display_users()
    button_dodaj_uztykownika.config(text='Dodaj użytkownika',command=add_new_user)
    entry_name.delete(0, END)
    entry_surname.delete(0, END)
    entry_posts.delete(0, END)
    entry_location.delete(0, END)
    entry_name.focus()


root=Tk()
root.geometry('800x700')
root.title('MapBook')

# ramki do porządkowania struktury
ramka_lista_uzytkownikow=Frame(root)
ramka_formularz=Frame(root)
ramka_szczegoly_uzytkownika=Frame(root)

ramka_lista_uzytkownikow.grid(row=0, column=0, padx=50)
ramka_formularz.grid(row=0, column=1)
ramka_szczegoly_uzytkownika.grid(row=1, column=0, columnspan=2, padx=50, pady=20)



# ramka lista obiektów
label_lista_uzytkownikow=Label(ramka_lista_uzytkownikow,text='Lista użytkowników')
listbox_lista_uzytkownikow=Listbox(ramka_lista_uzytkownikow,width=30)
button_pokaz_szczegoly=Button(ramka_lista_uzytkownikow,text='Pokaż szczegóły',command=show_user_details)
button_usun_uzytkownika=Button(ramka_lista_uzytkownikow,text='Usuń',command=delete_user)
button_edytuj_uzytkownika=Button(ramka_lista_uzytkownikow,text='Edytuj',command=edit_user)

label_lista_uzytkownikow.grid(row=0, column=0)
listbox_lista_uzytkownikow.grid(row=1, column=0, columnspan=3)
button_pokaz_szczegoly.grid(row=2, column=0)
button_usun_uzytkownika.grid(row=2, column=1)
button_edytuj_uzytkownika.grid(row=2, column=2)

# ramka formularz
label_napis_formularz=Label(ramka_formularz,text='Formularz edycji i dodawania')
label_name=Label(ramka_formularz,text='Imię')
label_surname=Label(ramka_formularz,text='Nazwisko')
label_posts=Label(ramka_formularz,text='Liczba postów')
label_location=Label(ramka_formularz,text='Miejscowosc')

entry_name=Entry(ramka_formularz)
entry_surname=Entry(ramka_formularz, width=30)
entry_posts=Entry(ramka_formularz)
entry_location=Entry(ramka_formularz)

button_dodaj_uztykownika=Button(ramka_formularz,text='Dodaj użytkownika',command=add_new_user)

label_napis_formularz.grid(row=0, column=0, columnspan=2)
label_name.grid(row=1, column=0, sticky=W)
label_surname.grid(row=2, column=0, sticky=W)
label_posts.grid(row=3, column=0, sticky=W)
label_location.grid(row=4, column=0, sticky=W)

entry_name.grid(row=1, column=1, sticky=W)
entry_surname.grid(row=2, column=1, sticky=W)
entry_posts.grid(row=3, column=1, sticky=W)
entry_location.grid(row=4, column=1, sticky=W)

button_dodaj_uztykownika.grid(row=5, column=0,columnspan=2)

# ramka pokaz szczegoly
label_opis_uzytkownika=Label(ramka_szczegoly_uzytkownika,text='Szczegóły użytkownika')
label_opis_name_uzytkownika=Label(ramka_szczegoly_uzytkownika,text='Imię')
label_opis_name_uzytkownika_wartosc=Label(ramka_szczegoly_uzytkownika,text='....',width=10)
label_opis_surname_uzytkownika=Label(ramka_szczegoly_uzytkownika,text='Nazwisko')
label_opis_surname_uzytkownika_wartosc=Label(ramka_szczegoly_uzytkownika,text='....',width=10)
label_opis_posts_uzytkownika=Label(ramka_szczegoly_uzytkownika,text='Liczba postów')
label_opis_posts_uzytkownika_wartosc=Label(ramka_szczegoly_uzytkownika,text='....',width=10)
label_opis_location_uzytkownika=Label(ramka_szczegoly_uzytkownika,text='Miejscowosc')
label_opis_location_uzytkownika_wartosc=Label(ramka_szczegoly_uzytkownika,text='....',width=10)

label_opis_uzytkownika.grid(row=0, column=0)
label_opis_name_uzytkownika.grid(row=1, column=1)
label_opis_name_uzytkownika_wartosc.grid(row=1, column=2)
label_opis_surname_uzytkownika.grid(row=1, column=3)
label_opis_surname_uzytkownika_wartosc.grid(row=1, column=4)
label_opis_posts_uzytkownika.grid(row=1, column=5)
label_opis_posts_uzytkownika_wartosc.grid(row=1, column=6)
label_opis_location_uzytkownika.grid(row=1, column=7)
label_opis_location_uzytkownika_wartosc.grid(row=1, column=8)

map_widget=tkintermapview.TkinterMapView(ramka_szczegoly_uzytkownika,width=700,height=300)
map_widget.grid(row=2, column=0, columnspan=8)
map_widget.set_position(52.21,21.00)
map_widget.set_zoom(10)


root.mainloop()
