# ------------------------------------------------------------------ Settings -
TAG="${USER}/python"
ARGS="${@}"

build:
	@docker build -t "${TAG}" .

run:
	@docker run -it --rm "${TAG}" python

python:
	@docker run -it --rm "${TAG}" python "${ARGS}"

clean:
	@docker image rm "${TAG}"