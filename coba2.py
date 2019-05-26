import csv
import RevuserConnect
import json

def __list_to_str(list) :
    abc=""
    size=len(list)
    count=1
    for i in list :
        abc=abc+i
        if count<size :
            abc=abc+','
        count = count + 1
    return abc

conn=RevuserConnect.connect()
strings=str("BQCAyG8228Ve7qmzPDwSVC7KCW7_H_rLwIbrdiPjU5Lftvla2ovKCNF8P-9qvnqXQnSO20jg7lgk23CwIRbziF00LuyGCLDJg4vQJPLbcn1liWJrH8zXFGztvaZm4B93kXXa4nVF7wLRuScK8s9BU8VqJZrlf21HsayLpwt0mW1-KViIOqxQ8VT0UMupKNas1Mb7sJflvnNanj9LUrDiKOkGg16oVSkAcTmED5ig87OBlBO1Ig")
conn.set_headers(strings)

result=conn.get_current_user_playlist()
result=json.loads(result)
print(result)
for i in result['items'] :
	if(i['name']=="Discover Weekly") : dscvrWkly=i['id'];print("discover weekly=",dscvrWkly)

offset=0
list_id=list()
username="Spotify"
print("username",username)
tracks=json.loads(conn.get_tracks_from_playlist(username,dscvrWkly,offset))
print(tracks)
for j in tracks['items']:
    list_id.append(j['track']['id'])

print("============================")
for i in (json.loads(conn.get_several_tracks(__list_to_str(list_id))))['tracks'] :
    print(i['name'])
#get the discover weekly

