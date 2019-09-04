#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Given a directory path, search all files in the path for a given text string
within the 'word/document.xml' section of a MSWord .dotm file.
"""
import os
import sys
import zipfile
import argparse

__author__ = "Salvador240"

def create_parser():
    '''Creates a parser for dotm searcher'''
    parser = argparse.ArgumentParser(description='Searches for text within all dotm files in a directory')
    parser.add_argument('--dir', help='directory to search for dotm files', default='.')
    parser.add_argument('text', help='text to search within each dotm file')
    return parser

def main():
    '''Opens a dotm file and scans for a substring'''
    # argparse creates a namespace of key-value pairs
    parser = create_parser()
    ns = parser.parse_args()
    search_text = ns.text
    search_path = ns.dir
    print(ns)

    print("Searching directory {} for dotm files with text '{}' ...".format(search_path, search_text))

    file_list = os.listdir(search_path)
    match_count = 0
    search_count = 0

    # Iterate over each file in search path
    for file in file_list:
        # Don't care about other file extensions besides dotm
        if not file.endswith('.dotm'):
            print("Disregard file: " + file)
            continue
        else:
            search_count +=1

        # full_path = search_path + '\\' + file
        full_path = os.path.join(search_path, file)
        # print(full_path)
        if zipfile.is_zipfile(full_path):
            with zipfile.ZipFile(full_path) as z:
                names = z.namelist()
                if 'word/document.xml' in names:
                    with z.open('word/document.xml', 'r') as doc:
                        for line in doc:
                            line = line.decode('utf-8')
                            text_location = line.find(search_text)
                            if text_location >= 0:
                                print('Match found in file {}'.format(full_path))
                                print('...' + line[text_location - 40:text_location + 41] + '...')
                                match_count += 1
    print('Total dotm files searched: {}'.format(search_count))
    print('Total dotm files matched: {}'.format(match_count))


if __name__ == '__main__':
    main()
