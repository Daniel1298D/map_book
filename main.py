users: list[dict] = [
    {"name": "Dawid", "surname": "Bałuka", "posts": 6000},
    {"name": "Kewin", "surname": "Czajkowski", "posts": 6002},
    {"name": "Kamil", "surname": "Gil", "posts": 1000000},
    {"name": "Daniel", "surname": "Błaszczyk", "posts": 6}
]


def show_users(user_list: list[dict]) -> None:
    for user in user_list:
        print(f"Twój znajomy {user['name']} opublikowal: {user['posts']}")


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
