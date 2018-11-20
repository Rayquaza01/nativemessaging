#!/usr/bin/env python3
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


def options():
    ap = argparse.ArgumentParser()
    ap.add_argument("browser", choices=["chrome", "firefox"], nargs="+")
    ap.add_argument("--manifest")
    return vars(ap.parse_args())


def readFile(file):
    with open(file, "r") as f:
        return f.read()


def writeFile(file, contents):
    with open(file, "w") as f:
        f.write(contents)


def createRegKey(path, value):
    winreg.CreateKey(winreg.HKEY_CURRENT_USER, path)
    registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_WRITE)
    winreg.SetValue(registry_key, "", winreg.REG_SZ, value)
    winreg.CloseKey(registry_key)
    print("Created registry key at HKEY_CURRENT_USER\\" + path)


def writeManifest(browser, path, manifest):
    if browser == "firefox":
        manifest.pop("allowed_origins", None)
    elif browser == "chrome":
        manifest.pop("allowed_extensions", None)
    writeFile(path, json.dumps(manifest))
    print("Saved manifest file to " + path)


def main():
    opts = options()
    if opts["manifest"] is not None and os.path.isfile(opts["manifest"]):  # read from arguments if available
        print("Reading manifest: " + opts["manifest"])
        file = readFile(opts["manifest"])
    elif os.path.isfile("native-manifest.json"):  # fall back to native-manifest.json
        print("Reading manifest: native-manifest.json")
        file = readFile("native-manifest.json")
    else:
        raise Exception("No manifest found. Supply a manifest in the arguments, or create a manifest named native-manifest.json")
    manifest = json.loads(file)
    manifest["path"] = os.path.abspath(manifest["path"])  # ensure path is absolute
    print("Absolute path: " + manifest["path"])
    if sys.platform == "win32":
        install_dir = os.path.dirname(manifest["path"])
        if manifest["path"].endswith(".py"):  # create batch file for python apps in windows
            batch_path = os.path.join(install_dir, manifest["name"] + ".bat")
            writeFile(batch_path,
                      "@echo off\npython -u \"{0}\"".format(manifest["path"]))
            manifest["path"] = batch_path
            print("Batch file created at: " + manifest["path"])
        # write registry key on windows
        for browser in opts["browser"]:
            manifest_path = os.path.join(install_dir, "{0}_{1}.json".format(manifest["name"], browser))
            writeManifest(browser, manifest_path, manifest)
            createRegKey(os.path.join(browser_info[browser]["registry"], manifest["name"]),
                         manifest_path)
    if sys.platform in ["linux", "darwin"]:  # save manifest in linux and mac
        for browser in opts["browser"]:
            manifest_path = os.path.join(browser_info[browser][sys.platform],
                                         manifest["name"] + ".json")
            manifest_path_folder = os.path.dirname(manifest_path)
            if not os.path.exists(manifest_path_folder):
                os.mkdir(manifest_path_folder)
            writeManifest(browser, manifest_path, manifest)
    input("Done! Press enter or close the window.")


if __name__ == "__main__":
    main()
