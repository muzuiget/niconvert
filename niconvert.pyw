#!/usr/bin/env python3

import sys


def run_cli():
    from niconvert.fndcli.main import main
    main()


def run_tk():
    from niconvert.fndtk.main import main
    main()


if len(sys.argv) >= 2 and sys.argv[1] == 'tk':
    run_tk()
elif sys.stdin and sys.stdin.isatty():
    run_cli()
else:
    run_tk()
