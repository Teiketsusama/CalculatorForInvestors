class MenuDisplay:
    def __init__(self):
        self.main_menu = "MAIN MENU\n" \
                         "0 Exit\n" \
                         "1 CRUD operations\n" \
                         "2 Show top ten companies by criteria\n"

        self.crud_menu = "\nCRUD MENU\n" \
                         "0 Back\n" \
                         "1 Create a company\n" \
                         "2 Read a company\n" \
                         "3 Update a company\n" \
                         "4 Delete a company\n" \
                         "5 List all companies\n"

        self.top_ten_menu = "\nTOP TEN MENU\n" \
                            "0 Back\n" \
                            "1 List by ND/EBITDA\n" \
                            "2 List by ROE\n" \
                            "3 List by ROA\n"

    def display_main_menu(self):
        print(self.main_menu)

    def display_crud_menu(self):
        print(self.crud_menu)

    def display_top_ten_menu(self):
        print(self.top_ten_menu)


def crud_menu():
    while True:
        user_input = input("Enter an option:\n")
        if user_input == "0":
            return
        elif user_input in ["1", "2", "3", "4", "5"]:
            print("Not implemented!\n")
            return
        else:
            print("Invalid option!\n")


def top_ten_menu():
    while True:
        user_input = input("Enter an option:\n")
        if user_input == "0":
            return
        elif user_input in ["1", "2", "3"]:
            print("Not implemented!\n")
            return
        else:
            print("Invalid option!\n")


def main():
    while True:
        MenuDisplay().display_main_menu()
        user_input = input("Enter an option:\n")
        if user_input == "0":
            print("Have a nice day!")
            exit()
        elif user_input == "1":
            MenuDisplay().display_crud_menu()
            crud_menu()
        elif user_input == "2":
            MenuDisplay().display_top_ten_menu()
            top_ten_menu()
        else:
            print("Invalid option!\n")


if __name__ == "__main__":
    main()
