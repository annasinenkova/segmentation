"""Doit tasks."""


def task_flake8():
    """Run flake8."""
    return {
        'actions': ['flake8'],
        'verbosity': 2
    }


def task_pydocstyle():
    """Run pydocstyle."""
    return {
        'actions': ['pydocstyle'],
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
        'actions': ['make -C docs html']
    }
    
    
def task_wheel():
    """Build wheel."""
    return {
        'actions': ['python3 -m build -w']
    }
