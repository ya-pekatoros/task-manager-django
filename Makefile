test:
	docker-compose exec api pytest --ds=task_manager.main.test.django_test_settings.test_settings -vv