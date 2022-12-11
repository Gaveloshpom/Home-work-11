from classes import AddressBook, Record

""""
Commands to use:
hello: Says "Hello" to you
create Name: creates a new contact with {Name}
add number Name Phone: add phone number {Phone} to user with name {Name}
change Name New_name: change users {Name} to {New_name}
show all: shows all users in Book
good bye/close/exit: stops program
delete phone Name Phone: deletes {Phone} of user with name {Name}
page A B : shows users with index from A to B,
birthday Name Birthday_date: add {birthday_date} to {Name},
days left Name: shows how many days left for {Name}`s  birthday,
"""
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "KeyError: Enter user name"
        except ValueError:
            return"ValueError: Give me name and phone please"
        except IndexError:
            return"IndexError: invalid index"
        except TypeError:
            return"TypeError"
    return inner


@input_error
def create(data, *_):
    name = data[0]
    if name not in book:
        book.add_record(name)
        return f"seccesfull created {name} "
    else:
        raise ValueError('This contact already exist.')


@input_error
def delete_phone(main_record: Record, user_info: list):
    return main_record.delete_phone(int(user_info[1]))


@input_error
def change(old_name: Record, new_name):
    if old_name.name.value != new_name[1]:
        return book.change_contact_name(old_name, new_name[1])
    else:
        return f"Old name {old_name.name.value} the same as new {new_name[1]}"


def add_number(main_record: Record, user_info: list):
    return main_record.add_phone(user_info[1])


def add_birthday(main_record: Record, user_info):
    return main_record.add_birthday(user_info[1])


# @input_error
def days_to_birthday(main_record: Record, *_):
    # print(main_record.days_to_birthday())
    return main_record.days_to_birthday()


@input_error
def phone_search(name):
    if name.strip() not in book:
        raise ValueError("This contact does`t exist")
    a = book.get(name.strip())
    return a


@input_error
def exit_func(*_):
    exit("bye")


@input_error
def hello_func(*_):
    return "Hello"


def show_all(*_):
    full_list = []
    for k, v in book.items():
        full_list.append(f"{v.name.value}. Phones: {[i.value for i in v.phones]}. Birthday:{v.birthday.value if v.birthday else None}")
    print(full_list)
    return full_list


def show_part(data: list):
    value_1 = int(data[0])
    value_2 = int(data[1])
    print(book.iterator(value_1, value_2))


def create_data(data):

    new_data = data.strip().split(" ")
    name = new_data[0]
    phone = new_data[1]
    if name.isnumeric():
        raise ValueError("Must be a str, not int/float")
    if not phone.isnumeric():
        raise ValueError("Must be a number, not str")
    return name, phone


def change_input(data):
    if not data:
        return ['', '']
    splited_text = data.split()

    if splited_text[0].lower() in ("add", "good", "delete", "days"):
        return [" ".join(splited_text[:2]).lower(), splited_text[2:]]
    else:
        return [splited_text[0].lower(), splited_text[1:]]


def reaction_func(reaction):
    signature = command_dict[reaction]
    return signature


def break_func():
    return 'Wrong enter.'


def main():
    while True:
        command = input('Enter command for bot: ')
        user_command, user_data = change_input(command)

        if user_command not in command_dict:
            print(f"Unknown command  '{user_command}'")
            continue

        if user_command == "create":
            result = reaction_func(user_command)(user_data)
            print(result)
            continue

        if user_command == "show":
            reaction_func(user_command)(user_data)
            continue

        try:
            main_record = book[user_data[0]] if user_data else None
        except KeyError:
            print(
                f"This contact {user_data[0]} doesn`t found. Please repeat or create new command")
            continue
        result = reaction_func(user_command)(main_record, user_data)
        if result:
            print(result)


command_dict = {
    'hello': hello_func,
    'create': create,
    'change': change,
    'add number': add_number,
    'delete phone': delete_phone,
    'phone': phone_search,
    'show': show_all,
    'good bye': exit_func,
    'close': exit_func,
    'exit': exit_func,
    'page': show_part,
    'birthday': add_birthday,
    'days left': days_to_birthday,
}


if __name__ == '__main__':
    book = AddressBook()
    main()
