import os

from speech2text.src import GoogleDriveAPI, GoogleDriveAPIError


if __name__ == '__main__':
    scopes = ['drive.readonly']
    folder = 'audio'

    try:
        with GoogleDriveAPI(scopes=scopes) as api:
            files = api.get_all_audio()

            for audio in files:
                destination = os.path.join(folder, audio.name)
                if not os.path.exists(destination):
                    api.download_audio(audio, destination)

    except KeyboardInterrupt:
        print("Ctrl+C")