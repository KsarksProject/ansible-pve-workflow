# ansible-pve-workflow

Example of Ansible AWX and Proxmox VE workflow playbooks

## Ansible AWX usage

1. Create project with this repository
2. Create job templates with survey as examples/extra_vars
3. Create workflow templates as like `wf_*.yaml`

### Import templates by awx-cli

```
$ pip install awxkit==17.0.1
$ awx --conf.host http://${AWX_IP} --conf.username ${AWX_ADMIN_USER} --conf.password ${AWX_ADMIN_PASSWORD} login
{
     "token": "lB25nRgh9PSu6vSLgoE0sDL40K56lI"
}
$ export AWX_TOKEN=lB25nRgh9PSu6vSLgoE0sDL40K56lI
$ sed -i -e "s/ainoniwa.net/${YOUR_ORGANIZATION}" job_templates/*
$ sed -i -e "s/ainoniwa.net/${YOUR_ORGANIZATION}" wf_templates/*
$ awx --conf.host http://${AWX_IP} --conf.token ${AWX_TOKEN} import < job_templates/pve_qemu_clone.json
$ awx --conf.host http://${AWX_IP} --conf.token ${AWX_TOKEN} import < job_templates/pve_qemu_config.json
$ awx --conf.host http://${AWX_IP} --conf.token ${AWX_TOKEN} import < job_templates/pve_qemu_start.json
$ awx --conf.host http://${AWX_IP} --conf.token ${AWX_TOKEN} import < job_templates/pve_qemu_stop.json
$ awx --conf.host http://${AWX_IP} --conf.token ${AWX_TOKEN} import < job_templates/pve_qemu_delete.json
$ awx --conf.host http://${AWX_IP} --conf.token ${AWX_TOKEN} import < wf_templates/vm_service_start.json
$ awx --conf.host http://${AWX_IP} --conf.token ${AWX_TOKEN} import < wf_templates/vm_service_config_vm.json
$ awx --conf.host http://${AWX_IP} --conf.token ${AWX_TOKEN} import < wf_templates/vm_service_start_vm.json
$ awx --conf.host http://${AWX_IP} --conf.token ${AWX_TOKEN} import < wf_templates/vm_service_stop_vm.json
$ awx --conf.host http://${AWX_IP} --conf.token ${AWX_TOKEN} import < wf_templates/vm_service_terminate.json
```

## Local testings

### Install ansible

```
$ git clone https://github.com/ainoniwa/ansible-pve-workflow
$ cd ansible-pve-workflow
$ python3 -m venv ~/.virtualenvs/$(basename ${PWD})
$ source ~/.virtualenvs/$(basename ${PWD})/bin/activate
$ pip install -r requirements.txt
$ ansible-galaxy install -r roles/requirements.yml
```

### Setting variables

1. Set proxmox VE API environments.

```
export PVE_API_ENDPOINT="https://pve.example.com"
export PVE_API_USERNAME="root@pam"
export PVE_API_PASSWORD="pve-password"
```

2. Edit `pve_templates.yaml` for template image and template name mappings.

For example, if the VM template name `centos7` and vmid `9001`, then edit as below.

```yaml
---
centos7: 9001
```

3. Edit `extra_vars/example.yaml` to local testings.

If uses Ansible Tower or AWX, to use survey instead of `-e @extra_vars/example.yaml`.

### Run playbook

The `wf_*.yaml` playbooks like a ansible tower workflow job template.

Run:

```
# Clone VM
ansible-playbook -e @extra_vars/example.yaml wf_qemu_clone.yaml
# Terminate VM
ansible-playbook -e @extra_vars/example.yaml wf_qemu_terminate.yaml
```

### Run playbook with zabbix setup tasks

```
# Clone VM and install zabbix-agent
ansible-playbook -e @extra_vars/example_zabbix.yaml -i pve_inventory.py wf_qemu_clone_and_zabbix.yaml
# Terminate VM and remove zabbix-host entry
ansible-playbook -e @extra_vars/example_zabbix.yaml -i pve_inventory.py wf_qemu_terminate_and_zabbix.yaml
```

