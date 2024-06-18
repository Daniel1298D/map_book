from tkinter import *
from tkinter import messagebox
import tkintermapview
from bs4 import BeautifulSoup
import requests
import logging

logging.basicConfig(filename='../program.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')

uzytkownicy = {
    'geoinfa': 'rzadzi',
    'rozpoznanie': 'tez',
    'meteo': 'mozebyc',
}   
    
def zaloguj():
    username = entry_username.get()
    password = entry_password.get()

    if username in uzytkownicy and uzytkownicy[username] == password:
        messagebox.showinfo("Logowanie", "Logowanie przeprowadzono pomyślnie.")
        okno_logowania.destroy()
    else:
        messagebox.showerror("Logowanie", "Niepoprawna nazwa użytkownika lub hasło.")
        entry_username.delete(0, END)
        entry_password.delete(0, END)

okno_logowania = Tk()
okno_logowania.title("Logowanie")
okno_logowania.geometry("400x200")

Label(okno_logowania, text="Użytkownik:").pack()
entry_username = Entry(okno_logowania)
entry_username.pack()

Label(okno_logowania, text="Hasło:").pack()
entry_password = Entry(okno_logowania, show="*")
entry_password.pack()

Button(okno_logowania, text="Zaloguj", command=zaloguj).pack()

okno_logowania.mainloop()

firmy = []
klienci = []
pracownicy = []
current_edit = None

class User:
    def __init__(self, nazwa, lokalizacja, lista_entitetow, widget_maps):
        self.nazwa = nazwa
        self.lokalizacja = lokalizacja
        self.koordynaty = self.pobierz_koordynaty()
        self.marker = widget_maps.set_marker(self.koordynaty[0], self.koordynaty[1], text=self.nazwa)
        lista_entitetow.append(self)

    def pobierz_koordynaty(self):
        url = f'https://pl.wikipedia.org/wiki/{self.lokalizacja}'
        response = requests.get(url)
        response_html = BeautifulSoup(response.text, 'html.parser')
        return [
            float(response_html.select('.latitude')[1].text.replace(",", ".")),
            float(response_html.select('.longitude')[1].text.replace(",", "."))
        ]

    def usun_marker(self):
        self.marker.delete()

class Biura(User):
    def __init__(self, nazwa, lokalizacja, widget_maps):
        super().__init__(nazwa, lokalizacja, firmy, widget_maps)
        self.klienci = []
        self.pracownicy = []

class Klient(User):
    def __init__(self, nazwa, lokalizacja, firma, widget_maps):
        super().__init__(nazwa, lokalizacja, klienci, widget_maps)
        self.firma = firma
        self.firma.klienci.append(self)

class Pracownik(User):
    def __init__(self, nazwa, lokalizacja, firma, widget_maps):
        super().__init__(nazwa, lokalizacja, pracownicy, widget_maps)
        self.firma = firma
        self.firma.pracownicy.append(self)

def pokaz_dane(lista_entitetow, lista):
    lista.delete(0, END)
    for entity in lista_entitetow:
        lista.insert(END, f'{entity.nazwa} - {entity.lokalizacja}')

def dodaj_firme():
    nazwa = entry_firma_nazwa.get()
    lokalizacja = entry_firma_lokalizacja.get()
    Biura(nazwa, lokalizacja, widget_mapy)
    pokaz_dane(firmy, listbox_firmy)
    entry_firma_nazwa.delete(0, END)
    entry_firma_lokalizacja.delete(0, END)

def dodaj_klienta():
    nazwa = entry_klient_nazwa.get()
    lokalizacja = entry_klient_lokalizacja.get()
    nazwa_firmy = entry_klient_firma.get()
    firma = next((f for f in firmy if f.nazwa == nazwa_firmy), None)
    if firma:
        Klient(nazwa, lokalizacja, firma, widget_mapy)
        pokaz_dane(klienci, listbox_klienci)
        entry_klient_nazwa.delete(0, END)
        entry_klient_lokalizacja.delete(0, END)
        entry_klient_firma.delete(0, END)

def dodaj_pracownika():
    nazwa = entry_pracownik_nazwa.get()
    lokalizacja = entry_pracownik_lokalizacja.get()
    nazwa_firmy = entry_pracownik_firma.get()
    firma = next((f for f in firmy if f.nazwa == nazwa_firmy), None)
    if firma:
        Pracownik(nazwa, lokalizacja, firma, widget_mapy)
        pokaz_dane(pracownicy, listbox_pracownicy)
        entry_pracownik_nazwa.delete(0, END)
        entry_pracownik_lokalizacja.delete(0, END)
        entry_pracownik_firma.delete(0, END)

def usun_User(lista_entitetow, lista):
    selected_index = lista.curselection()[0]
    entity = lista_entitetow[selected_index]
    entity.usun_marker()
    lista_entitetow.pop(selected_index)
    pokaz_dane(lista_entitetow, lista)

