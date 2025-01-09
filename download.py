#!/usr/bin/env python3
import sys
import os
import subprocess
import argparse
from yt_dlp import YoutubeDL

def get_downloads_folder():
    """Get the path to the user's Downloads folder."""
    if sys.platform == 'win32':
        from ctypes import windll, wintypes, byref
        import ctypes
        class GUID(ctypes.Structure):
            _fields_ = [
                ('Data1', wintypes.DWORD),
                ('Data2', wintypes.WORD),
                ('Data3', wintypes.WORD),
                ('Data4', wintypes.BYTE * 8)
            ]
        SHGetKnownFolderPath = windll.shell32.SHGetKnownFolderPath
        SHGetKnownFolderPath.argtypes = [
            ctypes.POINTER(GUID), wintypes.DWORD, wintypes.HANDLE,
            ctypes.POINTER(ctypes.c_wchar_p)
        ]
        FOLDERID_Downloads = GUID(
            0x374DE290, 0x123F, 0x4565,
            (wintypes.BYTE * 8)(0x91, 0x64, 0x39, 0xC4, 0x92, 0x5E, 0x46, 0x7B)
        )
        KF_FLAG_DEFAULT = 0
        path_ptr = ctypes.c_wchar_p()
        result = SHGetKnownFolderPath(
            byref(FOLDERID_Downloads), KF_FLAG_DEFAULT, None, byref(path_ptr)
        )
        if result != 0:
            raise ctypes.WinError(result)
        downloads = path_ptr.value
        windll.ole32.CoTaskMemFree(path_ptr)
        return downloads
    else:
        # For macOS and Linux
        downloads = os.path.join(os.path.expanduser('~'), 'Downloads')
        if os.path.exists(downloads):
            return downloads
    return None

def open_file_explorer(path):
    """Open the file explorer at the specified path."""
    if sys.platform == 'win32':
        os.startfile(path)
    elif sys.platform == 'darwin':
        subprocess.run(['open', path])
    else:
        subprocess.run(['xdg-open', path])

def play_media(file_path):
    """Play the video or audio file using the default media player."""
    if sys.platform == 'win32':
        os.startfile(file_path)
    elif sys.platform == 'darwin':
        subprocess.run(['open', file_path])
    else:
        subprocess.run(['xdg-open', file_path])

