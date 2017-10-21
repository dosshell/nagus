#!/usr/bin/python3
"""This module does blah blah."""
import argparse
import os
import json
import zipfile
import shutil

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
    global settings
    settings['servers'].append(server_path)
    save_settings()

def rm_server(server_path):
    """This function does blah."""
    global settings
    settings['servers'].remove(server_path)
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

def list_of_packages():
    """This function does blah."""
    if os.path.isdir(settings['stash']):
        return os.listdir(settings['stash'])
    else:
        return []

def add_package(item, extra_servers=None):
    """This function does blah."""
    if item in list_of_packages():
        print("Package already added: " + item)
        return
    if extra_servers is None:
        extra_servers = []
    found_file = False
    for x in settings['servers'] + extra_servers:
        server_file = os.path.join(x, item + '.zip')
        if os.path.isfile(server_file):
            with zipfile.ZipFile(server_file, 'r') as z:
                z.extractall(os.path.join(settings['stash'], item))
                found_file = True
                print("Added package: " + item + " from " + x)
                break
    if not found_file:
        print("Did not find packege: " + item) 

def rm_package(item):
    """This function does blah."""
    if not item in list_of_packages():
        print("package not found: " + item)
        return
    print("removing: " + item)
    shutil.rmtree(os.path.join(settings['stash'], item))

def rm_all_packages():
    """This function does blah."""
    for x in list_of_packages():
        rm_package(x)

def add_json(item):
    """This function does blah."""
    with open(item) as sync_file:
        sync = json.load(sync_file)
        for package in sync['packages']:
            add_package(package, sync['servers'])

def main():
    """This function does blah."""
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=('add', 'rm', 'stash', 'view'))
    parser.add_argument('item')
    args = parser.parse_args()

    load_settings()

    if args.action == "add":
        if os.path.splitext(args.item)[1] == '.json' and os.path.isfile(args.item):
            print("Adding packages from: " + args.item)
            add_json(args.item)
        elif is_package(args.item):
            if not has_servers():
                print("No servers is set")
                print("You can add servers with nagus add <you server path>")
                requested_server_path = input("Add server now: ")
                if requested_server_path != "":
                    print("Adding server: " + requested_server_path)
                    add_server(requested_server_path)
                else:
                    exit()
            add_package(args.item)
        else:
            print("adding server: " + args.item)
            add_server(args.item)
    elif args.action == 'rm':
        if args.item == '*':
            print("removing all packages")
            rm_all_packages()
        elif is_package(args.item):
            rm_package(args.item)
        else:
            print("removing server: " + args.item)
            rm_server(args.item)
    elif args.action == 'stash':
        set_stash(args.item)
    elif args.action == 'view':
        if args.item == 'servers':
            for server in settings['servers']:
                print(server)
        elif args.item == 'packages':
            for pkg in list_of_packages():
                print(pkg)
        elif os.path.splitext(args.item)[1] == '.json' and os.path.isfile(args.item):
            with open(args.item) as sync_file:
                sync = json.load(sync_file)
                print("Packages:")
                for package in sync['packages']:
                    print(package)
                print("Servers:")
                for server in sync['servers']:
                    print(server)
        else:
            print("You can only view servers, packages and nagus json files")

if __name__ == "__main__":
    main()
