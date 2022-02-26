#!/usr/bin/env python3

import addressbook_pb2


def main():
    print("Hello World!")

    person = addressbook_pb2.Person()
    person.id = 1234
    person.name = "John Doe"
    person.email = "jdoe@example.com"
    phone = person.phones.add()
    phone.number = "555-4321"
    phone.type = addressbook_pb2.Person.HOME

    print(person)


if __name__ == "__main__":
    main()
