"""
usage: pathx [-h] [-S] action pathname

positional arguments:
  action        Action to preform on %PATH% (APPEND, PREPEND, REMOVE)
  pathname      Pathname to add to or remove from %PATH%

optional arguments:
  -h, --help    show this help message and exit
  -S, --system  Preform action on system %PATH% instead of user %PATH%
"""

from argparse import ArgumentParser, ArgumentTypeError
from os.path import exists as path_exists
from winreg import HKEY_CURRENT_USER, HKEY_LOCAL_MACHINE, KEY_ALL_ACCESS, REG_SZ
from winreg import OpenKey, QueryValueEx, SetValueEx


def action(string):
    if string in ['APPEND', 'PREPEND', 'REMOVE']:
        return string
    raise ArgumentTypeError('Invalid Action')


def directory(string):
    if path_exists(string):
        return string
    raise ArgumentTypeError('Invalid Directory')

if __name__ == '__main__':
    parser = ArgumentParser(prog='pathx')
    parser.add_argument('action',
                        type=action,
                        help='action to preform on %%PATH%% (APPEND, PREPEND, REMOVE)')
    parser.add_argument('pathname',
                        type=directory,
                        help='pathname to add to or remove from %%PATH%%')
    parser.add_argument('-S', '--system',
                        action='store_true',
                        help='preform action on system %%PATH%% instead of user %%PATH%%')
    args = parser.parse_args()
    registry_location = HKEY_CURRENT_USER
    sub_key = 'Environment'
    if args.system:
        registry_location = HKEY_LOCAL_MACHINE
        sub_key = 'SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment'
    with OpenKey(registry_location, sub_key, access=KEY_ALL_ACCESS) as environment_key:  # open registry location
        path_value_list = QueryValueEx(environment_key, 'Path')[0].split(';')            # get and split values in current path value
        try:
            path_value_list.remove(args.pathname)  # removes the pathname from the current path value
        except Exception:
            pass
        finally:
            if args.action == 'APPEND':
                path_value_list.append(args.pathname)  # appends pathname to path
            elif args.action == 'PREPEND':
                path_value_list = [args.pathname] + path_value_list  # prepend pathname to path
        SetValueEx(environment_key, 'Path', 0, REG_SZ, ';'.join(path_value_list))  # write path back to registry
