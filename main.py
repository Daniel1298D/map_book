from models.data import users
from utils.crud import show_users,add_new_user,search_users,remove_users

if __name__ == "__main__":
    print("witaj użytkowniku")
    while True:
        print("MENU:")
        print("0. zakończ program")
        print("1. wyswietl co u znajomych")
        print("2.Dodaj użytkownika")
        print("3. znajdź użytkownika")
        if menu_option == "0":
            print("program kończy pracę")
            print("4. usuń użytkownika")
            menu_option: str = input("dokonaj wyboru:")
            break
        if menu_option == "1":
            show_users(users)
        if menu_option == "2":
            add_new_user(users)
        if menu_option == "3":
            search_user(users)
        if menu_option == "4":
            remove_users(users)