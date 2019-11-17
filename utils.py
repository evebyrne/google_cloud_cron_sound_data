import requests

import requests_toolbelt.adapters.appengine
requests_toolbelt.adapters.appengine.monkeypatch()

from firebase_admin import firestore
import uuid

def sendHttpRequest():
    print('sending http request')
    URL = "http://dublincitynoise.sonitussystems.com/applications/api/dublinnoisedata.php"
    r = requests.get(url = URL) 
    data = r.json()
    print('received response')

    all_data = zip(data['dates'], data['times'], data['aleq'])
    print(all_data)
    return all_data

def sendToFirebase(data):
    db = firestore.client()
    for item in data:
    
        doc_ref = db.collection(u'sonitus_data').document(str(uuid.uuid1()))
        doc_ref.set({
            u'date': item[0],
            u'time': item[1],
            u'aleq': item[2]
        })
