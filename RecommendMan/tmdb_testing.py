import requests
import json
import storage
import statelist

from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


###Return a list: the string to output, and the state
retpack = ["returnstmt", "statestring"]
def assistant(inputValue, storage):
    ###TMDB CLASS#########
    class Tmdb:
        def __init__(self,key):
            self.key = key

        def searchMovieName(self,name):
            url = 'https://api.themoviedb.org/3/search/movie?api_key=' + self.key + '&query='
            if ' ' in name:
                name.replace(' ','+')
            search = url+name
            return requests.get(search).json()

        def searchGenre(self,genre):
            url = 'https://api.themoviedb.org/3/genre/movie/list?api_key=' + self.key + '&query='
            #print("genre: '", genre, "'")
            if ' ' in genre:
                genre.replace(' ','%20')
            genre = genre.capitalize()
            search = url + genre
            req = requests.get(search).json()
            i = 0
            id = 0
            while i < len(req["genres"]):
                if req["genres"][i].get("name") == genre:
                    id = req["genres"][i].get("id")
                i+=1
            return id

        def searchKeyword(self,keyword):
            url = 'https://api.themoviedb.org/3/search/keyword?api_key=' + self.key + '&query='
            if ' ' in keyword:
                keyword.replace(' ','%20')
            search = url + keyword
            return requests.get(search).json()

        def parseTimes(self, movieList, time):
            list = []
            if (movieList.get("total_results")!=0):
                list = movieList['results']
                temp = []
                while list:
                    mv = list.pop()
                    release = mv["release_date"][0:4]
                    if (((time == "new") and (int(release) > 2010)) or ((time == "old") and (int(release) < 1985)) or (time == "")):
                            temp.append(mv)
                while temp:
                    list.append(temp.pop())
            return list
    
        def discover(self,genreID,keywordID):
            url = 'https://api.themoviedb.org/3/discover/movie?api_key=' + self.key + '&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1&with_genres='
            if ' ' in keywordID:
                keywordID.replace(' ','%2C')
            search = url + genreID
            search = search + "&with_keywords=" + keywordID
            return requests.get(search).json()

        def simpleSearch(self,genre,keyword):
            title="NO MOVIE FOUND"
            keyWordID = ""
            genreID=""
            genreID+=str(self.searchGenre(genre))
            for y in keyword:
                key = self.searchKeyword(y)
                res = key['results']
                id = 0
                for x in res:
                    #compare case insensitive
                    if x['name'].casefold() == y.casefold():
                        id = x['id']
                        #print("keyword: ", y)
                        #print("keywordID: ", id)
                        keyWordID += str(id) + ","

            movieList = self.discover(genreID,keyWordID)
            #print(movieList)
            list = self.parseTimes(movieList, time)
            if (movieList.get("total_results")!=0):
                if (len(list) > 0):
                    title = list[0]['title']
            return title
    ######################


    ###startup
    authenticator = IAMAuthenticator('Urysw6Zb3FD5CDASMUiyZEnmcctbDIuPpFUdyTCH3KrL')
    assistant = AssistantV2(
        version='2020-09-26',
        authenticator=authenticator
    )
    assistant.set_service_url('https://api.us-south.assistant.watson.cloud.ibm.com')
    ass_id = '2120d4b4-5d21-4880-981c-245436c7e12f'

    #print(response)
    startstate = statelist.startState()
    searchstate = '0'
    state = storage.getState()

    #likesActor = []
    #dislikesActor = []
    #likesGenre = []
    #dislikesGenre = []
    ###

    #if/else to see if startstate or not?

    response = assistant.message_stateless(
                assistant_id=ass_id,
                input={
                    'message_type': 'text',
                    'text': inputValue,
                    'options': {
                            'return_context': True
                    }
                },
                context={
                    'skills': {
                        'main skill': {
                            "system": {
                                    'state': state
                            }
                        }
                    }
                }
            ).get_result()
    
    output = response["output"]["generic"]
    print("OUTPUT[0][\"text\"]: ", output[0]["text"])

    if output[0]["text"] == "SEARCH":
        json_str = json.dumps(response, indent=2)
        #SIZE
        size = len(response["output"]["entities"])
        #print(response["output"]["entities"])
        #GENRE
        genre=""
        for word in response["output"]["entities"]:
            if word.get("entity")=="genre":
                    genre = word.get("value")
                    break
        #KEYWORD
        keywords = []
        for word in response["output"]["entities"]:
            if word.get("entity")=="keywords":
                    keywords.append(word.get("value"))
        #TIME
        time = ""
        for word in response["output"]["entities"]:
            if word.get("entity")=="times":
                    time = (word.get("value"))
                    break


        test = Tmdb("6ca5bdeac62d09b1186aa4b0fd678720")
        #print(test.simpleSearch(genre,keywords))
        state=statelist.searchState()
        #print("THIS IS THE HOME NODE")
        return([test.simpleSearch(genre,keywords) + "  " + "Search for another movie, get an example query, or return. ",state])
    else:
        state = response["context"]["skills"]["main skill"]["system"]["state"]
        if output[0]["text"] == "ACTORLIKE":
            for word in response["output"]["entities"]:
                if word.get("entity")=="actornames":
                    storage.addLikesActor(word["value"])
                    return ["You like "+word["value"]+"; tell me if you like/dislike another actor, type \"list\" to see a list of preferences, or \"return\" to go back." ,state]
        elif output[0]["text"] == "ACTORDISLIKE":
            for word in response["output"]["entities"]:
                if word.get("entity")=="actornames":
                    storage.addDislikesActor(word["value"])
                    return ["You dislike "+word["value"]+"; tell me if you like/dislike another actor, type \"list\" to see a list of preferences, or \"return\" to go back.",state]
        elif output[0]["text"] == "GENRELIKE":
            for word in response["output"]["entities"]:
                if word.get("entity")=="genre":
                    storage.addLikesGenre(word["value"])
                    return ["You like "+word["value"]+"; tell me if you like/dislike another genre, type \"list\" to see a list of preferences, or \"return\" to go back.",state]
        elif output[0]["text"] == "GENREDISLIKE":
            for word in response["output"]["entities"]:
                if word.get("entity")=="genre":
                    storage.addDislikesGenre(word["value"])
                    return ["You dislike "+word["value"]+"; tell me if you like/dislike another genre, type \"list\" to see a list of preferences, or \"return\" to go back.",state]
        elif output[0]["text"] == "ACTORLIST":
            likeslist = storage.getLikesActor()
            dislikeslist = storage.getDislikesActor()
            return [likeslist+"  "+dislikeslist + " Tell me the actor's/actresses' name and if you like/dislike them. Type \"return\" to go back, or \"list\" to see a list of your preferences.",state]
        elif output[0]["text"] == "GENRELIST":
            likeslist = storage.getLikesGenre()
            dislikeslist = storage.getDislikesGenre()
            return [likeslist+"  "+dislikeslist + " Tell me the actor's/actresses' name and if you like/dislike them. Type \"return\" to go back, or \"list\" to see a list of your preferences.",state]
        #elif output[0]["text"] == "RESET":
        #    storage.clearPrefs()
        #    return ["Preferences are reset. Are you looking for a movie recommendation, trying to update your movie preferences, or trying to learn more about Recommend-Man?", statelist.startState]
        elif output[0]["text"] == "GENREALL":
            #print("ACTION, ADVENTURE, COMEDY, CRIME")
            #print("DRAMA, FAMILY, FANTASY, HISTORY")
            #print("HORROR, MUSIC, MYSTERY, ROMANCE")
            #print("SCI-FI, THRILLER, WAR, WESTERN")
            return ["ACTION, ADVENTURE, COMEDY, CRIME, DRAMA, FAMILY, FANTASY, HISTORY, HORROR, MUSIC, MYSTERY, ROMANCE, SCI-FI, THRILLER, WAR, WESTERN; Do you want a list of genres, an example of keywords, or return?",state]
        else:
            #print(output)
            assmess = ""
            for resp in output:
                assmess = assmess + "  "+ resp["text"]
            retpack[0] = (assmess)
            retpack[1] = state
            #print (state)
            return retpack

    #usertext = input("YOUR INPUT HERE: ")
    #print(state)
