#!/usr/bin/env python
"""
Nagios/icinga plugin for checking a redis server.

Author: Bartek Jakubowski <bartekj@gmail.com>
License: GPL2
"""
import argparse
import nagiosplugin
import redis


class check_redis(nagiosplugin.Resource):

    def __init__(self, host, port=6379, password=None, warn=None, crit=None, timeout=300, check_type=None):
        self.host = host
        self.port = port
        self.password = password
        self.warn = warn
        self.crit = crit
        self.timeout = timeout
        self.check_type = check_type
        self._fetchInfo()

    def _fetchInfo(self):
        try:
            self.info = redis.Redis(host=self.host, port=self.port,
                                    password=self.password).info()
        except redis.ConnectionError:
            raise nagiosplugin.CheckError("Can't connect to %s:%s" % (self.host, self.port))

    def get_connected_clients(self):
        return self.info['connected_clients']

    def get_connected_slaves(self):
        return self.info['connected_slaves']

    def get_used_mem(self):
        return "%.0f" % float(self.info['used_memory'] / 1024.0 / 1024.0)

    def probe(self):
        if self.check_type == 'mem':
            return nagiosplugin.Metric('memory', int(self.get_used_mem()), "MB", context='mem', min=0)
        elif self.check_type == 'clients':
            return nagiosplugin.Metric('clients_connected', int(self.get_connected_clients()), context='clients', min=0)
        elif self.check_type == 'slaves':
            return nagiosplugin.Metric('slaves', int(self.get_connected_slaves()), context='slaves', min=0)


def main():
    parser = argparse.ArgumentParser(
        __file__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=('Redis server check for icinga/nagios written in python'),
        epilog='Copyright (C) 2015 Bart Jakubowski <bartekj@gmail.com>'
    )
    parser.add_argument("-t", "--check_type", help="check type", choices=["mem", "clients", "slaves"],
                        required=True)
    parser.add_argument("-H", "--server", dest="server", help="Redis server", default="127.0.0.1")
    parser.add_argument("-p", "--port", dest="port", help="Redis port", default=6379)
    parser.add_argument("-w", "--warn", dest="warn", help="WARNING trigger", required=True)
    parser.add_argument("-c", "--crit", dest="crit", help="CRITICAL triger", required=True)
    parser.add_argument("-T", "--timeout", dest="timeout", help="milliesconds to wait before timing out",
                        default=300)
    parser.add_argument('-v', '--version', help='Print version', action='version', version='%(prog)s 1.0')
    args = parser.parse_args()

    check = nagiosplugin.Check(check_redis(host='localhost',
                                           check_type=args.check_type,
                                           warn=args.warn,
                                           crit=args.crit),
                               nagiosplugin.ScalarContext(args.check_type, args.warn, args.crit))
    check.main()

if __name__ == '__main__':
    main()
