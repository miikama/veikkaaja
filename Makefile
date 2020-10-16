.PHONY: check
check:
	mypy --config-file .mypy.ini veikkaaja
	pylint --rcfile=.pylintrc veikkaaja