FROM gitpod/workspace-full

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH="$HOME/.poetry/bin:$PATH"