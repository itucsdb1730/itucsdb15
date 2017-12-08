class Concert_area:
    def __init__(self):
        self.concert_area_id = -1
        self.address = ""
        self.capacity = 0
        self.name = ""

    def IsValid(self):
        if(self.name == ""):
            return "Concert area's name is required"

        if(self.address == ""):
            return "Concert area's address is required"

        if self.capacity <= 0:
            return "Capacity must be bigger than 0"

        return ""