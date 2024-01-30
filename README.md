# LeBRA
Legacy Barcode Reader Application

LeBRA is a small python script serving a simple HTML form. Supplied data is emulated as key presses on the host. This allows old MDE devices like those with Windows CE or Windows Mobile to be used with applications requiring desktop operating systems or modern web browsers. You can also use a dedicated P2P-WiFi if your device is too old to connect to current access points.

On the technical side it uses python-keyboard for key emulation, it should work on Windows and Linux based systems.

Beware: Keyboard requires the script to be run as root on linux systems.