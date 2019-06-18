#!/usr/bin/python
#   Copyright Red Hat, Inc. All Rights Reserved.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = '''
---
module: dlrn_run
short_description: Ansible module to run DLRN
version_added: "1.0"
author: "jpena <jpena@redhat.com>"
description:
    - Ansible module to run DLRN on systems deployed with puppet-dlrn
options:
    package_name:
        description:
            - List of packages to manage. If not set, it will run a full
              build. Note this can be a very time-consuming process, so you
              may need to adjust timeouts.
    recheck:
        description:
            - If set to true, recheck the specified package(s).
        default: false
    force_recheck:
        description:
            - If set to true, forcefully recheck the specified package(s).
              Note that this requires to set recheck to true, and the
              configuration option allow_force_rechecks must be set to true
              in the DLRN instance.
        default: false
'''

EXAMPLES = '''
# Build all packages
- dlrn_run:
  become: yes
  become_user: centos-master-uc

# Build a single package
- dlrn_run:
    package_name: openstack-nova
  become: yes
  become_user: centos-master-uc

# Build several packages
- dlrn_run:
    package_name:
        - openstack-nova
        - openstack-cinder
        - python-tripleoclient
  become: yes
  become_user: centos-master-uc

# Recheck two packages
- dlrn_run:
    package_name:
        - openstack-nova
        - openstack-cinder
    recheck: true
  become: yes
  become_user: centos-master-uc

# Forcefully recheck a package
- dlrn_run:
    package_name:
        - openstack-nova
    recheck: true
    force_recheck: true
  become: yes
  become_user: centos-master-uc
'''

from ansible.module_utils.basic import *


def run_dlrn_recheck(module, package_name, force_recheck):
    output = ""

    for pkg in package_name:
        command_line = ['run-dlrn.sh']
        command_line.extend(['--package-name'])
        command_line.extend(['%s' % pkg])
        command_line.extend(['--recheck'])
        if force_recheck:
            command_line.extend(['--force-recheck'])
        rc, stdout, stderr = module.run_command(command_line,
                                                path_prefix='/usr/local/bin')

        output += stdout + stderr
        if rc != 0:
            return rc, output

    return 0, output


def run_dlrn(module, args):
    package_name = None
    recheck = False
    force_recheck = False
    if args.get('package_name'):
        package_name = args.get('package_name')
    if args.get('recheck'):
        recheck = bool(args.get('recheck'))
    if args.get('force_recheck'):
        force_recheck = bool(args.get('force_recheck'))

    if force_recheck and not recheck:
        return 1, "force_recheck: True requires recheck: True"

    if recheck:
        errno, output = run_dlrn_recheck(module, package_name, force_recheck)
        return errno, output

    command_line = ['run-dlrn.sh']
    for pkg in package_name:
        command_line.extend(['--package-name'])
        command_line.extend(['%s' % pkg])

    rc, stdout, stderr = module.run_command(command_line,
                                            path_prefix='/usr/local/bin')

    return rc, stdout + stderr


def main():
    fields = {
        'package_name': {"required": False, "type": "list"},
        'recheck': {"required": False, "default": False, "type": "bool"},
        'force_recheck': {"required": False, "default": False, "type": "bool"},
    }

    module = AnsibleModule(argument_spec=fields)
    errno, output = run_dlrn(module, module.params)

    if errno == 0:
        module.exit_json(changed=True, meta=output)
    else:
        module.fail_json(msg='Error running DLRN', meta=output)


if __name__ == '__main__':
    main()
