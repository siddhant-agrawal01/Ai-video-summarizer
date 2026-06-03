These steps are usually done because raw audio files come in many different formats, and speech-to-text models like Whisper work best when the audio is standardized.

## 1. Audio Normalization (Stereo → Mono)

### The Problem

Many recordings are stored in **stereo**, meaning they have **two channels**:

* Left channel (L)
* Right channel (R)

Example:

| Time  | Left Ear | Right Ear        |
| ----- | -------- | ---------------- |
| 1 sec | Voice    | Voice            |
| 2 sec | Voice    | Background Noise |

A transcription model doesn't need separate left and right channels because it only cares about the speech content.

Sometimes:

* The speaker's voice may be louder in one channel.
* One channel may contain more noise.
* Some recordings may have speech only on one side.

### The Solution

Convert stereo audio into **mono** (single channel).

Instead of:

```
Left  -> Voice
Right -> Voice
```

You get:

```
Mono -> Combined Voice
```

This:

* Reduces file size
* Simplifies processing
* Prevents channel imbalance issues
* Gives Whisper a single clean audio stream

### Analogy

Imagine two people are reading the same book to you through separate earbuds. For transcription, you only need one clear reading, not two copies.

---

## 2. Resampling to 16 kHz

### The Problem

Different audio files are recorded at different sample rates:

| Sample Rate | Common Usage      |
| ----------- | ----------------- |
| 8 kHz       | Phone calls       |
| 16 kHz      | Speech processing |
| 44.1 kHz    | Music CDs         |
| 48 kHz      | Video recordings  |

The sample rate determines how many times per second audio is measured.

Example:

```
16 kHz = 16,000 samples/sec
44.1 kHz = 44,100 samples/sec
```

### Why Whisper Prefers 16 kHz

Human speech mostly contains useful information below about 8 kHz.

According to the Nyquist principle:

f_{max}=\frac{f_s}{2}

For a 16 kHz sample rate:

```
Maximum representable frequency
= 16,000 / 2
= 8,000 Hz
```

This comfortably covers the frequencies important for human speech.

### What Happens Without Resampling?

Suppose you have:

```
Audio A → 48 kHz
Audio B → 44.1 kHz
Audio C → 8 kHz
```

Whisper would first need to convert them internally to a consistent format.

By resampling beforehand:

```
48 kHz  ─┐
44.1 kHz ├─> 16 kHz
8 kHz   ─┘
```

every file reaches the model in the format it expects.

### Benefits

* Faster processing
* Less memory usage
* Consistent input quality
* No unnecessary high-frequency data

---

## Example

Original file:

```
Channels: Stereo (2)
Sample Rate: 48,000 Hz
Duration: 10 min
```

After preprocessing:

```
Channels: Mono (1)
Sample Rate: 16,000 Hz
Duration: 10 min
```

The speech content remains almost identical, but the audio is now optimized for transcription.

### FFmpeg Command

A common command used before sending audio to Whisper is:

```bash
ffmpeg -i input.mp3 -ac 1 -ar 16000 output.wav
```

Where:

* `-ac 1` → convert to mono
* `-ar 16000` → resample to 16 kHz

This produces audio in the format Whisper is designed to handle most efficiently.
