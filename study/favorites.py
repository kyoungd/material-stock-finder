import json


class JsonFavorite:
    def __init__(self, filename=None, userId=None, readJsonFile=True) -> None:
        filename = 'favorites.json' if filename == None else filename
        self.userId = userId
        self.filename = "./data/{}".format(
            filename) if userId == None else "../data/{}/{}".format(userId, filename)
        self.data = self.readJson() if readJsonFile else {}

    @property
    def GetJson(self):
        return self.data

    def readJson(self):
        with open(self.filename, "r") as openfile:
            data = json.load(openfile)
        return data

    def WriteJson(self, data=None):
        self.data = data if data != None else self.data
        with open(self.filename, "w") as outfile:
            json.dump(self.data, outfile)

    def EmptyJson(self):
        self.data = {}
        self.WriteJson()
