# nativemessaging
A Python package for interfacing with Native Messaging in WebExtensions

[See Native Messaging on MDN](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Native_messaging)

Based on [Native Messaging on MDN](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Native_messaging#App_side) and [native-messaging on mdn/webextension-examples](https://github.com/mdn/webextensions-examples/tree/master/native-messaging) (MPL 2.0 License)

`pip3 install nativemessaging`

## `get_message()`
`nativemessaging.get_message()` will poll for a message from the browser.  
If [`runtime.connectNative`](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/runtime/connectNative) is used, `get_message()` must be called repeatedly in a loop to poll for messages.  
If [`runtime.sendNativeMessage`](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/runtime/sendNativeMessage) is used, `get_message()` only needs to be called once.

## `send_message( message )`
`nativemessaging.send_message()` takes one argument, a message to be returned to the browser.

## Sample
Browser side:
```javascript
function onReceived(response) {
    console.log(response);
}

// runtime.connectNative
var port = browser.runtime.connectNative("application_name");
port.onMessage.addListener(onReceived);
port.postMessage("hello");

// runtime.sendNativeMessage
browser.runtime.sendNativeMessage("application_name", "hello").then(onReceived);
```

App side:
```python
import nativemessaging

while True:
    message = nativemessaging.get_message()
    if message == "hello":
        nativemessaging.send_message("world")
```

## nativemessaging-install
`nativemessaging-install` is a command line script provided with the package.

### Arguments
`nativemessaging-install browser [--manifest manifest]`
 * `browser` - positional argument, 1 or more parameters. Must be `chrome` or `firefox`.
 * `--manifest` - a path to a manifest file to use for installing.

### manifest-install.json
A `native-manifest.json` file is expected in the current working directory when running the script, unless `--manifest` is passsed.
The format must be similar to the native manifest format for Chrome or Firefox, with two main differences:
 * `path` must be a relative path to the native app in relation to your current working directory.
 * Both `allowed_extensions` and `allowed_origins` must be in the manifest to work with both Chrome and Firefox.
```json
{
    "name": "application_name",
    "description": "description",
    "path": "application_name.py",
    "type": "stdio",
    "allowed_extensions": ["extension@id"],
    "allowed_origins": ["chrome-extension://extension-id"]
}
```

### Created files
On Windows, it will create `<application_name>_firefox.json` and `<application_name>_chrome.json` in the same directory as `<path>`.  
A batch file will also be created for python apps on Windows.  
A registry key is created at `HKEY_CURRENT_USER\Software\Google\Chrome\NativeMessagingHosts\<application_name>` or `HKEY_CURRENT_USER\Software\Mozilla\NativeMessagingHosts\<application_name>`

On linux, it will create `~/.config/google-chrome/NativeMessagingHosts/<application_name>.json` or `~/.mozilla/native-messaging-hosts/<application_name>.json`

On mac, it will create `~/Library/Application Support/Google/Chrome/NativeMessagingHosts/<application_name>.json` or `~/Library/Application Support/Mozilla/NativeMessagingHosts/<application_name>.json`

#### See also:
 * [Native Messaging on Chrome Docs](https://developer.chrome.com/extensions/nativeMessaging)
