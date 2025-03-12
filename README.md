# PwnedArchive

PwnedArchive is a command-line tool designed to perform dictionary attacks on password-protected ZIP and RAR files. It uses a wordlist to attempt to crack the password and supports multi-threading for faster processing.

## Features

- Supports ZIP and RAR file formats
- Dictionary-based attack using a wordlist
- Multi-threading for improved performance
- Progress bar to show the number of passwords tried
- Clear success message when the correct password is found

## Requirements

- Python 3.x
- `pyzipper` for handling ZIP files
- `rarfile` for handling RAR files (requires `unrar` to be installed)
- `colorama` for colored terminal output
- `tqdm` for progress bar

## Installation

1. Clone the repository:
   ```bash
   cd PwnedArchive
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure `unrar` is installed and available in your system's PATH.

## Usage

Run the script with the following command:
```bash
python pwnedarchive.py <archive_path> <wordlist_path>
```

Example:
```bash
python pwnedarchive.py protected.zip wordlist.txt
```

- `<archive_path>`: Path to the password-protected ZIP or RAR file.
- `<wordlist_path>`: Path to the wordlist file containing potential passwords.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Author

Made by syedbilalalam 