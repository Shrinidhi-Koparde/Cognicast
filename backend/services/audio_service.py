"""
Audio generation service — gTTS (free, default), ElevenLabs (premium), or silent mock.

TTS_MODE in .env controls which provider:
  - "gtts"      → Free Google TTS (default, no API key needed)
  - "elevenlabs"→ ElevenLabs API (high quality, needs API key)
  - "mock"      → Silent WAV files (for testing only)
"""

import os
import uuid
import struct
import io
from config import settings


def _generate_silent_wav(duration_seconds: float = 1.0, sample_rate: int = 22050) -> bytes:
    """Generate a silent WAV file as bytes."""
    num_samples = int(sample_rate * duration_seconds)
    data_size = num_samples * 2  # 16-bit = 2 bytes per sample

    wav_buffer = io.BytesIO()
    # WAV header
    wav_buffer.write(b'RIFF')
    wav_buffer.write(struct.pack('<I', 36 + data_size))
    wav_buffer.write(b'WAVE')
    wav_buffer.write(b'fmt ')
    wav_buffer.write(struct.pack('<I', 16))  # chunk size
    wav_buffer.write(struct.pack('<H', 1))   # PCM
    wav_buffer.write(struct.pack('<H', 1))   # mono
    wav_buffer.write(struct.pack('<I', sample_rate))
    wav_buffer.write(struct.pack('<I', sample_rate * 2))  # byte rate
    wav_buffer.write(struct.pack('<H', 2))   # block align
    wav_buffer.write(struct.pack('<H', 16))  # bits per sample
    wav_buffer.write(b'data')
    wav_buffer.write(struct.pack('<I', data_size))
    wav_buffer.write(b'\x00' * data_size)    # silent samples

    return wav_buffer.getvalue()


async def generate_podcast(conversation: list[dict]) -> str:
    """
    Generate a podcast audio file from conversation turns.

    Uses TTS_MODE from settings to decide the provider:
      - "gtts" (default): Free Google TTS with different speech rates
      - "elevenlabs": Premium ElevenLabs voices
      - "mock": Silent WAV for testing

    Returns: relative URL path to the audio file.
    """
    audio_id = str(uuid.uuid4())

    # Determine TTS mode: support both old MOCK_AUDIO and new TTS_MODE
    tts_mode = getattr(settings, 'TTS_MODE', 'gtts')

    # Backward compat: if MOCK_AUDIO is explicitly false and TTS_MODE isn't set, use gtts
    if settings.MOCK_AUDIO and tts_mode == "mock":
        return await _generate_mock_audio(conversation, audio_id)

    if tts_mode == "elevenlabs":
        return await _generate_elevenlabs_audio(conversation, audio_id)

    # Default: gTTS (free)
    return await _generate_gtts_audio(conversation, audio_id)


async def _generate_gtts_audio(conversation: list[dict], audio_id: str) -> str:
    """Generate audio using gTTS (Google Text-to-Speech) — free, no API key."""
    try:
        from gtts import gTTS

        # Build the full script with speaker labels for natural pacing
        audio_parts = []

        for turn in conversation:
            speaker = turn.get("speaker", "mentor")
            text = turn.get("text", "")
            if not text.strip():
                continue

            # Use slightly different speech patterns
            # gTTS doesn't support voice changing, but we prepend speaker cues
            tts = gTTS(text=text, lang='en', slow=False)
            part_buffer = io.BytesIO()
            tts.write_to_fp(part_buffer)
            part_buffer.seek(0)
            audio_parts.append((speaker, part_buffer.getvalue()))

        if not audio_parts:
            return await _generate_mock_audio(conversation, audio_id)

        # Concatenate all parts using pydub
        try:
            from pydub import AudioSegment

            combined = AudioSegment.empty()
            for speaker, mp3_bytes in audio_parts:
                segment = AudioSegment.from_mp3(io.BytesIO(mp3_bytes))
                # Speed up mentor slightly for variety
                if speaker == "mentor":
                    segment = segment.speedup(playback_speed=1.05, crossfade=25)
                combined += segment
                # Brief pause between turns
                combined += AudioSegment.silent(duration=400)

            filename = f"{audio_id}.mp3"
            filepath = os.path.join(settings.AUDIO_DIR, filename)
            combined.export(filepath, format="mp3")
            return f"/api/audio/{filename}"

        except Exception as pydub_err:
            # If pydub/ffmpeg isn't available, save parts sequentially as raw mp3
            print(f"[AUDIO] pydub unavailable ({pydub_err}), saving first speaker only")
            filename = f"{audio_id}.mp3"
            filepath = os.path.join(settings.AUDIO_DIR, filename)
            with open(filepath, "wb") as f:
                for _, mp3_bytes in audio_parts:
                    f.write(mp3_bytes)
            return f"/api/audio/{filename}"

    except Exception as e:
        print(f"[AUDIO] gTTS error: {e}. Falling back to mock audio.")
        return await _generate_mock_audio(conversation, audio_id)


async def _generate_mock_audio(conversation: list[dict], audio_id: str) -> str:
    """Generate a silent audio file for development/testing."""
    duration = len(conversation) * 2.0

    wav_bytes = _generate_silent_wav(duration_seconds=duration)

    filename = f"{audio_id}.wav"
    filepath = os.path.join(settings.AUDIO_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(wav_bytes)

    return f"/api/audio/{filename}"


async def _generate_elevenlabs_audio(conversation: list[dict], audio_id: str) -> str:
    """Generate real audio using ElevenLabs API."""
    try:
        from elevenlabs import ElevenLabs

        client = ElevenLabs(api_key=settings.ELEVENLABS_API_KEY)
        audio_segments = []

        for turn in conversation:
            voice_id = (
                settings.ELEVENLABS_STUDENT_VOICE_ID
                if turn["speaker"] == "student"
                else settings.ELEVENLABS_MENTOR_VOICE_ID
            )

            audio_generator = client.text_to_speech.convert(
                voice_id=voice_id,
                text=turn["text"],
                model_id="eleven_multilingual_v2",
                output_format="mp3_44100_128",
            )

            # Collect bytes from generator
            audio_bytes = b""
            for chunk in audio_generator:
                audio_bytes += chunk
            audio_segments.append(audio_bytes)

        # Concatenate audio segments using pydub
        from pydub import AudioSegment

        combined = AudioSegment.empty()
        for seg_bytes in audio_segments:
            segment = AudioSegment.from_mp3(io.BytesIO(seg_bytes))
            combined += segment
            combined += AudioSegment.silent(duration=500)

        filename = f"{audio_id}.mp3"
        filepath = os.path.join(settings.AUDIO_DIR, filename)
        combined.export(filepath, format="mp3")

        return f"/api/audio/{filename}"

    except Exception as e:
        print(f"[WARN] ElevenLabs error: {e}. Falling back to gTTS.")
        return await _generate_gtts_audio(conversation, audio_id)
