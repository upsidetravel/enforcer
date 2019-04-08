circleci := ${CIRCLECI}
current_dir := $(shell pwd)
image_name := $(shell git remote show origin | grep -e 'Push.*URL.*github.com' | rev | cut -d '/' -f 1 | rev | cut -d '.' -f 1)

define create_volume
$(call delete_volume,$(1))
docker volume create $(1)
endef

define delete_volume
$(call unmount_volume,$(1))
docker volume rm $(1) > /dev/null 2>&1 || true
endef

define mount_volume
docker create --mount source=$(1),target=$(2) --name $(1) alpine:3.4 /bin/true
endef

define unmount_volume
docker rm -f $(1) > /dev/null 2>&1 || true
endef

lint:
	@flake8 . --ignore=F403 &&\
		python -m pip install pip-licenses &&\
		(cat .licenseignore | sed 's/^[[:space:]]*$$/__nonexistent__/' > /tmp/licenseignore) &&\
		pip-licenses | grep -vf /tmp/licenseignore | (! grep -w GPL)

test:
	$(MAKE) lint
	tox

install:
	python setup.py develop

release:
	@python setup.py sdist bdist_wheel upload -r local

clean:
	@find . -name '*.pyc' -exec rm -f {} \;
	@find . -name '__pycache__' -exec rm -rf {} \;
	@find . -name 'Thumbs.db' -exec rm -f {} \;
	@find . -name '*~' -exec rm -f {} \;

snyk:
	$(call create_volume,$(image_name)-snyk)
	$(call mount_volume,$(image_name)-snyk,/src)
	@python setup.py snyksync
	docker cp . $(image_name)-snyk:/src
	docker run --rm -ti \
		--volumes-from $(image_name)-snyk \
		-e ARTIFACTORY_USERNAME \
		-e ARTIFACTORY_PASSWORD \
		-e SNYK_LEVEL \
		-e SNYK_TOKEN \
		-e WORKING_PATH=/src \
		upsidetravel-docker.jfrog.io/snyk-python-go-upside:latest
	$(call delete_volume,$(image_name)-snyk)
