#!/usr/bin/env python3
"""
A script to extract plain text from a single MHTML file provided as a command-line argument.
It parses the MHTML file as a MIME message, extracts text from its HTML (or plain text) parts,
removes HTML tags using BeautifulSoup, and writes the result to a .txt file.

Usage:
    python extract_mhtml_text.py your_file.mhtml

Make sure BeautifulSoup is installed:
    pip install beautifulsoup4
"""

import sys
import os
from email import policy
from email.parser import BytesParser
from bs4 import BeautifulSoup

def extract_text_from_mhtml(file_path):
    """
    Extract plain text from an MHTML file by parsing its MIME structure.
    Processes both HTML and plain text parts, decoding properly.
    """
    with open(file_path, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)
    
    text_parts = []

    def decode_part(part):
        charset = part.get_content_charset() or 'utf-8'
        try:
            return part.get_payload(decode=True).decode(charset, errors='replace')
        except Exception as e:
            print(f"Warning: failed to decode part: {e}")
            return ''

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == 'text/html':
                html_content = decode_part(part)
                soup = BeautifulSoup(html_content, 'html.parser')
                text_parts.append(soup.get_text(separator="\n", strip=True))
            elif content_type == 'text/plain':
                text_parts.append(decode_part(part))
    else:
        content_type = msg.get_content_type()
        if content_type == 'text/html':
            html_content = decode_part(msg)
            soup = BeautifulSoup(html_content, 'html.parser')
            text_parts.append(soup.get_text(separator="\n", strip=True))
        else:
            text_parts.append(decode_part(msg))
    
    return "\n\n".join(text_parts)

def main():
    if len(sys.argv) != 2:
        print("Usage: python extract_mhtml_text.py <file.mhtml>")
        return

    file_path = sys.argv[1]
    if not os.path.isfile(file_path):
        print(f"File '{file_path}' not found.")
        return

    print(f'Processing {file_path} ...')
    extracted_text = extract_text_from_mhtml(file_path)
    output_file = os.path.splitext(file_path)[0] + ".txt"
    with open(output_file, "w", encoding="utf-8") as out:
        out.write(extracted_text)
    print(f"Extracted text written to {output_file}")

if __name__ == "__main__":
    main()

