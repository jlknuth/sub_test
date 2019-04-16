import json
import os
import urllib.request
from urllib.error import HTTPError
from ssl import SSLError
from collections import defaultdict

git_dir = os.path.join(os.path.expanduser('~'), 'Downloads', 'package_control_channel')
pkg_path_tmp = os.path.join(os.path.expanduser('~'), 'sublime_packages')
# pkg_path = os.path.join('/data', 'sublime_packages')
pkg_path = os.path.join('https://0.0.0.0:4443', 'sublime_packages')

def fix_pkg(pkg):
    try:
        name = pkg['name']
    except KeyError:
        name = os.path.basename(pkg['details'])

    new_path = os.path.join(pkg_path, '_'.join(name.split(' ')))
    old_path = pkg['details']
    pkg['details'] = new_path

    return (name, new_path, old_path)

channel_file = os.path.join(git_dir, 'channel.json')
rep_folder = os.path.join(git_dir, 'repository')

repo_files = []


# with open(os.path.join(rep_folder, '0-9.json'), 'r') as fid:
#     json_data = json.load(fid)

# with open(channel_file, 'r') as fid:
#     data = json.load(fid)
# cnt = 0
# new_json_rep = defaultdict(list)
# for rep in data['repositories']:
#     cnt += 1
#     print('{}/{}'.format(cnt, len(data['repositories'])))
#     if rep[:4] == 'http':
#         try:
#             response = urllib.request.urlopen(rep)
#             html = response.read()
#             JSON_object = json.loads(html)
#         except HTTPError:
#             pass
#         except SSLError:
#             pass
#         except:
#             pass
#         else:
#             # new_json_rep.append(JSON_object)
#             new_json_rep[JSON_object['schema_version']].extend(JSON_object['packages'])

# new_json = {}
# new_json['schema_version'] = data['schema_version']


# with open(urllib.request.urlopen(rep)) as fid:
    # pass

pkg_paths = {}
for _file0 in os.listdir(rep_folder):
    _file = os.path.join(rep_folder, _file0)
    with open(_file, 'r') as fid:
        json_data = json.load(fid)
    for pkg in json_data['packages']:
        try:
            name, new_path, old_path = fix_pkg(pkg)
        except:
            import pudb; pudb.set_trace()
        pkg_paths[name] = old_path

        with open(_file, 'w') as fid:
            json.dump(json_data, fid)


pkg_list = ['Julia']
# Now grad any packages in the path

if not os.path.exists(pkg_path_tmp):
    os.mkdir(pkg_path_tmp)

for pkg_name in pkg_list:
    if pkg_name not in pkg_paths:
        raise Exception('Could not find package {}.'.format(pkg_name))

    old_path = pkg_paths[pkg_name]
    new_path = os.path.join(pkg_path_tmp, pkg_name)
    if os.path.exists(new_path):
        os.system('cd {}; git remote set-url origin {}; git fetch'.format(new_path, old_path))
    else:
        os.system('git clone --mirror {} {}'.format(old_path,new_path))

import pudb; pudb.set_trace()
print('hi')
