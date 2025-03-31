import re
from os import path, listdir
import sys
import json
from tqdm import tqdm
import logging

#
# Precompiled regular expression patterns for email parsing
#
time_pattern = re.compile(r"Date: (?P<data>[A-Z][a-z]+, \d{1,2} [A-Z][a-z]+ \d{4} \d{2}:\d{2}:\d{2} -\d{4} \([A-Z]{3}\))")
subject_pattern = re.compile(r"Subject: (?P<data>.*)")
sender_pattern = re.compile(r"From: (?P<data>.*)")
recipient_pattern = re.compile(r"To: (?P<data>.*)")
cc_pattern = re.compile(r"cc: (?P<data>.*)")
bcc_pattern = re.compile(r"bcc: (?P<data>.*)")
msg_start_pattern = re.compile(r"\n\n", re.MULTILINE)  # Email body typically starts after two newlines
msg_end_pattern = re.compile(r"\n+.*\n\d+/\d+/\d+ \d+:\d+ [AP]M", re.MULTILINE)  # Pattern to detect end of message in replies

# Global data structures to store parsed email information
feeds = []       # List to store all parsed email data
users = {}       # Dictionary mapping user email addresses to unique IDs
threads = {}     # Dictionary mapping email subjects to unique thread IDs
thread_users = {}  # Dictionary mapping thread IDs to sets of user IDs involved in that thread
user_threads = {}  # Dictionary mapping user IDs to sets of thread IDs they're involved in

# Global counter to track processed files
processed_files = 0

def count_files(pathname):
    """
    Recursively count the number of files in a directory.
    """
    if path.isdir(pathname):
        total_files = 0
        for child in listdir(pathname):
            if child[0] != ".":  # Skip hidden files
                total_files += count_files(path.join(pathname, child))
        return total_files
    else:
        return 1

def parse_email(pathname, orig=True, progress_bar=None, max_files=20):
    """
    Recursively parse email files from a directory or a single file.
    Only processes a maximum of 'max_files' files.
    """
    global processed_files
    if processed_files >= max_files:
        return

    if orig:
        total_files = count_files(pathname)
        print(f"Total files to process: {total_files}")
        progress_bar = tqdm(total=total_files, desc="Processing files", unit="file")

    if path.isdir(pathname):
        progress_bar.write(f"Processing directory: {pathname}")
        for child in listdir(pathname):
            if child[0] != ".":
                if processed_files >= max_files:
                    break
                parse_email(path.join(pathname, child), False, progress_bar, max_files)
    else:
        if processed_files >= max_files:
            return
        with open(pathname, encoding="utf-8", errors="replace") as TextFile:
            text = TextFile.read().replace("\r", "")
            # Remove non-ASCII characters
            text = re.sub(r"[^\x00-\x7F]+", "", text)
            try:
                # Extract email metadata
                time = time_pattern.search(text).group("data").replace("\n", "")
                subject = subject_pattern.search(text).group("data").replace("\n", "")
                sender = sender_pattern.search(text).group("data").replace("\n", "")
                recipient = recipient_pattern.search(text).group("data").split(", ")
                cc = cc_pattern.search(text).group("data").split(", ")
                bcc = bcc_pattern.search(text).group("data").split(", ")
                
                # Extract email body
                msg_start_iter = msg_start_pattern.search(text).end()
                try:
                    msg_end_iter = msg_end_pattern.search(text).start()
                    message = text[msg_start_iter:msg_end_iter]
                except AttributeError:  # Not a reply
                    message = text[msg_start_iter:]
                
                # Clean up the message text
                message = re.sub("[\n\r]", " ", message)
                message = re.sub("  +", " ", message)
            except AttributeError:
                logging.error("Failed to parse %s" % pathname)
                return None
                
            # Get or create unique IDs for users and threads
            sender_id = get_or_allocate_uid(sender)
            recipient_ids = [get_or_allocate_uid(u.strip()) for u in recipient if u.strip() != ""]
            cc_ids = [get_or_allocate_uid(u.strip()) for u in cc if u.strip() != ""]
            bcc_ids = [get_or_allocate_uid(u.strip()) for u in bcc if u.strip() != ""]
            thread_id = get_or_allocate_tid(subject)
            
        # Initialize thread_users entry if needed
        if thread_id not in thread_users:
            thread_users[thread_id] = set()
            
        # Track all users involved in this email thread
        users_involved = [sender_id] + recipient_ids + cc_ids + bcc_ids
        thread_users[thread_id] |= set(users_involved)
        
        # Update user_threads to track which threads each user is involved in
        for user in set(users_involved):
            if user not in user_threads:
                user_threads[user] = set()
            user_threads[user].add(thread_id)
 
        # Create the email entry and add it to the feeds list
        entry =  {"time": time, "thread": thread_id, "sender": sender_id, "recipients": recipient_ids, "cc": cc_ids, "bcc": bcc_ids, "message": message, "filepath": pathname}
        feeds.append(entry)
        
        processed_files += 1
        progress_bar.update(1)

    if orig:
        progress_bar.close()
        try:
            # Write all collected data to JSON files
            with open('user_data/messages.json', 'w') as f:
                json.dump(feeds, f)
            with open('user_data/users.json', 'w') as f:
                json.dump(users, f)
            with open('user_data/threads.json', 'w') as f:
                json.dump(threads, f)
            with open('user_data/thread-users.json', 'w') as f:
                # Convert sets to lists for JSON serialization
                for thread in thread_users:
                    thread_users[thread] = list(thread_users[thread])
                json.dump(thread_users, f)
            with open('user_data/user-threads.json', 'w') as f:
                # Convert sets to lists for JSON serialization
                for user in user_threads:
                    user_threads[user] = list(user_threads[user])
                json.dump(user_threads, f)
        except IOError:
            print("Unable to write to output files, aborting")
            exit(1)

def get_or_allocate_uid(name):
    """
    Get or create a unique ID for a user email address.
    """
    if name not in users:
        users[name] = len(users)
    return users[name]

def get_or_allocate_tid(name):
    """
    Get or create a unique ID for an email thread based on subject.
    """
    parsed_name = re.sub("(RE|Re|FWD|Fwd): ", "", name)
    if parsed_name not in threads:
        threads[parsed_name] = len(threads)
    return threads[parsed_name]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parser.py <file_path> [max_files]")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    # Check if a maximum files argument was provided; default if not.
    if len(sys.argv) >= 3:
        try:
            max_files = int(sys.argv[2])
        except ValueError:
            print("Invalid value for max_files; please provide an integer.")
            sys.exit(1)
    elif len(sys.argv) == 2:
        max_files = 20000
    else:
        print("Usage: python parser.py <file_path> [max_files]")
        sys.exit(1)
    
    try:
        parse_email(file_path, orig=True, max_files=max_files)
    except Exception as e:
        logging.error(f"Error: {e}")
        logging.error("Usage: python parser.py <file_path> [max_files]")
        exit(1)
