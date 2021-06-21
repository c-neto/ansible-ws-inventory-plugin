venv:
	virtualenv venv
	venv/bin/pip3 install ansible

build:
	venv/bin/ansible-galaxy collection build ansible-plugin/ws/

publish:
	venv/bin/ansible-galaxy collection publish *tar.gz --token=$(token)
