from pydub import AudioSegment


def wav2mp3(wav_file_path: str, mp3_file_path: str):
    audio = AudioSegment.from_wav(wav_file_path)

    # サンプルレートを11.025kHz、モノラルに設定
    audio = audio.set_frame_rate(11025)
    audio = audio.set_channels(1)

    # ビットレート32kbpsでMP3に変換
    audio.export(mp3_file_path, format="mp3", bitrate="32k")
