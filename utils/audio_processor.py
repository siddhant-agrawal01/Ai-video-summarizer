
from pydub import AudioSegment
import yt_dlp
import os

# //saving audio to a directorty
DOWNLOAD_DIRECTORY='downloades'

os.makedirs(DOWNLOAD_DIRECTORY,exist_ok=True);


def download_youtube_audio(url:str)->str:
    output_path=os.path.join(DOWNLOAD_DIRECTORY,"%(title)s.%(ext)s")
    ydl_options={
        "format":"bestaudio/best",
        "outtmpl":output_path,
       "postprocessors":[
        {
            "key":"FFmpegExtractAudio",
            "preferredcodec":"wav",
            "preferredquality":"192",
        }
       ],
       "quiet":True,
    }
    with yt_dlp.YoutubeDL(ydl_options) as ydl:
        info=ydl.extract_info(url,download=True)
        filename=ydl.prepare_filename(info).replace(".webm",".wav").replace(".mp4",".wav")
    return filename
# //converting file to wav using pydub
if __name__ == "__main__":
    result = download_youtube_audio("https://www.youtube.com/shorts/0E2MogEpNx0")
    print(f"Downloaded to: {result}")