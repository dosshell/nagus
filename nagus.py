#!/usr/bin/python3
"""This module does blah blah."""
import argparse
import os
import json
import zipfile

# pylint: disable=C0103
# pylint: disable=W0603
settings = {}

def load_default_settings():
    """This function does blah."""
    global settings
    settings = {}
    settings['servers'] = []
    settings['stash'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'stash')
    set_stash(settings['stash'])

def load_settings():
    """This function does blah."""
    try:
        with open('settings.json') as settings_file:
            global settings
            settings = json.load(settings_file)
    except FileNotFoundError:
        load_default_settings()
        save_settings()

def save_settings():
    """This function does blah."""
    with open('settings.json', 'w') as settings_file:
        global settings
        json.dump(settings, settings_file)

def add_server(server_path):
    """This function does blah."""
    print("Adding server: " + server_path)
    global settings
    settings['servers'].append(server_path)
    save_settings()

def is_package(item):
    """This function does blah."""
    if "/" not in item and "\\" not in item:
        return True
    else:
        return False

def has_servers():
    """This function does blah."""
    if settings['servers']:
        return True
    return False

def set_stash(directory):
    """This function does blah."""
    print("settings stash to: " + directory)
    os.environ['NAGUS_PATH'] = directory
    settings['stash'] = directory
    save_settings()
    if os.name == 'nt':
        os.system('setx NAGUS_STASH ' + directory)
        print("I also set OS environment variable NAGUS_PATH to " + directory + " for you")

def add_package(item):
    """This function does blah."""
    if os.path.isdir(os.path.join(settings['stash'], item)):
        print("Package already added")
        return
    found_file = False
    for x in settings['servers']:
        server_file = os.path.join(x, item + '.zip')
        if os.path.isfile(server_file):
            with zipfile.ZipFile(server_file, 'r') as z:
                z.extractall(os.path.join(settings['stash'], item))
                found_file = True
                break
    if not found_file:
        print("Did not find packege: " + item)
    else:
        print("Added package: " + item)

def main():
    """This function does blah."""
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=('add', 'rm', 'clear', 'stash'))
    parser.add_argument('item')
    args = parser.parse_args()

    load_settings()

    if args.action == "add":
        if is_package(args.item):
            if not has_servers():
                print("No servers is set")
                print("You can add servers with nagus add <you server path>")
                requested_server_path = input("Add server now: ")
                if requested_server_path != "":
                    add_server(requested_server_path)
                else:
                    exit()
            add_package(args.item)
        else:
            print("adding server: " + args.item)
    elif args.action == "rm":
        if is_package(args.item):
            print("removing package: " + args.item)
        else:
            print("removing server: " + args.item)
    elif args.action == "clear":
        if args.item == "servers":
            print("clearing all servers")
        elif args.item == "packages":
            print("clearing all packages")
        elif args.item == "all":
            print("clearing all servers")
            print("clearing all packages")
    elif args.action == "stash":
        set_stash(args.item)

if __name__ == "__main__":
    main()
