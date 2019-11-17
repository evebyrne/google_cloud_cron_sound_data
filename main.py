# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_flex_quickstart]
import logging
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import Flask
import requests
import uuid

cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
    'projectId': 'sensor-app-2122f',
})

#import requests_toolbelt.adapters.appengine
app = Flask(__name__)

def sendHttpRequest():
 #   requests_toolbelt.adapters.appengine.monkeypatch()
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

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'

@app.route('/data')
def data():
    data = sendHttpRequest()
    sendToFirebase(data)

    return "Getting data"

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_flex_quickstart]
