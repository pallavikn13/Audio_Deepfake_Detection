<<<<<<< HEAD
from mutagen import File

def analyze_metadata(audio_path):
    try:
        audio = File(audio_path)

        # If metadata can't be read
        if audio is None or not hasattr(audio, "info"):
            return 70   # neutral score

        score = 100

        # Safely check bitrate
        if hasattr(audio.info, "bitrate") and audio.info.bitrate:
            if audio.info.bitrate < 64000:
                score -= 30

        # Safely check sample rate
        if hasattr(audio.info, "sample_rate") and audio.info.sample_rate:
            if audio.info.sample_rate < 16000:
                score -= 30

        return max(score, 50)

    except Exception:
        # If metadata crashes (encoding issue, blob issue, etc.)
=======
from mutagen import File

def analyze_metadata(audio_path):
    try:
        audio = File(audio_path)

        # If metadata can't be read
        if audio is None or not hasattr(audio, "info"):
            return 70   # neutral score

        score = 100

        # Safely check bitrate
        if hasattr(audio.info, "bitrate") and audio.info.bitrate:
            if audio.info.bitrate < 64000:
                score -= 30

        # Safely check sample rate
        if hasattr(audio.info, "sample_rate") and audio.info.sample_rate:
            if audio.info.sample_rate < 16000:
                score -= 30

        return max(score, 50)

    except Exception:
        # If metadata crashes (encoding issue, blob issue, etc.)
>>>>>>> ff7d1f8aeb76fd3585a1b833f713ba1743e2d869
        return 70   # return neutral safe value