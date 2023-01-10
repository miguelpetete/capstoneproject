class Person:
    def __init__(self, name, first_surname, second_surname, username):
        self.name = name
        self.first_surname = first_surname
        self.second_surname = second_surname
        self.username = username

    def get_full_name(self):
        return f"{self.name} {self.first_surname} {self.second_surname}"

    def get_username(self):
        return f"{self.username}"


class Recruiter(Person):
    pass


class Candidate(Person):
    pass