def pokaz_szczegoly_firmy():
    selected_index = listbox_firmy.curselection()[0]
    firma = firmy[selected_index]
    pokaz_dane(firma.klienci, listbox_klienci)
    pokaz_dane(firma.pracownicy, listbox_pracownicy)

def edytuj_firme():
    global current_edit
    selected_index = listbox_firmy.curselection()[0]
    current_edit = ("firma", selected_index)
    firma = firmy[selected_index]
    entry_firma_nazwa.insert(0, firma.nazwa)
    entry_firma_lokalizacja.insert(0, firma.lokalizacja)
    button_firma.config(text="Wprowadź zmiany", command=update_firma)

def edytuj_klienta():
    global current_edit
    selected_index = listbox_klienci.curselection()[0]
    current_edit = ("klient", selected_index)
    klient = klienci[selected_index]
    entry_klient_nazwa.insert(0, klient.nazwa)
    entry_klient_lokalizacja.insert(0, klient.lokalizacja)
    entry_klient_firma.insert(0, klient.firma.nazwa)
    button_klient.config(text="Wprowadź zmiany", command=update_klient)

def edytuj_pracownika():
    global current_edit
    selected_index = listbox_pracownicy.curselection()[0]
    current_edit = ("pracownik", selected_index)
    pracownik = pracownicy[selected_index]
    entry_pracownik_nazwa.insert(0, pracownik.nazwa)
    entry_pracownik_lokalizacja.insert(0, pracownik.lokalizacja)
    entry_pracownik_firma.insert(0, pracownik.firma.nazwa)
    button_pracownik.config(text="Wprowadź zmiany", command=update_pracownik)

def update_firma():
    global current_edit
    if current_edit:
        entity_type, index = current_edit
        if entity_type == "firma":
            firma = firmy[index]
            firma.usun_marker()
            firma.nazwa = entry_firma_nazwa.get()
            firma.lokalizacja = entry_firma_lokalizacja.get()
            firma.koordynaty = firma.pobierz_koordynaty()
            firma.marker = widget_mapy.set_marker(firma.koordynaty[0], firma.koordynaty[1], text=firma.nazwa)
            pokaz_dane(firmy, listbox_firmy)
            button_firma.config(text="Wprowadź dane", command=dodaj_firme)
            current_edit = None
            entry_firma_nazwa.delete(0, END)
            entry_firma_lokalizacja.delete(0, END)

def update_klient():
    global current_edit
    if current_edit:
        entity_type, index = current_edit
        if entity_type == "klient":
            klient = klienci[index]
            klient.usun_marker()
            klient.nazwa = entry_klient_nazwa.get()
            klient.lokalizacja = entry_klient_lokalizacja.get()
            klient.koordynaty = klient.pobierz_koordynaty()
            klient.marker = widget_mapy.set_marker(klient.koordynaty[0], klient.koordynaty[1], text=klient.nazwa)
            pokaz_dane(klienci, listbox_klienci)
            button_klient.config(text="Wprowadź dane", command=dodaj_klienta)
            current_edit = None
            entry_klient_nazwa.delete(0, END)
            entry_klient_lokalizacja.delete(0, END)
            entry_klient_firma.delete(0, END)

def update_pracownik():
    global current_edit
    if current_edit:
        entity_type, index = current_edit
        if entity_type == "pracownik":
            pracownik = pracownicy[index]
            pracownik.usun_marker()
            pracownik.nazwa = entry_pracownik_nazwa.get()
            pracownik.lokalizacja = entry_pracownik_lokalizacja.get()
            pracownik.koordynaty = pracownik.pobierz_koordynaty()
            pracownik.marker = widget_mapy.set_marker(pracownik.koordynaty[0], pracownik.koordynaty[1], text=pracownik.nazwa)
            pokaz_dane(pracownicy, listbox_pracownicy)
            button_pracownik.config(text="Wprowadź dane", command=dodaj_pracownika)
            current_edit = None
            entry_pracownik_nazwa.delete(0, END)
            entry_pracownik_lokalizacja.delete(0, END)
            entry_pracownik_firma.delete(0, END)

root = Tk()
root.title("System do zarządzania firmami PR i ich klientami")
root.geometry("1920x1080")

ramka_biura = Frame(root)
ramka_klienci = Frame(root)
ramka_pracownicy = Frame(root)
ramka_dodaj_biuro = Frame(root)
ramka_dodaj_klienta = Frame(root)
ramka_dodaj_pracownika = Frame(root)

ramka_biura.grid(row=0, column=0, padx=5, pady=5, sticky=N + S + E + W)
ramka_klienci.grid(row=0, column=1, padx=5, pady=5, sticky=N + S + E + W)
ramka_pracownicy.grid(row=0, column=2, padx=5, pady=5, sticky=N + S + E + W)
ramka_dodaj_biuro.grid(row=1, column=0, padx=5, pady=5, sticky=N + S + E + W)
ramka_dodaj_klienta.grid(row=1, column=1, padx=5, pady=5, sticky=N + S + E + W)
ramka_dodaj_pracownika.grid(row=1, column=2, padx=5, pady=5, sticky=N + S + E + W)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)

