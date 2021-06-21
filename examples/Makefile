venv:
	virtualenv venv
	venv/bin/pip3 install -r requirements.txt

run:
	venv/bin/ansible-playbook -i ws-inventory.yml playbook-main.yml
