# Lightweight YouTube Download Tool

A lightweight terminal-based YouTube download tool with optional flags to open the file explorer after downloading, play the video, and more.

## Features

- **Download YouTube videos** directly from the terminal.
- **Specify output file name** as a second argument.
- **Download to the system's Downloads folder** with the `-d` flag.
- **Open the file explorer** after downloading with the `-o` flag.
- **Play the video immediately** after downloading with the `-p` flag.
- Choose video **quality** (`best` or `worst`) with the `-q` flag.
- Specify video **format** (e.g., `mp4`, `mp3`) with the `-f` flag.

## Requirements

- **Python 3.x**
- **yt-dlp package**

## Installation

1. **Clone or download this repository**.

2. **Install Dependencies**:
    pip install -r requirements.txt
    Alternatively, install yt-dlp directly:
    pip install yt-dlp

## Usage

python youtube_downloader.py [options] <YouTube_URL> [output_file_name]

Or make the script executable (Unix/Linux):

chmod +x youtube_downloader.py
./youtube_downloader.py [options] <YouTube_URL> [output_file_name]

## Options

- `-d`, `--downloads`: Download to the system's Downloads folder.
- `-o`, `--open`: Open the file explorer after downloading.
- `-p`, `--play`: Play the video immediately after downloading.
- `-q`, `--quality`: Choose the video quality to download (`best` or `worst`). Defaults to `best`.
- `-f`, `--format`: Specify the video format (e.g., `mp4`, `webm`, `mp3`).
- `-h`, `--help`: Show help message and exit.
- `--list-formats`: List all available formats for the given URL, then exit.
- `--subtitles`: Download subtitles for the video.
- `--sub-lang`: Comma-separated subtitle languages (default: en) to use when downloading subtitles.
- `--cookies`: Path to a cookies file (e.g., cookies.txt).
- `--max-downloads`: Maximum number of videos to download (useful for playlists).

## Examples

1. Download a video with default file name and format:
   python youtube_downloader.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

2. Download a video with a specified output file name:
   python youtube_downloader.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" myvideo.mp4

3. Download to the Downloads folder with a specified file name:
   python youtube_downloader.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" myvideo.mp4 -d

4. Attempt to download to a subdirectory in Downloads (will raise an error):
   python youtube_downloader.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" folder/subfolder/myvideo.mp4 -d
   Error: Cannot combine a custom output path with the '-d' flag.
   Remove the path from the output file name or do not use the '-d' flag.

5. Download a video to a specific directory specified in the output file name:
   python youtube_downloader.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" folder/subfolder/myvideo.mp4

6. Download a video with a specified format, warning if extension doesn't match:
   python youtube_downloader.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" myvideo.webm -f mp4
   Warning: The file extension of 'myvideo.webm' does not match the specified format 'mp4'. Proceeding anyway.

7. Download and play the video after downloading:
   python youtube_downloader.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -p

8. List all available formats for a URL (no download):
   python youtube_downloader.py --list-formats "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

9. Download subtitles (default: English) along with the video:
   python youtube_downloader.py --subtitles "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

10. Download subtitles in multiple languages:
   python youtube_downloader.py --subtitles --sub-lang "en,es" "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

11. Use a cookies file:
   python youtube_downloader.py --cookies /path/to/cookies.txt "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

12. Limit total downloads to 1 (useful for playlists):
   python youtube_downloader.py --max-downloads 1 "https://www.youtube.com/watch?v=PLAYLIST_LINK"

## Notes

- **Downloads Folder Detection**: The script automatically detects the Downloads folder across Windows, macOS, and Linux.
- **Output File Name and Paths**:
  - If the `-d` flag is used to download to the Downloads folder, and the output file name includes a path (e.g., `folder/subfolder/myvideo.mp4`), the script raises an error.
  - If only a file name is provided (without a path), it is saved in the Downloads folder when `-d` is used.
  - If a custom path is included in the output file name, do not use the `-d` flag.
- **File Extension Checks**:
  - The script warns if the file extension of the output file name doesn't match the specified or default format but proceeds with the download.
- **Dependencies**: Install the yt-dlp package using pip install yt-dlp.
- **Respect YouTube's Terms of Service**: Be mindful of YouTube's policies regarding content downloading.