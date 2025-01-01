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

    ```bash
    pip install -r requirements.txt
    ```

    Alternatively, install `yt-dlp` directly:

    ```bash
    pip install yt-dlp
    ```

## Usage

```bash
python youtube_downloader.py [options] <YouTube_URL> [output_file_name]
```

Or make the script executable (Unix/Linux):

```bash
chmod +x youtube_downloader.py
./youtube_downloader.py [options] <YouTube_URL> [output_file_name]
```

## Options

- `-d`, `--downloads`: Download to the system's Downloads folder.
- `-o`, `--open`: Open the file explorer after downloading.
- `-p`, `--play`: Play the video immediately after downloading.
- `-q`, `--quality`: Choose the video quality to download (`best` or `worst`). Defaults to `best`.
- `-f`, `--format`: Specify the video format (e.g., `mp4`, `webm`, `mp3`).
- `-h`, `--help`: Show help message and exit.

## Examples

1. **Download a video with default file name and format**:

    ```bash
    python youtube_downloader.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    ```

2. **Download a video with a specified output file name**:

    ```bash
    python youtube_downloader.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" myvideo.mp4
    ```

3. **Download to the Downloads folder with a specified file name**:

    ```bash
    python youtube_downloader.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" myvideo.mp4 -d
    ```

4. **Attempt to download to a subdirectory in Downloads (will raise an error)**:

    ```bash
    python youtube_downloader.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" folder/subfolder/myvideo.mp4 -d
    ```

    Output:

    ```
    Error: Cannot combine a custom output path with the '-d' flag.
    Remove the path from the output file name or do not use the '-d' flag.
    ```

5. **Download a video to a specific directory specified in the output file name**:

    ```bash
    python youtube_downloader.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" folder/subfolder/myvideo.mp4
    ```

6. **Download a video with a specified format, warning if extension doesn't match**:

    ```bash
    python youtube_downloader.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" myvideo.webm -f mp4
    ```

    Output:

    ```
    Warning: The file extension of 'myvideo.webm' does not match the specified format 'mp4'. Proceeding anyway.
    ```

7. **Download and play the video after downloading**:

    ```bash
    python youtube_downloader.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -p
    ```

## Notes

- **Downloads Folder Detection**: The script automatically detects the Downloads folder across Windows, macOS, and Linux.

- **Output File Name and Paths**:

    - If the `-d` flag is used to download to the Downloads folder, and the output file name includes a path (e.g., `folder/subfolder/myvideo.mp4`), the script raises an error.

    - If only a file name is provided (without a path), it is saved in the Downloads folder when `-d` is used.

    - If a custom path is included in the output file name, do not use the `-d` flag.

- **File Extension Checks**:

    - The script warns if the file extension of the output file name doesn't match the specified or default format but proceeds with the download.

- **Dependencies**: Install the `yt-dlp` package using `pip install yt-dlp`.

- **Respect YouTube's Terms of Service**: Be mindful of YouTube's policies regarding content downloading.
