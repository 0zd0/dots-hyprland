#!/bin/bash

set -e

REQUIRED_VERSION_PYTHON="3.11"
INSTALL_SCRIPT_PYTHON="installer/install.py"
PYTHON_BIN="python3"

REMOTE_REPO="0zd0/dots-hyprland"
CACHE_DIR="${HOME}/.cache/dots-setup"
INSTALLER_DIR="${CACHE_DIR}/installer"
VENV_DIR="${INSTALLER_DIR}/.venv"

check_arch_linux() {
    [[ -f /etc/os-release && "$(grep '^ID=' /etc/os-release | cut -d= -f2)" == "arch" ]] || {
        echo "Error: This script is designed for Arch Linux." >&2
        exit 1
    }
}

check_python_version() {
    local current_version
    current_version=$($PYTHON_BIN --version 2>/dev/null | awk '{print $2}')

    if [[ -z "$current_version" || "$(printf '%s\n' "$REQUIRED_VERSION_PYTHON" "$current_version" | sort -V | head -n 1)" != "$REQUIRED_VERSION_PYTHON" ]]; then
        echo "Error: Python $REQUIRED_VERSION_PYTHON+ is required" >&2
        exit 1
    fi
}

check_poetry_installed() {
    if ! command -v poetry &> /dev/null; then
        echo "Poetry is not installed. Installing Poetry..."
        curl -sSL https://install.python-poetry.org | python3 -
    fi
}

create_poetry_venv() {
    echo "Creating poetry virtual environment..."
    cd "$INSTALLER_DIR"
    poetry install
}

download_repo() {
    mkdir -p "$CACHE_DIR"
    cd "$CACHE_DIR"
    if [[ ! -d .git ]]; then
        git init -b main
        git remote add origin "https://github.com/$REMOTE_REPO"
    fi
    git pull origin main
    git submodule update --init --recursive
}

run_install_script() {
    poetry run "$PYTHON_BIN" "$INSTALL_SCRIPT_PYTHON" "$@"
}

main() {
    check_arch_linux
    check_python_version
    check_poetry_installed
    download_repo
    create_poetry_venv
    run_install_script "$@"
}

main "$@"
