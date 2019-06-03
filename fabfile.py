from fabpolish import polish, sniff, local, info
from fabpolish.contrib import (
    find_merge_conflict_leftovers,
    find_pep8_violations
)

import os

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))


@sniff(severity='major', timing='fast')
def remove_compiled_classes():
    # Remove compiled python classes
    info('Removing compiled python classes...')
    return local("find ./ -name '*.py[co]' -print0 | xargs -0 rm -f")


@sniff(severity='major', timing='fast')
def code_analyzer():
    """Running static code analyzer"""
    info('Running static code analyzer...')
    return local(
        "git ls-files -z | "
        "grep -vz '^\.' | "
        "grep -Pvz '\.(md|yml|log|txt|lock)$' |"
        "grep -Pzv '(fabfile.py|Makefile)' |"
        "grep -Pzv '(sample|cron)' |"
        "xargs -0 pyflakes"
    )

@sniff(severity='major', timing='fast')
def remove_debug_info():
    """Check and remove debugging print statements"""
    # Have to remove scripts and test file
    info('Checking for debug print statements...')
    return local(
        "! git ls-files -z | "
        "grep -PZvz '^scripts/' | "
        "grep -PZvz 'tests/run_tests.py' | "
        "grep -PZvz 'fabfile.py' | "
        "grep -PZz \.py$ | "
        "xargs -0 grep -Pn \'(?<![Bb]lue|>>> )print\' | "
        "grep -v NOCHECK"
    )


if __name__ == "__main__":
    polish()