import requests
import os
import json

class connect() :
    # #headers = {
    #     'Accept': 'application/json',
    #     'Authorization': 'Bearer BQBGIbunMFlspzqvJoqH6kD6KNtQeChj8amRE7HWZAUVVMo2pCX9KpcKuq4yvZ7GqaLUIrTJH1xDLwaQBb3NP3mUuhtMqddA_jhGiBYQxxO1m2YODRqedqYmYYgaUVWpJFgsnkuAMvtl6LRGyMdpvFwtdYqYh8j47kNd3Bw4CA',
    # #}

    def __init__(self):
        self.headers=None
        self.owner_id=None

    
    def create_playlist(self): #1
        endpoint = "https://api.spotify.com/v1/users/" + self.get_current_user() + "/playlists"
        body = {
            'name': '2.0 MusicMe-' + self.get_current_user(),
            'description': 'dibuat hanya untuk Tugas Akhir. Feel free to delete setelah semuanya berakhir. :)'
        }
        body = json.dumps(body)
        header = self.headers
        header.update({'Content-Type': 'application/json'})
        r = requests.post(endpoint, headers=self.headers, data=body)
        content = json.loads(r.content)
        print(r.content)
        print(content['id'])
        return content['id']

    def add_track_to_playlist(self,playlist_id, id_uris):
        endpoint = "https://api.spotify.com/v1/users/" + self.get_current_user() + "/playlists/" + playlist_id + "/tracks"
        header = self.headers
        header.update({'Content-Type': 'application/json'})
        body = {"uris": id_uris}
        body = json.dumps(body)
        print("uris======")
        print(body)
        r = requests.post(endpoint, headers=header, data=body)
        print(r.content)

    def set_headers(self,id):
        self.headers={
        'Accept': 'application/json',
        'Authorization': 'Bearer '+str(id),
        }

    def get_tracks_from_album(self,id) :
        endpoint='https://api.spotify.com/v1/albums/'+id+'/tracks?'+'limit=50'
        r=requests.get(endpoint,headers=self.headers)
        return r.content

    def get_tracks_from_playlist(self,user,id,offset) :
        params = (
            ('market', 'ID'),
            ('limit', 50),
            ('offset', offset)
        )
        link =str('https://api.spotify.com/v1/users/'+user+'/playlists/'+id+'/tracks')
        print("link=",type(link))
        r = requests.get(link, headers=self.headers,params=params)
        #get track ids
        return r.content

    #mendapatkan informasi user khususnya id saja
    def get_current_user(self) :
        link = 'https://api.spotify.com/v1/me'
        r = requests.get(link, headers=self.headers)
        json_data=json.loads(r.content)
        print(r.content)
        return json_data['id']

    def get_display_name(self) :
        link = 'https://api.spotify.com/v1/me'
        r = requests.get(link, headers=self.headers)
        json_data=json.loads(r.content)
        print(r.content)
        return json_data['display_name']
    #mendapatkan playlist yang difollow user (dibuat oleh user juga termasuk)
    
    def get_current_user_playlist(self) :
        # teks = os.open('userPlaylists.json', os.O_RDWR | os.O_CREAT)
        link = 'https://api.spotify.com/v1/me/playlists?limit=50'
        r = requests.get(link, headers=self.headers)
        return r.content

    def get_several_audio_features(self, id) :
        link='https://api.spotify.com/v1/audio-features/?ids='+id
        r=requests.get(link,headers=self.headers)
        #print r.content
        return r.content

    def get_audio_features(self, id):
        link = 'https://api.spotify.com/v1/audio-features/' + id
        r = requests.get(link, headers=self.headers)
        # print r.content
        return r.content

    def get_audio_features(self,id) :
        path_element= (
            ('id',id)
        )
        link='https://api.spotify.com/v1/audio-features/'+id
        r=requests.get(link,headers=self.headers)
        return r.content

    def get_several_tracks(self,id) : #mendapatkan info track dari beberapa track_id
        link = 'https://api.spotify.com/v1/tracks?ids=' + id #maximum 50 IDs
        r = requests.get(link, headers=self.headers)
        return r.content

    def get_saved_tracks(self,offset) :
        params = (
            ('market', 'ID'),
            ('limit', 50),
            ('offset',offset)
        )
        r = requests.get('https://api.spotify.com/v1/me/tracks',params = params, headers=self.headers)
        return r.content


    def recommendation_based_seeds(self,id) :
        link = 'https://api.spotify.com/v1/recommendations?market=ID&seed_tracks=' + id + "&limit=3&min_popularity=40"
        r = requests.get(link, headers=self.headers)
        json_data = json.loads(r.content)
        return json_data
    #x=get_audio_features('4NPARrLIbtMl29ZJv8ESr2')
    # x=get_several_audio_features('4NPARrLIbtMl29ZJv8ESr2')
