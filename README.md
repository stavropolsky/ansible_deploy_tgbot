# ansible_deploy_tgbot
Deploying a VM in Yandex.Cloud and deploying a Python application using ansible
1. Ansible must be installed on the server from which ansible-playbook will be launched, how to do this is described here - https://docs.ansible.com/ansible/latest/installation_guide/installation_distros.html

2. To deploy the server itself in Yandex.Cloud, a module was used - https://github.com/arenadata/ansible-module-yandex-cloud, for which you need to install https://github.com/yandex-cloud/python- sdk

   `pip install --user git+https://github.com/yandex-cloud/python-sdk`

3. Here and below, all paths and commands are indicated based on the fact that the current directory is the root directory of the project.

4. First, you need to edit the file `create_vm/vars/main.yml`, in it save all the variables that need to be transferred from Yandex.Cloud after registering with the service and creating folders and the internal network:

   token: how to get here https://cloud.yandex.ru/docs/iam/concepts/authorization/oauth-token
   user: The user that will be created when the server is deployed.
   folder_id: cloud folder identifier
   image_id: if you try to manually create a VM in Yandex.Cloud, there will be several operating systems of different versions available to choose from; when you select any OS, you can find out its image_id
   subnet_id: subnet identifier

5. Next, if necessary, you can edit the VM configuration file - `create_vm/tasks/main.yml`, specifying the required number of vcpu, vram, disk size, etc. The public IP address is assigned automatically, and it is dynamic. If you need a static one, then it must be reserved in the cloud web interface after creating the VM.

VM Deployment

1. To start VM deployment, use the command:

   `ansible-playbook playbook.yml --tags create_vm`

Setting up the server and launching the bot

1. If necessary, you can specify the Postgresql version in the `postgres/vars/main.yml` file.

2. In the file `deploy/vars/main.yml` we set the domain name, the root directory of the bot and the database password.

3. The `deploy/files` directory contains the bot files, and the `deploy/files/certs` directory contains certificates issued earlier. If necessary, it will be possible to re-release it after deployment, having previously linked the server IP to the domain name.
4. The `deploy/files/.env` file also contains important variables, such as the bot token, DATABASE_URL, etc.

5. The `deploy/templates` directory contains templates for future systemd daemons.

6. File with tasks for the deploy role - `deploy/tasks/main.yml`.

7. To start the deployment, use the following command:

   `ansible-playbook -i inventory.ini playbook.yml --tags postgres,deploy`
