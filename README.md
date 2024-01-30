# LeBRA
Legacy Barcode Reader Application

LeBRA is a small python script serving a simple HTML form. Supplied data is emulated as key presses on the host. This allows old MDE devices like those with Windows CE or Windows Mobile to be used with applications requiring desktop operating systems or modern web browsers. You can also use a dedicated P2P-WiFi if your device is too old to connect to current access points.

On the technical side it uses python-pynput for key emulation, it should work on Windows, macOS and Linux based systems.

On Linux, pynput uses X or uinput. X.org based systems work as user, uinput requires the script to be run as root.

On macOS the process must run as root. Your application must also be white listed under Enable access for assistive devices. You may also need to whitelist your terminal application if running your script from a terminal.