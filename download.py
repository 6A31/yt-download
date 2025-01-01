#!/usr/bin/env python3
import sys
import os
import subprocess
import argparse
from yt_dlp import YoutubeDL
import time

# Function to print a highly prominent warning message
def print_critical_warning(message):
    # Clear the screen
    os.system('cls' if os.name == 'nt' else 'clear')

    # Audible alert (may not work in all terminals)
    print('\a' * 3)

    # ASCII Art for warning
    warning_art = """
             ██     ██  █████  ██████  ███    ██ ██ ███    ██  ██████  
             ██     ██ ██   ██ ██   ██ ████   ██ ██ ████   ██ ██       
             ██  █  ██ ███████ ██████  ██ ██  ██ ██ ██ ██  ██ ██   ███ 
             ██ ███ ██ ██   ██ ██   ██ ██  ██ ██ ██ ██  ██ ██ ██    ██ 
              ███ ███  ██   ██ ██   ██ ██   ████ ██ ██   ████  ██████         
    """

    # Warning message with flashing effect (Note: Flashing text is not widely supported)
    flashing_start = "\033[5m"  # Starts blinking text (may not work in all terminals)
    flashing_end = "\033[25m"   # Ends blinking text

    # Bold red text
    red_bold = "\033[1;91m"
    reset = "\033[0m"

    # Display the warning
    print(red_bold + warning_art + reset)
    print(flashing_start + red_bold + "!!! CRITICAL WARNING !!!".center(80) + reset + flashing_end)
    print(red_bold + "=" * 80 + reset)
    print(red_bold + message.center(80) + reset)
    print(red_bold + "=" * 80 + reset)

def main():
    # List of known audio formats
    AUDIO_FORMATS = ['mp3', 'wav', 'aac', 'm4a', 'opus', 'flac']

    # Parsing command-line arguments
    parser = argparse.ArgumentParser(description='Lightweight YouTube Download Tool')
    parser.add_argument('url', help='YouTube video URL')
    parser.add_argument('output', nargs='?', help='Output file name (optional)')
    parser.add_argument('-d', '--downloads', action='store_true', help='Download to the system\'s Downloads folder')
    parser.add_argument('-o', '--open', action='store_true', help='Open file explorer after download')
    parser.add_argument('-p', '--play', action='store_true', help='Play the video after download')
    parser.add_argument('-q', '--quality', choices=['best', 'worst'], default='best', help='Select video quality (default: best)')
    parser.add_argument('-f', '--format', help='Specify download format (e.g., mp4, mp3)')
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

        # If output_dir is specified and -d is used, raise an error
        if args.downloads and output_dir:
            print("Error: Cannot combine a custom output path with the '-d' flag.")
            print("Remove the path from the output file name or do not use the '-d' flag.")
            sys.exit(1)

        # If output_dir is specified, use it as the download directory
        if output_dir:
            download_dir = os.path.abspath(output_dir)

        # Extract file extension from output file name
        output_basename, output_ext = os.path.splitext(output_file)
        output_ext = output_ext.lstrip('.').lower()

        # Determine expected format
        if args.format:
            expected_format = args.format.lower()
        else:
            expected_format = 'mp4'  # Default format

        # Check for file extension mismatch
        if output_ext != expected_format:
            warning_message = (
                f"THE FILE EXTENSION '{output_ext.upper()}' DOES NOT MATCH THE SPECIFIED FORMAT '{expected_format.upper()}'!\n"
                "THIS MISMATCH MAY LEAD TO UNEXPECTED BEHAVIOR OR ERRORS!"
            )
            print_critical_warning(warning_message)

            # Prompt user for explicit acknowledgment
            print("\nTo proceed, please type 'I UNDERSTAND AND ACCEPT THE RISK':")
            response = input("> ")
            if response.strip().lower() != 'i understand and accept the risk':
                print("\nAction aborted due to format mismatch and lack of acknowledgment.")
                sys.exit(1)

            if expected_format in AUDIO_FORMATS:
                # Adjust the output filename to have the expected format extension
                output_file = f"{output_basename}.{expected_format}"
                print(f"\nChanging output file name to '{output_file}' to match the format.")
                output_template = output_file
            else:
                output_template = output_file  # Proceed with the given filename
        else:
            output_template = output_file
    else:
        # No output file specified, use default template
        output_template = '%(title)s.%(ext)s'
        output_ext = None  # Will be determined based on the format
        expected_format = args.format.lower() if args.format else 'mp4'

    # Ensure download directory exists
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    # Setting up download options
    ydl_opts = {
        'outtmpl': os.path.join(download_dir, output_template),
        'noplaylist': True,  # Download only the video, not the entire playlist if URL is a playlist
        'updatetime': False,  # Do not set the file's mtime to the video's timestamp
    }

    # For audio formats, adjust output template to avoid double extensions
    if expected_format in AUDIO_FORMATS:
        # Adjust output template to include '.%(ext)s' and set 'final_ext'
        if args.output:
            output_basename = os.path.splitext(output_template)[0]
            output_template = output_basename + '.%(ext)s'
            ydl_opts['outtmpl'] = os.path.join(download_dir, output_template)
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['final_ext'] = expected_format  # Set final extension
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': expected_format,
            'preferredquality': '192',
        }]
    else:
        # Handle video formats
        if args.quality == 'best':
            ydl_opts['format'] = 'bestvideo+bestaudio/best'
        else:
            ydl_opts['format'] = 'worstvideo+worstaudio/worst'
        # Ensure the output extension matches the expected format
        ydl_opts['merge_output_format'] = expected_format

    # Downloading the video/audio
    with YoutubeDL(ydl_opts) as ydl:
        try:
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

    # Open file explorer after downloading
    if args.open:
        open_file_explorer(os.path.dirname(os.path.abspath(filename)))

    # Play the video/audio after downloading
    if args.play:
        play_media(os.path.abspath(filename))

def get_downloads_folder():
    """Get the path to the user's Downloads folder."""
    if sys.platform == 'win32':
        from ctypes import windll, wintypes, byref
        import ctypes

        # Define the GUID structure
        class GUID(ctypes.Structure):
            _fields_ = [
                ('Data1', wintypes.DWORD),
                ('Data2', wintypes.WORD),
                ('Data3', wintypes.WORD),
                ('Data4', wintypes.BYTE * 8)
            ]

        # Reference to the SHGetKnownFolderPath function
        SHGetKnownFolderPath = windll.shell32.SHGetKnownFolderPath
        SHGetKnownFolderPath.argtypes = [
            ctypes.POINTER(GUID), wintypes.DWORD, wintypes.HANDLE,
            ctypes.POINTER(ctypes.c_wchar_p)
        ]

        # Initialize the FOLDERID for Downloads
        FOLDERID_Downloads = GUID(
            0x374DE290, 0x123F, 0x4565,
            (wintypes.BYTE * 8)(
                0x91, 0x64, 0x39, 0xC4, 0x92, 0x5E, 0x46, 0x7B
            )
        )
        KF_FLAG_DEFAULT = 0
        path_ptr = ctypes.c_wchar_p()

        # Call the function
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

if __name__ == '__main__':
    main()