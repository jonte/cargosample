#!/usr/bin/env python3

# Copyright 2018 Jussi Pakkanen

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import subprocess, sys, os
import pathlib

cargo_url_templ = "https://crates.io/api/v1/crates/%s/%s/download"

header_templ = '''project('%s', 'rust', version : '%s')

'''

target_templ = '''%s_lib = static_library('%s',
  '%s')

'''

dep_templ = '''%s_dep = declare_dependency(link_with : %s_lib)\n'''

def get_crate_repo_url(crate_name, crate_version):
    return cargo_url_templ % (crate_name, crate_version)

def unpack_crate(spdir, crate_file_path, crate_dir_name):
    outdir = spdir / crate_dir_name
    if outdir.exists():
        print('Output path %s already exists, not doing a checkout.' % outdir)
        return outdir

    subprocess.check_call(['tar', 'xf', crate_file_path,
        '--one-top-level=%s' % crate_dir_name], cwd=spdir)

    return outdir

def create_checkout(crate_name, crate_version):
    spdir = pathlib.Path('subprojects')
    crates_dir = spdir / 'crates'
    crate_dir_name = '%s-%s' % (crate_name, crate_version)
    crate_file_path = (crates_dir / (crate_dir_name + '.crate')).resolve()
    crate_url = get_crate_repo_url(crate_name, crate_version)

    crates_dir.mkdir(exist_ok = True)
    subprocess.check_call(['curl', '-sL', crate_url, '-o', crate_file_path])

    return unpack_crate(spdir, crate_file_path, crate_dir_name)


def create_mesonfiles(crate_name, crate_version, outdir):
    mfile = outdir / 'meson.build'
    with mfile.open('w') as ofile:
        ofile.write(header_templ % (crate_name, crate_version))
        ofile.write(target_templ % (crate_name,
                                    crate_name,
                                    'src/lib.rs'))
        ofile.write(dep_templ % (crate_name, crate_name))

def convert_single(crate_name, crate_version):
    outdir = create_checkout(crate_name, crate_version)
    create_mesonfiles(crate_name, crate_version, outdir)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(sys.argv[0] + ' <name of dependency> <version of dependency>')
    (name, version) = sys.argv[1:]
    if not os.path.exists('subprojects'):
        sys.exit('Subprojects directory does not exist.')
    convert_single(name, version)
