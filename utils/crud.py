def show_users(user_list: list[dict]) -> None:
    for user in user_list:
        print(f"Twój znajomy {user['name']} opublikowal: {user['posts']}")

def add_new_user(users:list)->None:
    new_name: str = input("Enter your new name: ")
    new_surname: str = input("Enter your new surname: ")
    new_posts: int = int(input("Enter your new posts: "))
    new_user: dict = {"name": new_name, "surname": new_surname, "posts": new_posts}
    users.append(new_user)