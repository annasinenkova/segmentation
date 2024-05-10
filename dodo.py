"""Doit tasks."""
import glob


def task_pot():
    """Create .pot."""
    return {
        'actions': ['pybabel extract -o messages.pot src'],
        'file_dep': glob.glob('src/*.py'),
        'targets': ['messages.pot']
    }


def task_po():
    """Create .po."""
    return {
        'actions': ['pybabel init -i messages.pot -d translations -l ru'],
        'file_dep': ['messages.pot'],
        'targets': ['translations/ru/LC_MESSAGES/messages.po'],
    }


def task_mo():
    """Compile translations."""
    return {
        'actions': ['pybabel compile -f -d translations'],
        'file_dep': ['translations/ru/LC_MESSAGES/messages.po'],
        'targets': [f'translations/ru/LC_MESSAGES/messages.mo'],
    }


def task_flake8():
    """Run flake8."""
    return {
        'actions': ['flake8 src'],
        'verbosity': 2
    }


def task_pydocstyle():
    """Run pydocstyle."""
    return {
        'actions': ['pydocstyle src'],
        'verbosity': 2
    }


def task_tests():
    """Run tests."""
    return {
        'actions': ['pytest'],
        'verbosity': 2
    }


def task_html():
    """Build html."""
    return {
        'actions': ['make -C docs html'],
        'verbosity': 2
    }


def task_wheel():
    """Build wheel."""
    return {
        'actions': ['python3 -m build -w'],
        'task_dep': ['mo'],
        'verbosity': 2
    }
