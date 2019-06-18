# ansible-module-dlrn-run
Ansible module to run DLRN on systems deployed with puppet-dlrn

This Ansible module is designed to run certain DLRN operations on systems
deployed using <https://github.com/rdo-infra/puppet-dlrn>.

## Installation

Just place the library/ folder on the same directory as your playbook, or
copy the library/dlrn_run.py somewhere in your Ansible module path.

## Example playbooks

Build all packages

```yaml
- dlrn_run:
  become: yes
  become_user: centos-master-uc
```

Build a single package

```yaml
- dlrn_run:
    package_name: openstack-nova
  become: yes
  become_user: centos-master-uc
```

Build several packages

```yaml
- dlrn_run:
    package_name:
        - openstack-nova
        - openstack-cinder
        - python-tripleoclient
  become: yes
  become_user: centos-master-uc
```

Recheck two packages

```yaml
- dlrn_run:
    package_name:
        - openstack-nova
        - openstack-cinder
    recheck: true
  become: yes
  become_user: centos-master-uc
```

Forcefully recheck a package

```yaml
- dlrn_run:
    package_name:
        - openstack-nova
    recheck: true
    force_recheck: true
  become: yes
  become_user: centos-master-uc
```

Note that, to forcefully recheck a package, you need to set
allow_force_rechecks=True in the builder's projects.ini file.

## License

Apache 2.0

## Author

* Javier Peña ([@fj_pena](https://github.com/javierpena))
