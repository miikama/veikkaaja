
.PHONY: type-check
type-check:
	mypy --config-file .mypy.ini veikkaaja

.PHONY: lint
lint:
	pylint --rcfile=.pylintrc veikkaaja

.PHONY: check
check: lint type-check