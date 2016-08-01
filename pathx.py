from argparse import ArgumentParser, ArgumentTypeError
from winreg import HKEY_CURRENT_USER, HKEY_LOCAL_MACHINE, KEY_ALL_ACCESS, REG_SZ
from winreg import OpenKey, QueryValueEx, SetValueEx


def action(string):
    if string in ['APPEND', 'PREPEND', 'REMOVE']:
        return string
    raise ArgumentTypeError('Invalid Action')

parser = ArgumentParser(prog='pathx')
parser.add_argument('action',
                    type=action,
                    help='Action to preform on %%PATH%% (APPEND, PREPEND, REMOVE)')
parser.add_argument('pathname',
                    type=str,
                    help='Pathname to add to or remove from %%PATH%%')
parser.add_argument('-S', '--system',
                    action='store_true',
                    help='Preform action on system %%PATH%% instead of user %%PATH%%')
args = parser.parse_args()
registry_location = HKEY_CURRENT_USER
sub_key = 'Environment'
if args.system:
    registry_location = HKEY_LOCAL_MACHINE
    sub_key = 'SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment'
with OpenKey(registry_location, sub_key, access=KEY_ALL_ACCESS) as environment_key:
    path_value_list = QueryValueEx(environment_key, 'Path')[0].split(';')
    if args.action == 'APPEND':
        path_value_list.append(args.pathname)
    elif args.action == 'PREPEND':
        path_value_list = [args.pathname] + path_value_list
    elif args.action == 'REMOVE':
        path_value_list.remove(args.pathname)
    SetValueEx(environment_key, 'Path', 0, REG_SZ, ';'.join(path_value_list))
