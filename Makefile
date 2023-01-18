PACKAGE_NAME = my_package

all: clean build

clean:
	rm -rf build dist $(PACKAGE_NAME).egg-info

build:
	python setup.py sdist bdist_wheel

upload:
	twine upload dist/*