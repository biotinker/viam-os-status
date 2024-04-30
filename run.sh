#!/bin/sh
cd "$(dirname "$0")"
LOG_PREFIX="[Viam OS Status module setup]"

echo "$LOG_PREFIX Starting the module."

os=$(uname -s)
arch=$(uname -m)


# Else, try running with a virtual environment and source
VENV_NAME="viam-os-status"
PYTHON="$VENV_NAME/bin/python"

echo "$LOG_PREFIX Running the module using virtual environment. This requires Python >=3.8.1, pip3, and venv to be installed."

if ! python3 -m venv "$VENV_NAME" >/dev/null 2>&1; then
    echo "$LOG_PREFIX Error: failed to create venv. Please use your system package manager to install python3-venv." >&2
    exit 1
else
    echo "$LOG_PREFIX Created/found venv."
fi

# -qq suppresses extraneous output from pip
echo "$LOG_PREFIX Installing/upgrading Python packages."
if [ $(arch) = "arm7l" ] ; then
    mkdir wheels
    python3 -m pip download \
        --extra-index-url https://www.piwheels.org/simple \
        --implementation cp \
        --platform linux_armv6l \
        --abi cp37m \
        --only-binary=:all: \
        -d wheels \
        viam-sdk
else
    if ! "$PYTHON" -m pip install -r requirements.txt -qq; then
        echo "$LOG_PREFIX Error: pip failed to install requirements.txt. Please use your system package manager to install python3-pip." >&2
        exit 1
    fi
fi 


# Be sure to use `exec` so that termination signals reach the python process,
# or handle forwarding termination signals manually
echo "$LOG_PREFIX Starting module."
exec "$PYTHON" -m src.main "$@"