def main():
    AUDIO_FORMATS = ['mp3', 'wav', 'aac', 'm4a', 'opus', 'flac']

    parser = argparse.ArgumentParser(description='Lightweight YouTube Download Tool')
    parser.add_argument('url', help='YouTube video URL')
    parser.add_argument('output', nargs='?', help='Output file name (optional)')

    # Existing flags
    parser.add_argument('-d', '--downloads', action='store_true',
                        help='Download to the system\'s Downloads folder')
    parser.add_argument('-o', '--open', action='store_true',
                        help='Open file explorer after download')
    parser.add_argument('-p', '--play', action='store_true',
                        help='Play the video after download')
    parser.add_argument('-q', '--quality', choices=['best', 'worst'], default='best',
                        help='Select video quality (default: best)')
    parser.add_argument('-f', '--format', help='Specify download format (e.g., mp4, mp3)')

    # New flags for expanded yt_dlp functionality
    parser.add_argument('--list-formats', action='store_true',
                        help='List all available formats for the given URL, then exit')
    parser.add_argument('--subtitles', action='store_true',
                        help='Download subtitles for the video')
    parser.add_argument('--sub-lang',
                        help='Comma-separated subtitle languages (e.g. "en,es"). Default is "en"')
    parser.add_argument('--cookies', help='Path to a cookies file (e.g., cookies.txt)')
    parser.add_argument('--max-downloads', type=int,
                        help='Maximum number of videos to download')

    args = parser.parse_args()

    # Determine download directory
    if args.downloads:
        download_dir = get_downloads_folder()
        if download_dir is None:
            print("Unable to determine the Downloads folder on this system.")
            sys.exit(1)
    else:
        download_dir = '.'

    # Determine output file name and path
    if args.output:
        output_path = args.output
        output_dir, output_file = os.path.split(output_path)
        if args.downloads and output_dir:
            print("Error: Cannot combine a custom output path with the '-d' flag.")
            print("Remove the path from the output file name or do not use the '-d' flag.")
            sys.exit(1)
        if output_dir:
            download_dir = os.path.abspath(output_dir)

        output_basename, output_ext = os.path.splitext(output_file)
        output_ext = output_ext.lstrip('.').lower()

        # Determine expected format
        if args.format:
            expected_format = args.format.lower()
        else:
            expected_format = 'mp4'  # Default format

        # Check for file extension mismatch
        if output_ext != expected_format:
            print("Warning: Incompatible filetype, continuing anyway.")
            if expected_format in AUDIO_FORMATS:
                output_file = f"{output_basename}.{expected_format}"
                print(f"Changing output file name to '{output_file}' to match the format.")
                output_template = output_file
            else:
                output_template = output_file
        else:
            output_template = output_file
    else:
        output_template = '%(title)s.%(ext)s'
        output_ext = None
        expected_format = args.format.lower() if args.format else 'mp4'

    # Ensure download directory exists
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    # Base download options
    ydl_opts = {
        'outtmpl': os.path.join(download_dir, output_template),
        'noplaylist': True,        # Download only the video, not the entire playlist
        'updatetime': False,       # Do not set the file's mtime to the video's timestamp
    }

    # Incorporate new yt_dlp options

    # 1. List formats (if requested)
    # We'll handle this logic right before the actual download.
    # 2. Cookies
    if args.cookies:
        ydl_opts['cookiefile'] = args.cookies
    # 3. Max downloads
    if args.max_downloads:
        ydl_opts['max_downloads'] = args.max_downloads

    # Subtitles
    if args.subtitles:
        ydl_opts['writesubtitles'] = True
        # Use the provided subtitle language(s) or default to English
        if args.sub_lang:
            subs_list = [lang.strip() for lang in args.sub_lang.split(',')]
        else:
            subs_list = ['en']
        ydl_opts['subtitleslangs'] = subs_list
        # If you’d like to also download automatic subtitles:
        # ydl_opts['writeautomaticsub'] = True

    # Handle audio vs. video formats
    if expected_format in AUDIO_FORMATS:
        # For audio
        # If output is given, adjust the template to '%(ext)s'
        if args.output:
            output_basename = os.path.splitext(output_template)[0]
            output_template = output_basename + '.%(ext)s'
            ydl_opts['outtmpl'] = os.path.join(download_dir, output_template)

        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['final_ext'] = expected_format
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': expected_format,
            'preferredquality': '192',
        }]
    else:
        # For video
        if args.quality == 'best':
            ydl_opts['format'] = 'bestvideo+bestaudio/best'
        else:
            ydl_opts['format'] = 'worstvideo+worstaudio/worst'
        ydl_opts['merge_output_format'] = expected_format

    with YoutubeDL(ydl_opts) as ydl:
        try:
            # If user only wants to list the formats, do so and exit
            if args.list_formats:
                print("Listing all available formats for this URL:\n")
                info_dict = ydl.extract_info(args.url, download=False)
                # The actual printing of formats is done by yt_dlp automatically
                # if 'listformats' is True in ydl_opts, or we can manually print them:
                formats = info_dict.get('formats', [])
                for f in formats:
                    print(f"{f.get('format_id')}: {f.get('ext')} - {f.get('format_note')} - {f.get('resolution')} - {f.get('filesize', 0)} bytes")
                sys.exit(0)

            print(f"Downloading video from {args.url} ...")
            result = ydl.extract_info(args.url, download=True)

            if args.output:
                if expected_format in AUDIO_FORMATS:
                    filename = os.path.join(download_dir, output_basename + '.' + expected_format)
                else:
                    filename = os.path.join(download_dir, output_template)
            else:
                filename = ydl.prepare_filename(result)

            print(f"Download completed successfully: {filename}")
        except Exception as e:
            print(f"An error occurred: {e}")
            sys.exit(1)

    # Optionally open file explorer
    if args.open:
        open_file_explorer(os.path.dirname(os.path.abspath(filename)))

    # Optionally play the media
    if args.play:
        play_media(os.path.abspath(filename))

if __name__ == '__main__':
    main()
