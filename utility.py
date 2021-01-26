import pyrebase
firebaseConfig = {'apiKey': "AIzaSyB1THVhS3Hc3-i7Gle9Hibtb77JiRGPkLI",
    'authDomain': "twitter-threader.firebaseapp.com",
    'projectId': "twitter-threader",
    'storageBucket': "twitter-threader.appspot.com",
    'messagingSenderId': "679885575729",
    'appId': "1:679885575729:web:9a5d8284a0ea32025b2710",
    'measurementId': "G-HB8TZSQB2F"}
firebase = pyrebase.initialize_app(firebaseConfig)