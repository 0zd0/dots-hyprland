import os

from loader import log
from sh.runners.with_retry import run_with_retry


def install_yay() -> None:
    temp_dir = "/tmp/build_yay"
    base_dir = os.getcwd()

    run_with_retry(["sudo", "pacman", "-S", "--needed", "--noconfirm", "base-devel"])

    log.info("Cloning Yay repository...")
    run_with_retry(["git", "clone", "https://aur.archlinux.org/yay-bin.git", temp_dir])

    os.chdir(temp_dir)
    log.info("Building Yay package...")
    run_with_retry(["makepkg", "-o"])
    run_with_retry(["makepkg", "-se"])
    run_with_retry(["makepkg", "-i", "--noconfirm"])

    log.info("Cleaning up...")
    os.chdir(base_dir)
    run_with_retry(["rm", "-rf", temp_dir])
