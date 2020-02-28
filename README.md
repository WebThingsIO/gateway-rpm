# WebThings Gateway by Mozilla

![GitHub Workflow Status](https://img.shields.io/github/workflow/status/mozilla-iot/gateway-rpm/Build)

RPM package for Mozilla's WebThings Gateway, available here: https://github.com/mozilla-iot/gateway/releases

Current build targets:
* Fedora 30 (x86\_64, aarch64)
* Fedora 31 (x86\_64, aarch64)

## Installation

1. Download the appropriate package from the gateway's [releases page](https://github.com/mozilla-iot/gateway/releases).
2. Install the package:

    ```sh
    sudo dnf install ./webthings-gateway-fedora-31-x86_64.rpm
    ```

3. Set up your gateway by visiting http://localhost:8080 in a browser.

## Building

```sh
./build.sh
```
