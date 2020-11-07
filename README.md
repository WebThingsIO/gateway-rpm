# WebThings Gateway

RPM package for WebThings Gateway, available here: https://github.com/WebThingsIO/gateway/releases

Current build targets:
* Fedora 31 (x86\_64, aarch64)
* Fedora 32 (x86\_64, aarch64)
* Fedora 33 (x86\_64, aarch64)

## Installation

1. Download the appropriate package from the gateway's [releases page](https://github.com/WebThingsIO/gateway/releases).
2. Install the package:

    ```sh
    sudo dnf install ./webthings-gateway-fedora-31-x86_64.rpm
    ```

3. Set up your gateway by visiting http://localhost:8080 in a browser.

## Building

```sh
./build.sh
```
