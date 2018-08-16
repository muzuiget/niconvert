#!/usr/bin/env python3

import sys
import niconvert

if len(sys.argv) >= 2 and sys.argv[1] == 'tk':
    niconvert.run_tk()
elif sys.stdin and sys.stdin.isatty():
    niconvert.run_cli()
else:
    niconvert.run_tk()
