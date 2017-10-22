#!/usr/bin/python3
"""This module does blah blah."""
import argparse
import os
import json
import zipfile
import shutil
import glob
import subprocess

# pylint: disable=C0103
# pylint: disable=W0603
settings = {}

def load_default_settings():
    """Load default settings to global variable `settings`"""
    global settings
    settings = {}
    settings['servers'] = []
    settings['stash'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'stash')
    set_stash(settings['stash'])

def load_settings():
    """Load setting from `settings.json` to global variable `settings`"""
    try:
        with open('settings.json') as settings_file:
            global settings
            settings = json.load(settings_file)
    except FileNotFoundError:
        load_default_settings()
        save_settings()

def save_settings():
    """Save global variable `settings` to `settings.json`"""
    with open('settings.json', 'w') as settings_file:
        global settings
        json.dump(settings, settings_file)

def add_server(server_path):
    """Add a server path to settings"""
    global settings
    settings['servers'].append(server_path)
    save_settings()

def rm_server(server_path):
    """Remove a server path from settings"""
    global settings
    settings['servers'].remove(server_path)
    save_settings()

def is_package(item):
    """Does this string describes a package"""
    if "/" not in item and "\\" not in item:
        return True
    else:
        return False

def has_servers():
    """Do we have atleast one server"""
    if settings['servers']:
        return True
    return False

def set_stash(directory):
    """Set stash to a directory and save it. Also set ENV PATH in windows"""
    print("settings stash to: " + directory)
    os.environ['NAGUS_PATH'] = directory
    settings['stash'] = directory
    save_settings()
    if os.name == 'nt':
        os.system('setx NAGUS_STASH ' + directory)
        print("I also set OS environment variable NAGUS_PATH to " + directory + " for you")

def list_of_packages():
    """Return a list of all local packages"""
    if os.path.isdir(settings['stash']):
        return os.listdir(settings['stash'])
    else:
        return []

def add_package(item, extra_servers=None):
    """Download a list of package"""
    if item in list_of_packages():
        print("Package already added: " + item)
        return
    if extra_servers is None:
        extra_servers = []
    found_file = False
    for x in settings['servers'] + extra_servers:
        #mount server if needed
        if "@" in x:
            if os.name == 'nt':
                username = x.split(':')[0]
                password = x.split(':')[1].split('@')[0]
                path = x.split('@')[1]
                cmd_mount = 'NET USE ' + path + ' /User:' + username + ' ' + password
                subprocess.run(cmd_mount, stdout=open(os.devnull, 'wb'))
                x = path
            else:
                print("This platform does not support the path: " + x)
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
    """Remove a local package"""
    if not item in list_of_packages():
        print("package not found: " + item)
        return
    print("removing: " + item)
    shutil.rmtree(os.path.join(settings['stash'], item))

def rm_all_packages():
    """Remove all local packages"""
    for x in list_of_packages():
        rm_package(x)

def add_json(item):
    """Download all packages described by a json file"""
    with open(item) as sync_file:
        sync = json.load(sync_file)
        for package in sync['packages']:
            add_package(package, sync['servers'])

def is_nagus_json(item):
    """Does this string describes a json sync file"""
    return os.path.splitext(item)[1] == '.json' and os.path.isfile(item)

def keep_only(items):
    """Remove all local packages except them in `items`"""
    list_to_keep = []
    for item in items:
        if is_nagus_json(item):
            with open(item) as json_file:
                nagus_file_data = json.load(json_file)
                list_to_keep.extend(nagus_file_data['packages'])
        elif os.path.isdir(item):
            print("dir: " + item)
            for filename in glob.iglob(item + '/**/nagus_packages.json', recursive=True):
                with open(filename) as json_file:
                    nagus_file_data = json.load(json_file)
                    list_to_keep.extend(nagus_file_data['packages'])
        else:
            list_to_keep.append(item)
    to_remove = [x for x in list_of_packages() if x not in list_to_keep]
    for pkg in to_remove:
        rm_package(pkg)

def main():
    """Main functioon"""
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=('add', 'rm', 'stash', 'view', 'keep'))
    parser.add_argument('item', nargs='+')
    args = parser.parse_args()
    load_settings()

    if args.action == "add":
        for item in args.item:
            if is_nagus_json(item):
                print("Adding packages from: " + item)
                add_json(item)
            elif is_package(item):
                if not has_servers():
                    print("No servers is set")
                    print("You can add servers with nagus add <you server path>")
                    requested_server_path = input("Add server now: ")
                    if requested_server_path != "":
                        print("Adding server: " + requested_server_path)
                        add_server(requested_server_path)
                    else:
                        exit()
                add_package(item)
            else:
                print("adding server: " + item)
                add_server(item)
    elif args.action == 'rm':
        for item in args.item:
            if item == '*':
                print("removing all packages")
                rm_all_packages()
            elif is_package(item):
                rm_package(item)
            else:
                print("removing server: " + args.item)
                rm_server(args.item)
    elif args.action == 'stash':
        if len(args.item) != 1:
            print("I do not support several stashes")
            return
        set_stash(args.item[0])
    elif args.action == 'view':
        for item in args.item:
            if item == 'servers':
                for server in settings['servers']:
                    print("Servers:")
                    print(server)
            elif item == 'packages':
                print("Packages:")
                for pkg in list_of_packages():
                    print(pkg)
            elif is_nagus_json(item):
                with open(item) as sync_file:
                    sync = json.load(sync_file)
                    print("Packages:")
                    for package in sync['packages']:
                        print(package)
                    print("Servers:")
                    for server in sync['servers']:
                        print(server)
            else:
                print("You can only view servers, packages and nagus json files")
    elif args.action == 'keep':
        keep_only(args.item)

if __name__ == "__main__":
    main()
