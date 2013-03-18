#!/usr/bin/env python
import ConfigParser, os
import argparse
import scrapinghub

def list_spiders(args, conn):
    project = conn[str(args.project)]
    fmt = lambda a, b, c: "| %s | %s | %s |" % (a.ljust(60), b.ljust(10), c.ljust(20))
    if args.extended_info:
        s = fmt("name", "type", "version")
        print s
        print "-" * len(s)
        for item in project.spiders():
            print fmt(item['id'], item['type'], item['version'])
        print "-" * len(s)
    else:
        for item in project.spiders():
            print item['id']

def main():
    config = ConfigParser.ConfigParser()
    config.read([os.path.expanduser('~/.scrapy.cfg')])
    username = config.get("deploy", "username")
    password = config.get("deploy", "password")
    try:
        project_id = config.get("deploy", "project")
    except ConfigParser.NoOptionError:
        project_id = None

    conn = scrapinghub.Connection(username, password)

    parser = argparse.ArgumentParser(prog='shub-cli')
    parser.add_argument('-p', '--project',
        help='scrapinghub project id', 
        default=project_id)

    subparsers = parser.add_subparsers(dest='subcommand')

    parser_listspiders = subparsers.add_parser('list-spiders')
    parser_listspiders.add_argument('-E', '--extended-info',
        help='show extended information about spiders',
        action='store_true')
    args = parser.parse_args()

    if args.subcommand == 'list-spiders':
        list_spiders(args, conn)
    else:
        parser.error("unknown command")

if __name__ == '__main__':
    main()
