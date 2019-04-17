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


