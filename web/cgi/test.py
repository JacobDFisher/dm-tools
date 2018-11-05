#!/usr/bin/env python3

import sys
import cgi, cgitb
#import redis

def main():
    form = cgi.FieldStorage()
    print("Content-Type: text/html")
    print()
    print(sys.version)

main()
