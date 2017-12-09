class News:
    def __init__(self):
        self.newsId = -1
        self.title = ""
        self.musicianId = -1
        self.content = ""
        self.imgUrl = "../static/images/defaultnews.ico"
        self.createdBy = -1
        self.createDate = ""
        self.updateDate = ""


    def IsValid(self):
        if(self.title == ""):
            return "News title is required"

        if(self.musicianId == -1):
            return "Musician is not found in our database. Please provide an existing musician"

        if(self.content == ""):
            return "News content is required"

        return ""