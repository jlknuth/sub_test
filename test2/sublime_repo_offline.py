import json
import os
import urllib.request
from urllib.error import HTTPError
from ssl import SSLError
from collections import defaultdict

def safe_mkdir(_dir):
    if (not os.path.exists(_dir)):
        os.makedirs(_dir)


dir_path = os.path.dirname(os.path.realpath(__file__))
pkg_location = 'http://127.0.0.1:8000/'

channel_file = os.path.join(dir_path, 'channel_v3.json')
channel_url = 'https://packagecontrol.io/channel_v3.json'
os.system('cd {}; pwd; curl -O {}'.format(dir_path, channel_url))

package_cache_file = os.path.join(dir_path, 'package_cache.json')
channel_file_local = os.path.join(dir_path, 'channel_v3_local.json')

# response = urllib.request.urlopen(channel_url)
# html = response.read()
# JSON_object = json.loads(html)

# pkg_location = 'http://0.0.0.0:8000/test2'

# package_cache = {'PackageList': ['Julia'], 'Cache': {}}
# with open(package_cache_file, 'w') as fid:
#     json.dump(package_cache, fid)

with open(package_cache_file, 'r') as fid:
    package_cache = json.load(fid)

with open(channel_file, 'r') as fid:
    channel = json.load(fid)


pkg_to_add = []

kept_reps  = []

for rep_key, reps in channel['packages_cache'].items():
    new_reps = []
    channel['packages_cache'][rep_key] = new_reps
    for rep in reps:
        name = rep['name']
        if name in package_cache['PackageList']:
            new_reps.append(rep)
            releases = rep['releases']
            if name == 'pygments':
                import pudb; pudb.set_trace()
            for releas in releases:
                key = str(sorted(releas.items()))
                url = releas['url']
                _, pth = url.split('//')
                pth = '_'.join(pth.split('.'))
                pth = '_'.join(pth.split(' '))
                file_name = os.path.basename(url)
                pkg_pth_rel = os.path.join('packages', os.path.dirname(pth))
                new_url = os.path.join(pkg_location, pkg_pth_rel, file_name)
                releas['url'] = new_url

                # Now download the package
                if name not in package_cache['Cache']:
                    package_cache['Cache'][name] = []

                if key not in package_cache['Cache'][name]:
                    package_cache['Cache'][name].append(key)
                    rel_path = os.path.join(dir_path, pkg_pth_rel)
                    safe_mkdir(rel_path)
                    url = '%20'.join(url.split(' '))
                    os.system('cd {}; curl -O {}; pwd'.format(rel_path, url))

    # if len(new_reps) > 0:
    # if True:
    #     kept_reps.append(rep_key)

# Get the dependencies
for rep_key, reps in channel['dependencies_cache'].items():
    # try:
    #     rep = channel['dependencies_cache'][rep_key]
    # except KeyError:
    #     continue

    for rep in reps:
        name = rep['name']
        releases = rep['releases']
        for releas in releases:
            key = str(sorted(releas.items()))
            url = releas['url']
            _, pth = url.split('//')
            pth = '_'.join(pth.split('.'))
            pth = '_'.join(pth.split(' '))
            file_name = os.path.basename(url)
            pkg_pth_rel = os.path.join('packages', os.path.dirname(pth))
            new_url = os.path.join(pkg_location, pkg_pth_rel, file_name)
            releas['url'] = new_url

            # Now download the package
            if name not in package_cache['Cache']:
                package_cache['Cache'][name] = []

            if key not in package_cache['Cache'][name]:
                package_cache['Cache'][name].append(key)
                rel_path = os.path.join(dir_path, pkg_pth_rel)
                safe_mkdir(rel_path)
                url = '%20'.join(url.split(' '))
                os.system('cd {}; curl -O {}; pwd'.format(rel_path, url))


with open(channel_file_local, 'w') as fid:
    json.dump(channel, fid)

with open(package_cache_file, 'w') as fid:
    json.dump(package_cache, fid)


# git_dir = os.path.join(os.path.expanduser('~'), 'Downloads', 'package_control_channel')
# pkg_path_tmp = os.path.join(os.path.expanduser('~'), 'sublime_packages')
# # pkg_path = os.path.join('/data', 'sublime_packages')
# pkg_path = os.path.join('https://0.0.0.0:4443', 'sublime_packages')

# def fix_pkg(pkg):
#     try:
#         name = pkg['name']
#     except KeyError:
#         name = os.path.basename(pkg['details'])

#     new_path = os.path.join(pkg_path, '_'.join(name.split(' ')))
#     old_path = pkg['details']
#     pkg['details'] = new_path

#     return (name, new_path, old_path)

# channel_file = os.path.join(git_dir, 'channel.json')
# rep_folder = os.path.join(git_dir, 'repository')

# repo_files = []


# # with open(os.path.join(rep_folder, '0-9.json'), 'r') as fid:
# #     json_data = json.load(fid)

# # with open(channel_file, 'r') as fid:
# #     data = json.load(fid)
# # cnt = 0
# # new_json_rep = defaultdict(list)
# # for rep in data['repositories']:
# #     cnt += 1
# #     print('{}/{}'.format(cnt, len(data['repositories'])))
# #     if rep[:4] == 'http':
# #         try:
# #             response = urllib.request.urlopen(rep)
# #             html = response.read()
# #             JSON_object = json.loads(html)
# #         except HTTPError:
# #             pass
# #         except SSLError:
# #             pass
# #         except:
# #             pass
# #         else:
# #             # new_json_rep.append(JSON_object)
# #             new_json_rep[JSON_object['schema_version']].extend(JSON_object['packages'])

# # new_json = {}
# # new_json['schema_version'] = data['schema_version']


# # with open(urllib.request.urlopen(rep)) as fid:
#     # pass

# pkg_paths = {}
# for _file0 in os.listdir(rep_folder):
#     _file = os.path.join(rep_folder, _file0)
#     with open(_file, 'r') as fid:
#         json_data = json.load(fid)
#     for pkg in json_data['packages']:
#         try:
#             name, new_path, old_path = fix_pkg(pkg)
#         except:
#             import pudb; pudb.set_trace()
#         pkg_paths[name] = old_path

#         with open(_file, 'w') as fid:
#             json.dump(json_data, fid)


# pkg_list = ['Julia']
# # Now grad any packages in the path

# if not os.path.exists(pkg_path_tmp):
#     os.mkdir(pkg_path_tmp)

# for pkg_name in pkg_list:
#     if pkg_name not in pkg_paths:
#         raise Exception('Could not find package {}.'.format(pkg_name))

#     old_path = pkg_paths[pkg_name]
#     new_path = os.path.join(pkg_path_tmp, pkg_name)
#     if os.path.exists(new_path):
#         os.system('cd {}; git remote set-url origin {}; git fetch'.format(new_path, old_path))
#     else:
#         os.system('git clone --mirror {} {}'.format(old_path,new_path))

# import pudb; pudb.set_trace()
# print('hi')
