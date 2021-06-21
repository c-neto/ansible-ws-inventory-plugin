venv:
	virtualenv venv
	venv/bin/pip3 install -r requirements.txt

containers:
	venv/bin/docker-compose pull 
	venv/bin/docker-compose up -d

playbook:
	venv/bin/ansible-playbook -i ws-inventory.yml playbook-main.yml --ask-pass

devel:
	docker-compose -f docker-compose-devel.yml up --build -d
