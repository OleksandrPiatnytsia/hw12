from clases_use import AddressBook, Name, Phone, Record, Birthday


def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except ValueError as et:

            print(et)

        except IndexError as et:

            print(et)

    return wrapper



@input_error
def get_func_from_text(input_text: str):
    input_command = input_text.strip().split(" ")[0]

    if not input_command:
        raise IndexError("No command inputted! Try again")

    for command, func in COMMANDS_LIST.items():
        if input_command == command:
            return func, input_text.replace(command, "").strip()

    return no_command, input_command


def help(*args):
    return f"""Hello! I am contact manager bot!
I can add new contact with command: 'add', use following syntax: add 'contact name, phone'
I can add new contact with command: 'del', use following syntax: del 'contact name, deleted_phone'
I can change existing contact with command: 'change', use following syntax: change 'contact name, old_phone, new_phone'
I can find contact by phone with command: 'phone', use following syntax: phone 'contact name'
For viewing all list use command: 'show'
For exit use commands: 'exit'"""


@input_error
def hello(*args):
    return f"How can I help you?"


@input_error
def no_command(*args):
    return f"No such '{args[0]}' command use command 'help'"

@input_error
def add(*args):
    input_params = args[0]
    params_list = input_params.split(",")
    if len(params_list) == 1:
        return f"Inputted not correctly data: {input_params}: ',' - is missing: ''"
    elif len(params_list) > 2:
        return f"Inputted not correctly data: {input_params}: to mach parameters!"

    phone = params_list[1].strip()

    for ch in phone:
        if not ch.isdigit():
            return f"Inputted not correctly data: {params_list[1]}: must consist only digits!"

    contact_name = params_list[0].strip().title()

    if CONTACT_DICT.get(contact_name):
        return f"Inputted name: '{contact_name}' already exist"

    for k, v in CONTACT_DICT.items():
        if v == phone:
            return f"Inputted phone: '{phone}' already have contact: '{get_formated_contact(contact_name, phone)}'"

    CONTACT_DICT.add_record(Record(Name(contact_name), Phone(phone)))

    return f"{get_formated_contact(contact_name, phone)} - added to contacts"


@input_error
def remove_phone(*args):
    input_params = args[0]
    params_list = input_params.split(",")
    if len(params_list) < 1:
        return f"Inputted not correctly data: {input_params}! Phone or number absent!"
    elif len(params_list) > 2:
        return f"Inputted not correctly data: {input_params}: to mach parameters!"

    contact_name = params_list[0].strip().title()

    record_exist: Record = CONTACT_DICT.get(contact_name)

    if record_exist:

        phones_params = params_list[1].strip().split(" ")

        phone_ = phones_params[0]

        for ch in phone_:
            if not ch.isdigit():
                return f"Inputted not correctly data: {old_phone}: must consist only digits!"

        return record_exist.remove_phone(phone_)

    else:
        return f"{contact_name} - no such contact"


@input_error
def change(*args):
    input_params = args[0]
    params_list = input_params.split(",")
    if len(params_list) < 2:
        return f"Inputted not correctly data: {input_params}! Phone or number absent!"
    elif len(params_list) > 3:
        return f"Inputted not correctly data: {input_params}: to mach parameters!"

    contact_name = params_list[0].strip().title()

    record_exist: Record = CONTACT_DICT.get(contact_name)

    if record_exist:

        phones_params = params_list[1].strip().split(" ")

        old_phone = Phone(phones_params[0])
        new_phone = Phone(params_list[2].strip().split(" ")[0])

        result = record_exist.change_phone(old_phone, new_phone)

        return result

    else:
        return f"{contact_name} - no such contact"


@input_error
def phone(*args):
    input_contact_name = args[0]

    result_list = []
    if input_contact_name:
        for contact_name, record in CONTACT_DICT.items():
            if input_contact_name.lower() in contact_name.lower():
                result_list.append(str(record))
    else:
        raise ValueError("Parameter 'contact name' is empty, try again or use 'help'")

    if result_list:
        return "\n".join(result_list)
    else:
        return f"There are no '{input_contact_name}' matches among contacts"


@input_error
def show_all(*args):
    records_count = args[0]
    if records_count:
        for i in CONTACT_DICT.iterator(int(records_count)):
            print(i)
    else:
        return CONTACT_DICT


@input_error
def exit(*args):
    return f"Work ended"

@input_error
def days_to_birthday(*args):
    input_contact_name = args[0]

    if input_contact_name:
        for contact_name, record in CONTACT_DICT.items():
            if input_contact_name.lower() in contact_name.lower():
                return record.days_to_birthday()

    else:
        raise ValueError("Parameter 'contact name' is empty, try again or use 'help'")

    if result_list:
        return "\n".join(result_list)
    else:
        return f"There are no '{input_contact_name}' matches among contacts"

def get_formated_contact(contact_name, phone):
    return f"{contact_name}: {phone}"

COMMANDS_LIST = {"hello": hello,
                 "help": help,
                 "add": add,
                 "change": change,
                 "del": remove_phone,
                 "phone": phone,
                 "show all": show_all,
                 "show": show_all,
                 "good bye": exit,
                 "exit": exit,
                 "bd": days_to_birthday}

CONTACT_DICT = AddressBook()

@input_error
def input_previosly_contacts():
    previous_contacts = {"Bob Marley": "0967845456",
                     "Borys Johnson": "0967845111",
                     "Lara Croft": "0967111456",
                     "Bred Pitt": "0961223456",
                     "Test": "123"}

    for k, v in previous_contacts.items():
        CONTACT_DICT.add_record(Record(Name(k), Phone(v), Birthday("2020.04.30")))


def main():

    input_previosly_contacts()

    while True:

        input_data = input("Input command (For help use command 'help'):")

        result = get_func_from_text(input_data)

        if result:
            command, data = result

            result_comand = command(data)

            if result_comand:
                print(result_comand)

            if command == exit:
                break


if __name__ == '__main__':
    main()
