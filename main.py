from speech2text.src import GoogleDriveAPI, GoogleDriveAPIError


if __name__ == '__main__':
    scopes = ['drive.readonly']
    destination = 'audio'

    try:
        with GoogleDriveAPI(scopes=scopes) as api:
            files = api.get_all_audio()

            for audio in files:
                api.download_audio(audio, destination)

    except KeyboardInterrupt:
        print("Ctrl+C")