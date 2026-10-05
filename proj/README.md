# Mokha / «فجر اليمن» news video — project (5 Oct 2026)

Final deliverable: `final/video_1080p_final.mp4` (14:44, 1080p25, H.264 + AAC, −15.1 LUFS / −2.8 dBTP).
GitHub rejects files over 100 MB, so the MP4 is committed as parts:

```bash
cat final/parts/video_1080p_final.mp4.part_* > final/video_1080p_final.mp4
sha256sum -c final/parts/video_1080p_final.mp4.sha256
```

Read `final/FINAL_REPORT.txt` for sources and accuracy notes, `final/EDL_shotlist_final.tsv` for the shot list.

## Layout
| folder | contents |
|---|---|
| `sources/audio/` | master narration (`audio_5_oct.mp3`, untouched) |
| `transcription/` | faster-whisper `small` transcript (segments + word timestamps) |
| `downloads/tg/` | Telegram clips (`tg_<channel>_<post>.mp4`) + channel scans (`scan_*.json`) |
| `downloads/cm/` | Wikimedia Commons archive stills + `meta.json` (licence/author/date) |
| `maps/` | animated maps (mp4) + Natural Earth subsets in `maps/data/` |
| `graphics/` | `common.py`, `maps.py` + `map_specs.py`, `cards.py`, `overlays.py`, `render.py`, fonts, cards, overlay PNGs |
| `temp/` | `edl_build.py` (scene plan) → `edl.json`, `render_log.tsv`, QC contact sheets, `mix.m4a` |
| `final/` | final video (parts), reports |

## Rebuild
```bash
pip install faster-whisper pillow numpy --break-system-packages
python3 graphics/maps.py                 # all maps (or name specific ones)
python3 graphics/cards.py                # cards + stat counters
python3 temp/edl_build.py                # -> temp/edl.json
python3 graphics/render.py               # all shots (or: render.py 12 40 77)
ls temp/segs/seg_*.mp4 | sort | sed "s|^|file '$PWD/|;s|$|'|" > temp/concat.txt
ffmpeg -f concat -safe 0 -i temp/concat.txt -c copy temp/video_only.mp4
# music bed (synthesized; regenerate with temp/make_music.sh), then mix:
ffmpeg -i sources/audio/audio_5_oct.mp3 -i sources/music/drone_bed.wav -filter_complex \
 "[0:a]aresample=48000,aformat=channel_layouts=stereo,asplit[v][sc];[1:a]volume=0.45[m];[m][sc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[md];[v][md]amix=inputs=2:normalize=0:duration=first,lowpass=f=16000,volume=3.4dB,alimiter=limit=0.7:level=false[a]" \
 -map "[a]" -c:a aac -b:a 256k -aac_coder twoloop temp/mix.m4a
ffmpeg -i temp/video_only.mp4 -i temp/mix.m4a -map 0:v -map 1:a -c copy -movflags +faststart final/video_1080p_final.mp4
```
