
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
# data= download_youtube_audio("https://www.youtube.com/shorts/0E2MogEpNx0")
# print(f"Downloaded to: {data}")


def convert_to_wav(input_path:str)->str:
    "converting any audio/video file to wav file using pydub"
    output_path=os.path.splitext(input_path)[0]+"_converted.wav"
    audio=AudioSegment.from_file(input_path)
    audio=audio.set_channels(1)
    audio=audio.set_frame_rate(16000)#16khz
    audio.export(output_path,format="wav")
    return output_path


# print(convert_to_wav(data))


# //creating chunks of audio

def chunk_audio(wav_path : str , chunk_minutes : int = 10) -> list:
    audio = AudioSegment.from_wav(wav_path)
    chunk_ms = chunk_minutes * 60 * 1000 

    chunks = []

    for i, start in enumerate(range(0,len(audio),chunk_ms)):
        chunk = audio[start : start + chunk_ms]
        chunk_path = f"{wav_path}_chunk_{i}.wav"
        chunk.export(chunk_path , format = "wav")

        chunks.append(chunk_path)
    
    return chunks

# //trigger function 
def process_input(source: str) -> list:
    if source.startswith("http://") or source.startswith("https://"):
        print("Detected YouTube URL. Downloading audio...")
        wav_path = download_youtube_audio(source)
    else:
        print("Detected local file. Converting to WAV...")
        wav_path = convert_to_wav(source)

    print("Chunking audio...")
    chunks = chunk_audio(wav_path)
    print(f"Audio ready — {len(chunks)} chunk(s) created.")
    return chunks