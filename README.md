# LeBRA
Legacy Barcode Reader Application

LeBRA is a small python script serving a simple HTML form. Supplied data is emulated as key presses on the host. This allows old MDE devices like those with Windows CE or Windows Mobile to be used with applications requiring desktop operating systems or modern web browsers. You can also use a dedicated P2P-WiFi if your device is too old to connect to current access points.

On the technical side it uses xdotool for key emulation, so this script will only work on X.org based Linux systems. Also there is no further parsing, you are limited to lowercase ascii characters and numbers. Should be sufficient for UPC/EAN.