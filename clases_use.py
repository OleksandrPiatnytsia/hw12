from collections import UserDict
from datetime import datetime, timedelta
from itertools import islice


class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    def __str__(self):
        return self.__value

    def __repr__(self):
        return str(self.__value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):

        if isinstance(self, Phone):
            for ch in value:
                if not ch.isdigit():
                    raise ValueError(f"Inputted not correctly phone: {value}: must consist only digits!")
        elif isinstance(self, Birthday):

            list_birthday_parts = [int(i.strip()) for i in value.split(".")]

            if len(list_birthday_parts) != 3:
                raise ValueError(f"Inputted date of birth: {value}: non correct! Use format year.month.day")

            datetime_b = datetime(list_birthday_parts[0], list_birthday_parts[1], list_birthday_parts[2])

            if datetime_b.date() >= datetime.today().date():
                raise ValueError(f"Inputted date of birth: {value}: non correct!")

        self.__value = value


class Name(Field):
    pass


class Phone(Field):

    def change_phone(self, new_phone):
        self.value = new_phone.value

    def __eq__(self, other):
        return self.value == other.value


class Birthday(Field):
    pass


class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None):
        self.name = name
        self.phones = []
        self.birthday = birthday

        if phone:
            if not isinstance(phone, Phone):
                raise ValueError("Phone must be class Phone")

            self.phones.append(phone)

    def __str__(self):
        return f"{self.name}: {', '.join([str(i) for i in self.phones])} {': ' + str(self.birthday) if self.birthday else ''}"

    def __repr__(self):
        return f"{self.name}: {', '.join([str(i) for i in self.phones])} {': ' + str(self.birthday) if self.birthday else ''}"

    def add_phone(self, phone: Phone):

        if phone and isinstance(phone, Phone):
            for exist_phone in self.phones:
                if exist_phone.value == phone.value:
                    raise ValueError(f"Phone {phone} already exist!")

            self.phones.append(phone)
        else:
            raise ValueError(f"Phone must be class Phone")

    def remove_phone(self, phone: str):

        if phone:
            for exist_phone in self.phones:
                if exist_phone.value == phone:
                    self.phones.remove(exist_phone)
                    return f"Phone {phone} removed!"

    def change_phone(self, old_phone: Phone, new_phone: Phone):

        if old_phone == new_phone:
            return f"The phones are the same"

        phone_changed = False
        for exist_phone in self.phones:
            if exist_phone.value == old_phone.value:
                exist_phone.change_phone(new_phone)
                phone_changed = True

        if phone_changed:
            return f"Phone {old_phone} is changed"
        else:
            return f"Phone {old_phone} cant be changed! reason: phone exist!"

    def add_birthday(self, birthday):
        self.birthday = birthday
        return f"Birthday {birthday} added to {self}"

    def days_to_birthday(self):

        if self.birthday:

            tooday = datetime.today().date()

            birthday_str = self.birthday.value

            list_b_data = birthday_str.split(".")

            datetime_birth = datetime(int(list_b_data[0]), int(list_b_data[1]), int(list_b_data[2])).date()

            year = tooday.year

            if datetime_birth.month == tooday.month and datetime_birth.day == tooday.day:
                return f"Day to next birthday: 0"

            elif datetime_birth.month < tooday.month:
                year += 1
            elif datetime_birth.month == tooday.month and datetime_birth.day < tooday.day:
                year += 1

            difference_dates: timedelta = datetime(year, datetime_birth.month, datetime_birth.day).date() - tooday

            return f"Contact: {self} Day to next birthday: {difference_dates.days + 1}"
        else:
            return f"{self} birthday is empty!"


class AddressBook(UserDict):

    def add_record(self, record: Record):
        self.data[record.name.value] = record
        # return f"{self} added to adres book!"

    def iterator(self, records_count=3):
        start_iterate = 0
        while True:
            if start_iterate >= len(self.data):
                break
            yield list(self.data.values())[start_iterate: start_iterate + records_count]
            start_iterate += records_count

    def __str__(self):
        return ";\n".join([f"{k}: {v}" for k, v in self.data.items()])


if __name__ == '__main__':
    book = AddressBook()

    record1 = Record(Name("Тест1"), Phone("0960969696"))
    print(record1.days_to_birthday())

    # record1.add_phone(Phone("987865421"))
    # print("record1: ", record1)
    #
    # record1.remove_phone("0960969696")
    # print("record1: ", record1)

    # record1.change_phone(Phone("0960969696"), "0960969696")
    #
    # print("record1: ", record1)
    #
    # book.add_record(record1)
    #
    # record2 = Record(Name("Тест2"), Phone("987865421"))
    #
    # book.add_record(record2)
    #
    # print("AddressBook: ", book)
