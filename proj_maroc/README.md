# Morocco / Spain — IRIFI, F-16 Block 72, Marrakech Air Show 2026 (video project)

- Final 1080p master: `final/video_1080p_final.mp4` (Git LFS) — direct download:
  https://media.githubusercontent.com/media/omaridabd/mycloud/claude/clever-turing-p1h7a3/proj_maroc/final/video_1080p_final.mp4
- 720p preview (plays on GitHub): `final/preview_720p.mp4`
- Reports: `final/FINAL_REPORT.txt`, `final/EDL_shotlist_final.tsv`, `final/QC_motion_report_final.txt`

## Add the expert's name (part 2)
1. Edit `graphics/project_cfg.py` → `EXPERT_NAME`, `EXPERT_ROLE`
2. `python3 graphics/cards_maroc.py`
3. `python3 graphics/render.py $(python3 -c "import json;print(' '.join(str(e['i']) for e in json.load(open('temp/edl.json')) if e['t0']>=283))")`
4. concat + mux:
```bash
ls temp/segs/seg_*.mp4 | sort | sed "s|^|file '$PWD/|;s|$|'|" > temp/concat.txt
ffmpeg -f concat -safe 0 -i temp/concat.txt -c copy temp/video_only.mp4
ffmpeg -i temp/video_only.mp4 -i temp/mix.m4a -map 0:v -map 1:a -c copy -movflags +faststart final/video_1080p_final.mp4
```
(`temp/mix.m4a` is committed; regenerate the music with `temp/make_music.sh` if needed.)

## Rebuild from scratch
`python3 graphics/maps.py` · `python3 graphics/cards_maroc.py` · `python3 temp/edl_build.py` · `python3 graphics/render.py`
