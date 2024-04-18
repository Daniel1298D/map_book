from models.data import users
from utils.crud import show_users,add_new_user


if __name__ == "__main__":
    print("witaj użytkowniku")
    while True:
        print("MENU:")
        print("0. zakończ program")
        print("1. wyswietl co u znajomych")
        menu_option: str = input("dokonaj wyboru:")
        print("2.Dodaj użytkownika")
        if menu_option == "0":
            print("program kończy pracę")
            break
        if menu_option == "1":
            show_users(users)
        if menu_option == "2":
            add_new_user(users)