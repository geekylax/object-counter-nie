run_postgres:
	docker compose up -d 
lock_pip: requirements.txt
	@test -d .venv || (echo " No virtual environemnt; use this command to create a venv 'python3 -m venv .venv' " && exit 1);
	source .venv/bin/activate; pip freeze | xargs --no-run-if-empty pip uninstall -y;
	pip install -r requirements.txt;
	pip freeze > requirements.lock.txt