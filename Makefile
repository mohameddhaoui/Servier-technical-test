ifndef ENV
	environment = dev
else
	environment = ${ENV}
endif



.PHONY: requirements
requirements:
	pip install -r requirements-dev.txt

unit_tests:
	PYTHONPATH=`pwd` pytest -s --disable-warnings -vv tests/unit_test/

format:
	yapf -p -r src/ entrypoint/ -i --style='{based_on_style: google, column_limit: 100}'
	# yapf -i config.py


init_pipeline:
	find ./data/exposition/ -type f -print0| xargs -0 rm  && find ./data/quarantine/ -type f -print0| xargs -0 rm && find ./data/preprocessed/ -type f -print0| xargs -0 rm

run_pipeline:
	PYTHONPATH=. python3 bin/run_drugs_relations_pipeline.py
