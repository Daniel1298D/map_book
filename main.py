from models.data import users
from utils.crud import show_users


if __name__ == "__main__":
    print("witaj użytkowniku")
    while True:
        print("MENU:")
        print("1. wyswietl co u znajomych")
        menu_option: str = input("dokonaj wyboru:")
        if menu_option == "0":
            print("program kończy pracę")
            break
        if menu_option == "1":
            show_users(users)
