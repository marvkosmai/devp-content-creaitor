from SubtitleToStorage import SubtitlesToStorage


def main():
    downloader = SubtitlesToStorage(
        source='youtube',
        video_id='mzAfich6mow',
        storage_config={'type': 'file'}
    )

    downloader.save()


if __name__ == "__main__":
    main()
