# -*- coding: utf-8 -*-

import argparse
import os
import sys
import json
if sys.platform == "win32":
    import winreg

# locations for storing manifests
browser_info = {
    "chrome": {
        "registry": "Software\\Google\\Chrome\\NativeMessagingHosts",
        "linux": os.path.join(os.path.expandvars("$HOME"), ".config/google-chrome/NativeMessagingHosts"),
        "darwin": os.path.join(os.path.expandvars("$HOME"), "Library/Application Support/Google/Chrome/NativeMessagingHosts")
    },
    "firefox": {
        "registry": "Software\\Mozilla\\NativeMessagingHosts",
        "linux": os.path.join(os.path.expandvars("$HOME"), ".mozilla/native-messaging-hosts"),
        "darwin": os.path.join(os.path.expandvars("$HOME"), "Library/Application Support/Mozilla/NativeMessagingHosts")
    }
}

def read_file(filename):
    with open(filename, "r") as f:
        return f.read()


def write_file(filename, contents):
    with open(filename, "w") as f:
        f.write(contents)


def write_manifest(browser, path, manifest):
    if browser == "firefox":
        manifest.pop("allowed_origins", None)
    elif browser == "chrome":
        manifest.pop("allowed_extensions", None)
    write_file(path, json.dumps(manifest))
    #print("Saved manifest file to " + path)


def create_reg_key(path, value):
    winreg.CreateKey(winreg.HKEY_CURRENT_USER, path)
    registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_WRITE)
    winreg.SetValue(registry_key, "", winreg.REG_SZ, value)
    winreg.CloseKey(registry_key)
    print("Created registry key at HKEY_CURRENT_USER\\" + path)


def install_windows(browsers, manifest):
    install_dir = os.path.dirname(manifest["path"])
    if manifest["path"].endswith(".py"):
        # create batch file for python apps in windows
        batch_path = os.path.join(install_dir, manifest["name"] + ".bat")
        write_file(batch_path, "@echo off\npython -u \"{0}\"".format(manifest["path"]))
        manifest["path"] = batch_path
        #print("Batch file created at: " + manifest["path"])
    # write registry key on windows
    for browser in browsers:
        manifest_path = os.path.join(install_dir, "{0}_{1}.json".format(manifest["name"], browser))
        write_manifest(browser, manifest_path, manifest)
        create_reg_key(os.path.join(browser_info[browser]["registry"], manifest["name"]),
                       manifest_path)


def install_unix(browsers, manifest):
    for browser in browsers:
        manifest_path_folder = browser_info[browser][sys.platform]
        if not os.path.exists(manifest_path_folder):
            os.mkdir(manifest_path_folder)
        manifest_path = os.path.join(manifest_path_folder, manifest["name"] + ".json")
        write_manifest(browser, manifest_path, manifest)


def install(browsers, manifest):
    # ensure path is absolute
    manifest["path"] = os.path.abspath(manifest["path"])
    #print("Absolute path: " + manifest["path"])

    if sys.platform == "win32":
        install_windows(browsers, manifest)
    elif sys.platform in ["linux", "darwin"]:
        install_unix(browsers, manifest)


def options():
    ap = argparse.ArgumentParser()
    ap.add_argument("browser", choices=["chrome", "firefox"], nargs="+")
    ap.add_argument("--manifest")
    return vars(ap.parse_args())


def main():
    opts = options()

    manifest_file = "native-manifest.json"
    if opts["manifest"] is not None and os.path.isfile(opts["manifest"]):
        # read from arguments if available
        manifest_file = opts["manifest"]
    elif os.path.isfile("native-manifest.json"):
        # fall back to native-manifest.json
        pass
    else:
        raise Exception("No manifest found. Supply a manifest in the arguments, or create a manifest named native-manifest.json")

    # read contents of manifest file
    print("Reading manifest: " + manifest_file)
    manifest_contents = read_file(manifest_file)
    manifest = json.loads(manifest_contents)

    install(opts["browser"], manifest)

    input("Done! Press enter or close the window.")
