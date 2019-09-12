[![Build Status](https://travis-ci.org/hydrabus-framework/framework.svg?branch=master)](https://travis-ci.org/hydrabus-framework/framework) [![Python 3.6|3.7|3.7-dev](https://img.shields.io/badge/python-3.6|3.7-blue.svg)](https://www.python.org/) [![License](https://img.shields.io/badge/license-GPLv3-important.svg)](https://github.com/hydrabus-framework/framework/master/LICENSE.md)

# hydrabus-framework [v0.0.1]

## Description

This project is a framework around the [hydrabus project](https://hydrabus.com/).
It provides multiple modules allowing you to work efficiently and save time on any hardware project.

[![asciicast](https://asciinema.org/a/z9iBJsZMsDmSB94TiYWRrctKi.svg)](https://asciinema.org/a/z9iBJsZMsDmSB94TiYWRrctKi)

## Installation

Clone this repository or get the latest release, then :

```
python3 setup.py install
```

## Usage

This framework work like metasploit. Simply run hbfconsole, load any available modules and enjoy!

## Use Docker image

### Build the image

```
docker build -t hbf .
```

### Run the instance

```
docker run --rm -it -v /local/folder/:/remote/folder --device=/dev/ttyACM0:/dev/hydrabus hbf
```

Please run `hbfupdate` in order to install available modules before running `hbfconsole`

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

## FAQ

* How to list available modules ?

``` [hbf] > show modules ```

* What's a global options ?

A global option is an option who will be used for every module loaded.
Setting the options with the `setg` command will set the specified options globally for every module loaded.
Unset a specific global option with `unsetg` command.
It is also possible to print the previously defined global using `show global` command.

* Can you give me a typical example of use?

You identify an SPI flash chip on a hardware device. You want to dump his memory.
Simply run `hbfconsole` from a shell and follow these instructions :

1. List available module:

```[hbf] > show modules```

2. Select the correct module:

```[hbf] > use spi/dump_eeprom```

3. Show available options

```[hbf] spi(dump_eeprom) > show options```

4. Set necessary options

```[hbf] spi(dump_eeprom) > set dump_file dump.bin```

5. Run the module

```[hbf] spi(dump_eeprom) > run```

* How to properly remove the framework along with installed modules?

Coming soon