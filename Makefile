VIRTUALENV=~/.venvs/pixua

.PHONY: setup requirements install requirements_py install_py requirements_js install_js create_virtualenv
.PHONY: test test_py test_js test_all linters linters_py linters_js coverage unit_tests_py unit_tests_js
.PHONY: integration_tests_py functional_tests functional_tests_ci ensure_virtualenv_installed clean
.PHONY: clean_all clean_py clean_js clean_cache remove_virtualenv remove_javascript_packages run
setup: install

requirements: requirements_py requirements_js

install: requirements install_py install_js

requirements_py: create_virtualenv
	@. $(VIRTUALENV)/bin/activate;\
	pip install --upgrade pip setuptools

install_py: service/requirements.txt service/test_requirements.txt
	@. $(VIRTUALENV)/bin/activate;\
	cd service;\
	pip install pysqlcipher --upgrade --force-reinstall --install-option="--bundled";\
	pip install --exists-action s -r requirements.txt -r test_requirements.txt

requirements_js:
	@cd web-ui;\
	npm install --production;\
	npm install;\
	node_modules/.bin/bower install

install_js:
	@cd web-ui;\
	npm rebuild node-sass;\
	npm run build

create_virtualenv: ensure_virtualenv_installed
	@if [ ! -e $(VIRTUALENV)/bin/activate ]; then\
		echo "Pixelated virtualenv doesn't exist, creating now";\
		virtualenv --python=python2 $(VIRTUALENV);\
	fi

test: clean install test_py test_js coverage
test_py: linters_py unit_tests_py integration_tests_py
test_js: linters_js unit_tests_js
test_all: test functional_tests
linters: clean install linters_py linters_js

linters_py:
	@. $(VIRTUALENV)/bin/activate;\
	cd service;\
	pep8 --ignore=E501 pixelated test

linters_js:
	@cd web-ui;\
	npm run lint

coverage:
	@. $(VIRTUALENV)/bin/activate;\
	cd service;\
	export PYTHONPATH=$(PYTHONPATH):`pwd`;\
	coverage run -p --source=pixelated `which trial` test.unit;\
	coverage run -p --source=pixelated `which trial` test.integration;\
	coverage combine;\
	coverage html

unit_tests_py:
	@. $(VIRTUALENV)/bin/activate;\
	cd service;\
	export PYTHONPATH=$(PYTHONPATH):`pwd`;\
	trial --reporter=text test.unit

unit_tests_js:
	@cd web-ui;\
	npm run test

integration_tests_py:
	@. $(VIRTUALENV)/bin/activate;\
	cd service;\
	export PYTHONPATH=$(PYTHONPATH):`pwd`;\
	trial --reporter=text test.integration

functional_tests: clean requirements install
	@. $(VIRTUALENV)/bin/activate;\
	cd service;\
	xvfb-run --server-args="-screen 0 1280x1024x24" behave --tags ~@wip --tags ~@smoke test/functional/features

smoke_tests: clean install
	@. $(VIRTUALENV)/bin/activate;\
	cd service;\
	xvfb-run --server-args="-screen 0 1280x1024x24" behave --tags ~@wip --tags @smoke test/functional/features -k -D host=$(provider)

functional_tests_ci: clean requirements install
	@. $(VIRTUALENV)/bin/activate;\
	cd service;\
	behave --tags ~@wip --tags ~@smoke test/functional/features

functional_tests_wip:
	@. $(VIRTUALENV)/bin/activate;\
	cd service;\
	xvfb-run --server-args="-screen 0 1280x1024x24" behave --tags @wip test/functional/features

ensure_virtualenv_installed:
	@if [ ! `which virtualenv` ]; then\
		echo "Virtualenv must be installed";\
		exit 1;\
	fi

clean: clean_py clean_js clean_cache
clean_all: clean remove_javascript_packages remove_virtualenv

clean_py:
	rm -rf service/_trial_temp
	find . -name "*.pyc" -delete
	rm -rf service/.coverage
	rm -rf service/htmlcov

clean_js:
	rm -rf web-ui/dist
	rm -rf web-ui/.sass-cache

clean_cache:
	rm -rf ~/.config/leap
	rm -rf ~/.leap
	rm -rf service/ghostdriver.log

remove_virtualenv:
	rm -rf $(VIRTUALENV)

remove_javascript_packages:
	rm -rf web-ui/node_modules
	rm -rf web-ui/app/bower_components

diagrams:
	@. $(VIRTUALENV)/bin/activate;\
	pip install plantuml;\
	cd service/diagrams/png;\
	python -m plantuml *.txt

run:
	@. $(VIRTUALENV)/bin/activate;\
	pixelated-user-agent --host 0.0.0.0 --multi-user --provider=$(provider)
