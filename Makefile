test:
	coverage run -m pytest --ds=task_manager.main.test.django_test_settings.test_settings -vv -s
	coverage report
	coveralls