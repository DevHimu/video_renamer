import os
import shutil
import subprocess
import json
from pymediainfo import MediaInfo
import questionary
from rich.console import Console
from rich.table import Table

console = Console()

# -------------------------
# Load config.json
# -------------------------
CONFIG_FILE = "config.json"
with open(CONFIG_FILE, "r", encoding="utf-8") as f:
    cfg = json.load(f)

INPUT_FOLDER = cfg["input_folder"]
OUTPUT_FOLDER = cfg["output_folder"]
ADD_SRT = cfg["add_srt"]
CREDIT = cfg["credit"]
WIDTH_RES_MAP = cfg["width_resolution_map"]
VIDEO_CODEC_MAP = cfg["video_codec_map"]
AUDIO_CODEC_MAP = cfg["audio_codec_map"]

DEFAULT_SEASON = "01"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# -------------------------
# Utilities
# -------------------------
def get_media_info(file_path):
    mi = MediaInfo.parse(file_path)
    width = 0
    video_codec_id = "AVC"
    audio_codec_id = "AAC"
    audio_langs = []

    for track in mi.tracks:
        if track.track_type == "Video":
            width = track.width or 0
            video_codec_id = track.format or track.codec_id or "AVC"
        elif track.track_type == "Audio":
            audio_codec_id = track.format or track.codec_id or "AAC"
            if track.language:
                audio_langs.append(track.language.upper())
            else:
                audio_langs.append("UND")

    if not audio_langs:
        audio_langs = ["EN"]

    # Apply rules: single und = EN, multiple tracks = MULTI
    if len(audio_langs) == 1 and audio_langs[0] == "UND":
        audio_langs = ["EN"]
    elif len(audio_langs) > 1:
        audio_langs = ["MULTI"]

    resolution = WIDTH_RES_MAP.get(str(width), "Unknown")
    video_codec = VIDEO_CODEC_MAP.get(video_codec_id.upper(), video_codec_id.upper())
    audio_codec = AUDIO_CODEC_MAP.get(audio_codec_id.upper(), audio_codec_id.upper())

    return resolution, video_codec, audio_codec, audio_langs

# -------------------------
# Build new filename
# -------------------------
def build_new_name(mode, file, show_name, season, platform, episode_no, resolution, video_codec, audio_codec, audio_langs):
    lang_str = ".".join(audio_langs)
    base, ext = os.path.splitext(file)

    if mode == "Movie":
        parts = base.rsplit(".", 1)
        if len(parts) == 2:
            movie_name, year = parts
        else:
            movie_name, year = base, "0000"
        return f"{movie_name}.{year}.{resolution}.{platform}.WEB-DL.{lang_str}.{audio_codec}.{video_codec}-{CREDIT}{ext}"
    else:
        return f"{show_name}.S{season}E{episode_no}.{resolution}.{platform}.WEB-DL.{lang_str}.{audio_codec}.{video_codec}-{CREDIT}{ext}"

# -------------------------
# Attach SRT + tags using mkvmerge
# -------------------------
def attach_srt_and_tag(old_path, new_path, audio_langs):
    temp_path = new_path + ".tmp.mkv"
    cmd = ["mkvmerge", "-o", temp_path, old_path]

    if os.path.isfile(ADD_SRT):
        cmd += ["--language", "0:und", "--forced-track", "0:yes", ADD_SRT]

    # Overwrite all track names with CREDIT
    mi = MediaInfo.parse(old_path)
    for idx, track in enumerate(mi.tracks):
        if track.track_type in ("Video", "Audio", "Text"):
            cmd += ["--track-name", f"{idx}:{CREDIT}"]

    # Set main title as CREDIT
    cmd += ["--title", CREDIT]

    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if os.path.isfile(temp_path):
        shutil.move(temp_path, new_path)

# -------------------------
# Main
# -------------------------
def main():
    console.print("\n[bold cyan]====================================================[/bold cyan]")
    console.print("               [bold green]Renamer by HIMU[/bold green]")
    console.print("[bold cyan]====================================================[/bold cyan]\n")

    mode = questionary.select("Choose Mode:", choices=["Movie", "Series"]).ask()

    summary = []

    files = [f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith(".mkv")]
    files.sort()
    if not files:
        console.print("[yellow]No .mkv files found in input folder[/yellow]")
        return

    if mode == "Series":
        show_name = questionary.text("Enter Show Name:").ask()
        season_input = questionary.text(f"Enter Season Number (default={DEFAULT_SEASON}):").ask()
        season = (season_input.strip() or DEFAULT_SEASON).zfill(2)
        platform = questionary.text("Enter OTT Platform:").ask().upper()

        for file in files:
            old_path = os.path.join(INPUT_FOLDER, file)
            episode_no = os.path.splitext(file)[0]  # Use filename as episode number
            resolution, video_codec, audio_codec, audio_langs = get_media_info(old_path)
            new_name = build_new_name(mode, file, show_name, season, platform, episode_no, resolution, video_codec, audio_codec, audio_langs)
            new_path = os.path.join(OUTPUT_FOLDER, new_name)
            attach_srt_and_tag(old_path, new_path, audio_langs)
            summary.append((file, new_name, ",".join(audio_langs)))

    else:  # Movie
        platform = questionary.text("Enter OTT Platform:").ask().upper()
        for file in files:
            old_path = os.path.join(INPUT_FOLDER, file)
            resolution, video_codec, audio_codec, audio_langs = get_media_info(old_path)
            new_name = build_new_name(mode, file, "", "", platform, 0, resolution, video_codec, audio_codec, audio_langs)
            new_path = os.path.join(OUTPUT_FOLDER, new_name)
            attach_srt_and_tag(old_path, new_path, audio_langs)
            summary.append((file, new_name, ",".join(audio_langs)))

    # Display summary
    table = Table(title="Renaming Summary")
    table.add_column("Old Name", style="cyan")
    table.add_column("New Name", style="green")
    table.add_column("Languages", style="magenta")

    for old, new, langs in summary:
        table.add_row(old, new, langs)

    console.print(table)

    again = questionary.select("Do you want to rename more files?", choices=["Yes", "No"]).ask()
    if again == "Yes":
        main()
    else:
        console.print("\n[bold green]All tasks finished![/bold green]\n")


if __name__ == "__main__":
    main()
