#!/usr/bin/env python3

import sys
import os
import zipfile
import rarfile
import threading
from colorama import init, Fore, Style
from tqdm import tqdm
import logging
import pyzipper

# Initialize colorama for cross-platform colored output
init()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ASCII Art Banner
def print_banner():
    banner = f'''
{Fore.RED}
██████╗ ██╗    ██╗███╗   ██╗███████╗██████╗  █████╗ ██████╗  ██████╗██╗  ██╗██╗██╗   ██╗███████╗
██╔══██╗██║    ██║████╗  ██║██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██║  ██║██║██║   ██║██╔════╝
██████╔╝██║ █╗ ██║██╔██╗ ██║█████╗  ██║  ██║███████║██████╔╝██║     ███████║██║██║   ██║█████╗  
██╔═══╝ ██║███╗██║██║╚██╗██║██╔══╝  ██║  ██║██╔══██║██╔══██╗██║     ██╔══██║██║╚██╗ ██╔╝██╔══╝  
██║     ╚███╔███╔╝██║ ╚████║███████╗██████╔╝██║  ██║██║  ██║╚██████╗██║  ██║██║ ╚████╔╝ ███████╗
╚═╝      ╚══╝╚══╝ ╚═╝  ╚═══╝╚══════╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝  ╚══════╝
{Style.RESET_ALL}
{Fore.CYAN}Made by syedbilalalam{Style.RESET_ALL}
'''
    print(banner)

# Ensure rarfile is configured to use unrar
rarfile.UNRAR_TOOL = 'unrar'  # Ensure 'unrar' is installed and in PATH

def try_password(archive_path, password, archive_type='zip'):
    try:
        if archive_type == 'zip':
            with pyzipper.AESZipFile(archive_path) as archive:
                archive.extractall(pwd=password.encode())
                return True
        elif archive_type == 'rar':
            with rarfile.RarFile(archive_path) as archive:
                archive.extractall(pwd=password)
                return True
    except:
        return False  # Remove detailed logging

def crack_archive(archive_path, wordlist_path, num_threads=4):
    if not os.path.exists(archive_path):
        print(f"{Fore.RED}Error: Archive file not found!{Style.RESET_ALL}")
        return
    
    if not os.path.exists(wordlist_path):
        print(f"{Fore.RED}Error: Wordlist file not found!{Style.RESET_ALL}")
        return

    archive_type = 'rar' if archive_path.lower().endswith('.rar') else 'zip'
    
    with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
        passwords = f.read().splitlines()

    print(f"{Fore.YELLOW}Starting password cracking with {num_threads} threads...{Style.RESET_ALL}")
    
    # Add a threading event to signal when a password is found
    found_event = threading.Event()

    def worker(password_chunk, pbar):
        for password in password_chunk:
            if found_event.is_set():
                break
            if try_password(archive_path, password, archive_type):
                print(f"\n{Fore.GREEN}Password found: {password}{Style.RESET_ALL}")
                found_event.set()
                break
            pbar.update(1)

    # Split passwords into chunks for threading
    chunk_size = len(passwords) // num_threads
    threads = []

    # Update the progress bar to show the number of passwords tried out of the total
    with tqdm(total=len(passwords), desc="Trying passwords", unit="pwd") as pbar:
        for i in range(num_threads):
            start_idx = i * chunk_size
            end_idx = start_idx + chunk_size if i < num_threads - 1 else len(passwords)
            password_chunk = passwords[start_idx:end_idx]
            
            thread = threading.Thread(target=worker, args=(password_chunk, pbar))
            threads.append(thread)
            thread.start()

        while not found_event.is_set() and any(thread.is_alive() for thread in threads):
            threading.Event().wait(0.1)

    # Ensure the program exits gracefully once the correct password is found
    if not found_event.is_set():
        print(f"{Fore.RED}Password not found in wordlist.{Style.RESET_ALL}")

def main():
    print_banner()
    
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <archive_path> <wordlist_path>")
        sys.exit(1)

    archive_path = sys.argv[1]
    wordlist_path = sys.argv[2]
    
    crack_archive(archive_path, wordlist_path)

if __name__ == "__main__":
    main()