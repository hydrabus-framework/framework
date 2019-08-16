# hydrabus-framework [v0.1.0]

## Description

This project is a framework around the [hydrabus project](https://hydrabus.com/).
It provide multiple modules allowing you to work efficiently and save times on any hardware project.

## Installation

Clone this repository or get the latest release, then :

```
python3 setup.py install
```

## Usage

This framework work like metasploit. Simply run hbfconsole, load any available modules and enjoy !

## Configuration explanation

```

[HYDRABUS]
port = /dev/ttyACM0 ==> **Hydrabus device**
baudrate = 115200 ==> **baudrate value to communicate with hydrabus device**
read_timeout = 1 ==> **The read timeout value**

[MINITERM]
parity = N ==> **set parity (hydrabus communication, not device). one of {N, E, O, S, M}**
xonxoff = False ==> **enable software flow control**
echo = False ==> **enable local echo**
filters = default ==> **Text transformation, see Miniterm man**
raw = False ==> **Do no apply any encodings/transformations if True**
quiet = False ==> **suppress non-error messages**
exit_char = 29 ==> **Unicode of special character that is used to exit the application, default ctrl+] (29)**
menu_char = 20 ==> **Unicode code of special character that is used to control miniterm (menu), default ctrl+t (20)**
serial_port_encoding = UTF-8 ==> **set the encoding for the serial port (Latin1, UTF-8, ...)**
eol = CR ==> **end of line mode (CR, LF, CRLF)**

[THEME] **You can use HTML color code. For all possible theme value, see promp_toolkit manual https://python-prompt-toolkit.readthedocs.io/en/master/pages/advanced_topics/styling.html#style-strings**
base = #3399ff ==> **Base prompt color [hbf]**
pound = #3399ff ==> **Pound prompt color >**
module = #ff0000 bold **Selected module name color (baudrate)**
category = #ffffff **Selected module category color uart()**

```

## Contributing

Follow the guideline on the [CONTRIBUTING.md](CONTRIBUTING.md) files

## Thanks

I would like to thanks [@Nitr4x](https://github.com/Nitr4x) for his code review and ideas helping me to improve this framework.