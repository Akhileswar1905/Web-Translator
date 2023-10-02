import firebase_admin
from firebase_admin import credentials
import pyrebase


def upload_audio_and_get_url(audio_file_path):
    # Initialize Firebase Admin SDK
    cred = credentials.Certificate("service.json")
    firebase_admin.initialize_app(cred)

    # Initialize Firebase Storage
    config = {
        "apiKey": "AIzaSyAK3cPC84orGvpj0r9f7b15FlKhnWmBayg",
        "authDomain": "tts-storage.firebaseapp.com",
        "databaseURL": "https://tts-storage-default-rtdb.firebaseio.com",
        "projectId": "tts-storage",
        "storageBucket": "tts-storage.appspot.com",
        "messagingSenderId": "419975917314",
        "appId": "1:419975917314:web:d348e59facd6be26afdc1b",
    }

    firebase = pyrebase.initialize_app(config)
    storage = firebase.storage()

    try:
        # Upload the audio file
        storage.child(f"{audio_file_path}").put(audio_file_path)

        # Get the public URL of the uploaded audio file
        file_url = storage.child(f"{audio_file_path}").get_url(None)
        return file_url
    except Exception as e:
        return str(e)


# Usage example
if __name__ == "__main__":
    audio_file_path = "audio/output.mp3"
    public_url = upload_audio_and_get_url(audio_file_path)
    print("Public URL:", public_url)
