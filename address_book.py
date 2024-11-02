from collections import UserDict
from record import Record
from datetime import datetime, timedelta

class AddressBook(UserDict):
    """Адресна книга для зберігання та управління записами контактів."""

    def add_record(self, record: Record):
        """Додає запис до адресної книги."""
        if record.name.value in self.data:
            raise KeyError(f"Record with name '{record.name.value}' already exists.")
        self.data[record.name.value] = record

    def find(self, name: str):
        """Знаходить запис за іменем."""
        record = self.data.get(name)
        # if not record:
        #     raise KeyError(f"Record with name '{name}' not found.")
        # return record

    def delete(self, name: str):
        """Видаляє запис за іменем."""
        # if name not in self.data:
        #     raise KeyError(f"Record with name '{name}' not found.")
        del self.data[name]

    def get_upcoming_birthdays(self, days=7):
        """Повертає список контактів з днями народження протягом наступних 'days' днів."""
        today = datetime.today()
        upcoming_birthdays = []
        for record in self.data.values():
            if record.birthday:
                days_to_birthday = record.days_to_birthday()
                if days_to_birthday is not None and 0 <= days_to_birthday < days:
                    upcoming_birthdays.append(record)
        return upcoming_birthdays
