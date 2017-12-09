class News:
    def __init__(self):
        self.newsId = -1
        self.title = ""
        self.content = ""
        self.imgUrl = "../static/images/defaultnews.ico"
        self.createdBy = -1
        self.createDate = ""
        self.updateDate = ""


    def IsValid(self):
        if(self.title == ""):
            return "News title is required"

        if(self.content == ""):
            return "News content is required"

        return ""