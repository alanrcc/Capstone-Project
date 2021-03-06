import requests
import json

from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


# inputValue = 'crime movie with cool car chase and nice soundtrack'


def tmdb(inputValue):
    authenticator = IAMAuthenticator('Urysw6Zb3FD5CDASMUiyZEnmcctbDIuPpFUdyTCH3KrL')
    assistant = AssistantV2(
        version='2020-09-26',
        authenticator=authenticator
    )
    assistant.set_service_url('https://api.us-south.assistant.watson.cloud.ibm.com')
    ass_id = '2120d4b4-5d21-4880-981c-245436c7e12f'

    response = assistant.create_session(
        assistant_id=ass_id
    ).get_result()

    sess_id = response["session_id"]

    response = assistant.message(
        assistant_id=ass_id,
        session_id=sess_id,
        input={
            'message_type': 'text',
            'text': inputValue
        }
    ).get_result()

    ass_response = response["output"]["generic"][0]["text"]
    # response codes:
    # 1: will return movie
    # 2: no keywords found
    # 3: no genre/did not understand

    if ass_response == "2":
        response = assistant.delete_session(
            assistant_id=ass_id,
            session_id=sess_id
        ).get_result()
        return "Please include some keywords to narrow the search."
    elif ass_response == "3":
        response = assistant.delete_session(
            assistant_id=ass_id,
            session_id=sess_id
        ).get_result()
        return "You need a genre and some keywords to search."

    json_str = json.dumps(response, indent=2)
    # SIZE
    size = len(response["output"]["entities"])
    # print(size)
    # print(response["output"]["entities"])
    # GENRE
    genre = ""
    for word in response["output"]["entities"]:
        if word.get("entity") == "genre":
            genre = word.get("value")
            break
    # KEYWORD
    keywords = []
    i = 1
    for word in response["output"]["entities"]:
        if word.get("entity") == "keywords":
            keywords.append(word.get("value"))

    # TIME
    time = ""
    for word in response["output"]["entities"]:
        if word.get("entity") == "times":
            time = (word.get("value"))
            break

    response = assistant.delete_session(
        assistant_id=ass_id,
        session_id=sess_id
    ).get_result()

    class Tmdb:
        def __init__(self, key):
            self.key = key

        def searchMovieName(self, name):
            url = 'https://api.themoviedb.org/3/search/movie?api_key=' + self.key + '&query='
            if ' ' in name:
                name.replace(' ', '+')
            search = url + name
            return requests.get(search).json()

        def searchGenre(self, genre):
            url = 'https://api.themoviedb.org/3/genre/movie/list?api_key=' + self.key + '&query='
            # print("genre: '", genre, "'")
            if ' ' in genre:
                genre.replace(' ', '%20')
            genre = genre.capitalize()
            search = url + genre
            req = requests.get(search).json()
            i = 0
            id = 0
            while i < len(req["genres"]):
                if req["genres"][i].get("name") == genre:
                    id = req["genres"][i].get("id")
                i += 1
            return id

        # gets person name from tmdb using search func and return the json output
        def searchPerson(self, person):
            url = 'https://api.themoviedb.org/3/search/people?api_key=' + self.key + '&query='
            if ' ' in person:
                person.replace(' ', '%20')
            search = url + person
            return requests.get(search).json()

        def searchKeyword(self, keyword):
            url = 'https://api.themoviedb.org/3/search/keyword?api_key=' + self.key + '&query='
            if ' ' in keyword:
                keyword.replace(' ', '%20')
            search = url + keyword
            return requests.get(search).json()

        def parseTimes(self, movieList, time):
            list = []
            if movieList.get("total_results") != 0:
                list = movieList['results']
                temp = []
                while list:
                    mv = list.pop()
                    release = mv["release_date"][0:4]
                    if (((time == "new") and (int(release) > 2010)) or ((time == "old") and (int(release) < 1985)) or (
                            time == "")):
                        temp.append(mv)
                while temp:
                    list.append(temp.pop())
            return list

        def discover(self, genreID, keywordID):
            url = 'https://api.themoviedb.org/3/discover/movie?api_key=' + self.key + '&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1&with_genres='
            if ' ' in keywordID:
                keywordID.replace(' ', '%2C')
            search = url + genreID
            search = search + "&with_keywords=" + keywordID + "&without_keywords=9663"  # remove sequels
            return requests.get(search).json()

        def simpleSearch(self, genre, keyword):
            title = "NO MOVIE FOUND"
            keyWordID = ""
            genreID = ""
            personID = ""
            genreID += str(self.searchGenre(genre))
            for y in keyword:
                key = self.searchKeyword(y)
                res = key['results']
                id = 0
                for x in res:
                    # compare case insensitive
                    if x['name'].casefold() == y.casefold():
                        id = x['id']
                        # print("keyword: ", y)
                        # print("keywordID: ", id)
                        keyWordID += str(id) + ","

            movieList = self.discover(genreID, keyWordID)
            list = self.parseTimes(movieList, time)
            if movieList.get("total_results") != 0:
                if len(list) > 0:
                    title = list[0]['title']

            return title

    test = Tmdb("6ca5bdeac62d09b1186aa4b0fd678720")
    keyword = keywords
    output = test.simpleSearch(genre, keyword)
    return output