Label(ramka_biura, text="Biura").grid(row=0, column=0)
listbox_firmy = Listbox(ramka_biura, width=40, height=30)
listbox_firmy.grid(row=1, column=0, sticky=N + S + E + W)
Button(ramka_biura, text="Pokaż przypisanych klientów i pracowników", command=pokaz_szczegoly_firmy).grid(row=2, column=0)
Button(ramka_biura, text="Usuń Biuro", command=lambda: usun_User(firmy, listbox_firmy)).grid(row=3, column=0)
Button(ramka_biura, text="Edytuj Biuro", command=edytuj_firme).grid(row=4, column=0)

Label(ramka_klienci, text="Klienci:").grid(row=0, column=0)
listbox_klienci = Listbox(ramka_klienci, width=40, height=30)
listbox_klienci.grid(row=1, column=0, sticky=N + S + E + W)
Button(ramka_klienci, text="Usuń Klienta", command=lambda: usun_User(klienci, listbox_klienci)).grid(row=2, column=0)
Button(ramka_klienci, text="Edytuj Klienta", command=edytuj_klienta).grid(row=3, column=0)

Label(ramka_pracownicy, text="Pracownicy:").grid(row=0, column=0)
listbox_pracownicy = Listbox(ramka_pracownicy, width=40, height=30)
listbox_pracownicy.grid(row=1, column=0, sticky=N + S + E + W)
Button(ramka_pracownicy, text="Usuń Pracownika", command=lambda: usun_User(pracownicy, listbox_pracownicy)).grid(row=2, column=0)
Button(ramka_pracownicy, text="Edytuj Pracownika", command=edytuj_pracownika).grid(row=3, column=0)

Label(ramka_dodaj_biuro, text="Dodaj nowe biuro").grid(row=0, column=0, columnspan=2)
Label(ramka_dodaj_biuro, text="Nazwa biura:").grid(row=1, column=0)
entry_firma_nazwa = Entry(ramka_dodaj_biuro)
entry_firma_nazwa.grid(row=1, column=1)
Label(ramka_dodaj_biuro, text="Lokalizacja biura:").grid(row=2, column=0)
entry_firma_lokalizacja = Entry(ramka_dodaj_biuro)
entry_firma_lokalizacja.grid(row=2, column=1)
button_firma = Button(ramka_dodaj_biuro, text="Wprowadź dane", command=dodaj_firme)
button_firma.grid(row=3, column=0, columnspan=2)

Label(ramka_dodaj_klienta, text="Dodaj Klienta").grid(row=0, column=0, columnspan=2)
Label(ramka_dodaj_klienta, text="Imię i nazwisko:").grid(row=1, column=0)
entry_klient_nazwa = Entry(ramka_dodaj_klienta)
entry_klient_nazwa.grid(row=1, column=1)
Label(ramka_dodaj_klienta, text="Lokalizacja klienta:").grid(row=2, column=0)
entry_klient_lokalizacja = Entry(ramka_dodaj_klienta)
entry_klient_lokalizacja.grid(row=2, column=1)
Label(ramka_dodaj_klienta, text="Nazwa podległego biura:").grid(row=3, column=0)
entry_klient_firma = Entry(ramka_dodaj_klienta)
entry_klient_firma.grid(row=3, column=1)
button_klient = Button(ramka_dodaj_klienta, text="Wprowadź dane", command=dodaj_klienta)
button_klient.grid(row=4, column=0, columnspan=2)

Label(ramka_dodaj_pracownika, text="Dodaj Pracownika").grid(row=0, column=0, columnspan=2)
Label(ramka_dodaj_pracownika, text="Imię i nazwisko:").grid(row=1, column=0)
entry_pracownik_nazwa = Entry(ramka_dodaj_pracownika)
entry_pracownik_nazwa.grid(row=1, column=1)
Label(ramka_dodaj_pracownika, text="Lokalizacja pracownika:").grid(row=2, column=0)
entry_pracownik_lokalizacja = Entry(ramka_dodaj_pracownika)
entry_pracownik_lokalizacja.grid(row=2, column=1)
Label(ramka_dodaj_pracownika, text="Nazwa podległego biura:").grid(row=3, column=0)
entry_pracownik_firma = Entry(ramka_dodaj_pracownika)
entry_pracownik_firma.grid(row=3, column=1)
button_pracownik = Button(ramka_dodaj_pracownika, text="Wprowadź dane", command=dodaj_pracownika)
button_pracownik.grid(row=4, column=0, columnspan=2)

widget_mapy = tkintermapview.TkinterMapView(root, width=900, height=800)
widget_mapy.set_position(52.0, 19.0)
widget_mapy.set_zoom(7)
widget_mapy.grid(row=0, column=3, rowspan=3, padx=5, pady=5, sticky=N + S + E + W)

root.mainloop()