

FROM ubuntu:22.04

ENV PYENV_ROOT="/opt/.pyenv" \
    PATH="/opt/pipx/bin:/opt/.pyenv/shims:/opt/.pyenv/bin:$PATH" \
    PIPX_HOME="/opt/pipx" \
    PIPX_BIN_DIR="/opt/pipx/bin"

RUN mkdir $PIPX_HOME \
    && apt-get update \
    && apt-get install -y ccache build-essential git curl libssl-dev libz-dev libbz2-dev libncurses-dev libffi-dev libsqlite3-dev liblzma-dev libreadline-dev \
    && curl https://pyenv.run | bash \
    && git clone https://github.com/pyenv/pyenv-ccache.git $(pyenv root)/plugins/pyenv-ccache \
    # NOTE: 3.3 installation fails with a segmentation fault :(
    # NOTE: 3.4 installation fails: cannot find libssl (while it is installed)
    && pyenv install 2.7 3.5 3.6 3.7 3.8 3.9 3.10 3.11 3.12 \
    # enable all versions, 3.12 is default
    && pyenv global 3.12 2.7 3.5 3.6 3.7 3.8 3.9 3.10 3.11 \
    && pip install pipx \
    && pipx install tox>=4 \
    && pipx install poetry \
    && pipx install pre-commit \
    && ccache -C \
    && rm -rf /var/lib/apt/lists/*
