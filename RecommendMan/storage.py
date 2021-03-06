class Storage:

    def __init__(self):
        self.state = 'eyJzZXNzaW9uX2lkIjoiNjc3OGFmYzUtNjExYi00ODQzLWIxMTgtMWRjNjMzZWZiMDg3Iiwic2tpbGxfcmVmZXJlbmNlIjoibWFpbiBza2lsbCIsImFzc2lzdGFudF9pZCI6IjIxMjBkNGI0LTVkMjEtNDg4MC05ODFjLTI0NTQzNmM3ZTEyZiIsImluaXRpYWxpemVkIjp0cnVlLCJkaWFsb2dfc3RhY2siOlt7ImRpYWxvZ19ub2RlIjoiV2VsY29tZSJ9XSwiX25vZGVfb3V0cHV0X21hcCI6eyJXZWxjb21lIjp7IjAiOlswLDBdfX0sImxhc3RfYnJhbmNoX25vZGUiOiJXZWxjb21lIn0='
        self.girlstate = 'eyJzZXNzaW9uX2lkIjoiZDZjODRjZWMtZDBkZi00MGFiLThhNWUtYjY0ZjU1NWQ5MTA5Iiwic2tpbGxfcmVmZXJlbmNlIjoibWFpbiBza2lsbCIsImFzc2lzdGFudF9pZCI6IjIxMjBkNGI0LTVkMjEtNDg4MC05ODFjLTI0NTQzNmM3ZTEyZiIsImluaXRpYWxpemVkIjp0cnVlLCJkaWFsb2dfc3RhY2siOlt7ImRpYWxvZ19ub2RlIjoicm9vdCJ9XX0='
        self.title = ""
        self.history = []
        self.chosenMovie = ''
        self.likesActor = []
        self.dislikesActor = []
        self.likesGenre = []
        self.dislikesGenre =[]
        self.recommends = []
        self.current = ""

    def update(self, st):
            self.state = st

    def getState(self): 
            return self.state

    def getGirlState(self): 
        return self.girlstate
    

    def updateRecommends(self, recList):
        self.recommends = recList
    def getRecommends(self):
        return self.recommends
    def popRecommends(self):
        self.recommends.pop(0)

    def addHistory(self, movie):
        self.history.append(movie)
            
    def getHistory(self):
        return self.history
    def setChosenMovie(self, title):
        self.chosenMovie = title
    def getChosenMovie(self):
        return self.chosenMovie


    def addLikesActor(self, actor):
        if (actor not in self.likesActor):
            self.likesActor.append(actor)
        if (actor in self.dislikesActor):
            self.dislikesActor.remove(actor)
        print(self.likesActor)

    def printLikesActor(self):
        list = "Likes: "
        for name in self.likesActor:
           list = list +" "+ name
           print
        return list

    def getLikesActor(self):
        return self.likesActor

    def addDislikesActor(self, actor):
        if (actor not in self.dislikesActor):
            self.dislikesActor.append(actor)
        if (actor in self.likesActor):
            self.likesActor.remove(actor)

    def printDislikesActor(self):
        list = "Dislikes: "
        for name in self.dislikesActor:
           list = list +" "+ name
        return list

    def getDislikesActor(self):
        return self.dislikesActor

    def addLikesGenre(self, genre):
        if (genre not in self.likesGenre):
            self.likesGenre.append(genre)
        if (genre in self.dislikesGenre):
            self.dislikesGenre.remove(genre)

    def printLikesGenre(self):
        list = "Likes: "
        for name in self.likesGenre:
           list = list +" "+ name
        return list

    def getLikesGenre(self):
        return self.likesGenre

    def addDislikesGenre(self, genre):
        if (genre not in self.dislikesGenre):
            self.dislikesGenre.append(genre)
        if (genre in self.likesGenre):
            self.likesGenre.remove(genre)

    def printDislikesGenre(self):
        list = "Dislikes: "
        for name in self.dislikesGenre:
           list = list +" "+ name
        return list

    def getDislikesGenre(self):
        return self.dislikesGenre

    def clearPrefs(self):
        self.likesActor.clear()
        self.dislikesActor.clear()
        self.likesGenre.clear()
        self.dislikesGenre.clear()