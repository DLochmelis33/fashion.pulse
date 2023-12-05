import os


def read_env_var(name: str) -> str:
    env_var = os.environ.get(name)
    if env_var is None:
        print(f'Failed to find environment variable `{name}`')
        exit(-1)
    return env_var
