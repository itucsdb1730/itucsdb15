class User:
    def __init__(self):
        self.userId = -1
        self.firstName = ""
        self.lastName = ""
        self.username = ""
        self.password = ""
        self.email = ""
        self.userType = 2


    def IsValid(self):
        if(self.firstName == ""):
            return "First name is required"

        if " " in self.firstName:
            return "First name cannot contain whitespace"

        if(self.lastName == ""):
            return "Last name is required"

        if " " in self.lastName:
            return "Last name cannot contain whitespace"

        if(self.username == ""):
            return "Username is required"

        if " " in self.username:
            return "Username cannot contain whitespace"

        if(self.email == ""):
            return "E-mail is required"

        if " " in self.email:
            return "E-mail cannot contain whitespace"

        return self.PasswordIsValid()


    def PasswordIsValid(self):
        if (self.password == ""):
            return "Password is required"

        if len(self.password) < 4:
            return "Password must be longer than 3 characters"

        if " " in self.password:
            return "Password cannot contain whitespace"

        return ""