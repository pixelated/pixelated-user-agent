VIRTUALENV=~/.venvs/pixua

.PHONY=setup requirements install requirements_py requirements_js\
install_py install_js create_virtualenv \
test test_all linters coverage unit_tests integration_tests functional_tests\
clean ensure_virtualenv_installed ensure_phantomjs_installed

setup: requirements install

requirements: requirements_py requirements_js

install: install_py install_js
	@echo "Installing dependencies"

requirements_py: create_virtualenv
	@echo "Upgrading pip and setuptools"
	@source ~/.venvs/pixua/bin/activate;\
	pip install --upgrade pip setuptools

requirements_js:
	@echo "Installing js requirements"

install_py: service/requirements.txt service/test_requirements.txt
	@echo "Installing python packages"
	@source ~/.venvs/pixua/bin/activate;\
	cd service;\
	pip install --exists-action s -r requirements.txt -r test_requirements.txt

install_js:
	@echo "Installing javascript packages"

create_virtualenv: ensure_virtualenv_installed
	@if [ ! -e $(VIRTUALENV)/bin/activate ]; then\
		echo "Pixelated virtualenv doesn't exist, creating now";\
		virtualenv --python=python2 $(VIRTUALENV);\
	else\
    echo "Pixelated virtualenv already exists, moving on";\
	fi

test: clean requirements_py install_py linters coverage unit_tests integration_tests

test_all: test functional_tests

linters:
	@echo "Running pep8 and jshint"
	@source ~/.venvs/pixua/bin/activate;\
	cd service;\
	pep8 --ignore=E501 pixelated test
	@echo jshint pending

coverage:

unit_tests:
	@echo "Running python and javascript unit tests"
	-@source ~/.venvs/pixua/bin/activate;\
	cd service;\
	trial --reporter=text test.unit
	@echo js unit tests pending

integration_tests:
	@echo "Running integration tests"
	source ~/.venvs/pixua/bin/activate;\
	cd service;\
	trial -j`grep -c "^processor" /proc/cpuinfo || sysctl -n hw.logicalcpu` --reporter=text test.integration

functional_tests: ensure_phantomjs_installed
	@echo "Running behave functional tests"
	@source ~/.venvs/pixua/bin/activate;\
	cd service;\
	behave --tags ~@wip --tags ~@smoke test/functional/features

ensure_phantomjs_installed:
	@if [ ! `which phantomjs` ]; then\
		echo "You need phantomJS to run these tests";\
		exit 1;\
	fi

ensure_virtualenv_installed:
	@if [ ! `which virtualenv` ]; then\
		exit 1;\
	else\
	  echo "Virtualenv located at "`which virtualenv`;\
	fi

clean:
		@echo "Cleaning cache and temporary files"
		rm -rf ~/.config/leap
		rm -rf ~/.leap
		rm -rf service/_trial_temp
		find . -name "*.pyc" -delete
