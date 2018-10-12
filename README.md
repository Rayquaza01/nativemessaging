# nativemessaging
A python package for interfacing with native messaging in webextensions

[See Native Messaging on MDN](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Native_messaging)

Based on [Native Messaging on MDN](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Native_messaging#App_side) and [native-messaging on mdn/webextension-examples](https://github.com/mdn/webextensions-examples/tree/master/native-messaging) (MPL 2.0 License)

`pip3 install nativemessaging`

## `get_message()`
`nativemessaging.get_message()` will poll for a message from the browser.  
If [`runtime.connectNative`](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/runtime/connectNative) is used, `get_message()` must be called repeatedly in a loop to poll for messages.  
If [`runtime.sendNativeMessage`](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/runtime/sendNativeMessage) is used, `get_message()` only needs to be called once.

## `encode_message( message_content )`
`nativemessaging.encode_message()` takes one argument, a message to be encoded.  
Returns an encoded version of a message to be returned to the browser. Use with `send_message()`.

## `send_message( encoded_message )`
`nativemessaging.send_message()` takes one argument, an encoded message from `encode_message()`. Returns a message to the browser.

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
        nativemessaging.send_message(nativemessaging.encode_message("world"))
```
