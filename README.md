# check_redis
Nagios/icinga plugin for checking a redis server
##Requirements
This script is based on python nagiosplugin class and redis module.
To setisfy requirements please run `pip install -r requirements.txt`

##Usage
```
usage: ./check_redis.py [-h] -t {mem,clients,slaves} [-H SERVER] [-p PORT] -w
                        WARN -c CRIT [-T TIMEOUT] [-v]

Redis server check for icinga/nagios written in python

optional arguments:
  -h, --help                                                    show this help message and exit
  -t {mem,clients,slaves}, --check_type {mem,clients,slaves}    check type
  -H SERVER, --server SERVER                                    Redis server
  -p PORT, --port PORT                                          Redis port
  -w WARN, --warn WARN                                          WARNING trigger
  -c CRIT, --crit CRIT                                          CRITICAL triger
  -T TIMEOUT, --timeout TIMEOUT                                 milliesconds to wait before timing out
  -v, --version                                                 Print version

Copyright (C) 2015 Bart Jakubowski <bartekj@gmail.com>
```
