from datetime import datetime, timedelta
from address_book import AddressBook
from record import Record


def input_error(handler):
    """Декоратор для обробки помилок користувацького вводу."""
    def wrapper(*args, **kwargs):
        try:
            return handler(*args, **kwargs)
        except (IndexError, KeyError, ValueError) as e:
            return str(e)
    return wrapper


@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_phone(args, book: AddressBook):
    """Змінює номер телефону для конкретного контакту."""
    name, old_phone, new_phone = args
    record = book.find(name)
    if record is None:
        return f"No contact found with name '{name}'."
    record.edit_phone(old_phone, new_phone)
    return f"Phone number updated for {name}."

@input_error
def show_phones(args, book: AddressBook):
    """Show all phone numbers for a specific contact."""
    """Показує всі телефонні номери для якогось конкретного контакту"""
    name = args[0]
    record = book.find(name)
    if record is None:
        return f"No contact found with name '{name}'."
    phones = "; ".join(phone.value for phone in record.phones)
    return f"{name}'s phone numbers: {phones}"

@input_error
def show_all_contacts(book: AddressBook):
    """Display all contacts and their details in the address book."""
    if not book.data:
        return "No contacts in the address book."
    result = "All contacts:\n"
    for record in book.data.values():
        result += f"{record}\n"
    return result.strip()


@input_error
def add_birthday(args, book: AddressBook):
    name, birthday = args
    record = book.find(name)
    if record is None:
        return f"No contact found with name '{name}'."
    record.add_birthday(birthday)
    return f"Birthday added for {name}."


@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record is None:
        return f"No contact found with name '{name}'."
    if record.birthday:
        return f"{name}'s birthday is on {record.birthday.value.strftime('%d.%m.%Y')}."
    return f"No birthday set for {name}."


@input_error
def birthdays(args, book: AddressBook):
    days = int(args[0]) if args else 7
    upcoming_birthdays = book.get_upcoming_birthdays(days)
    if not upcoming_birthdays:
        return "No upcoming birthdays in the next week."
    result = "Upcoming birthdays:\n"
    for record in upcoming_birthdays:
        result += f"{record.name.value}: {record.birthday.value.strftime('%d.%m.%Y')}\n"
    return result


def parse_input(user_input):
    """Розбиває введений користувачем рядок на команду та аргументи."""
    parts = user_input.split()
    return parts[0], parts[1:]


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_phone(args, book))

        elif command == "phone":
            print(show_phones(args, book))

        elif command == "all":
            print(show_all_contacts(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()