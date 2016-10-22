import subprocess


def test_flake8():
    exit_status = subprocess.call(['flake8', '--exclude=venv/*,*test*'])
    assert exit_status == 0
