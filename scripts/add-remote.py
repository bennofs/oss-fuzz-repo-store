#!/usr/bin/env python3
import sys
import subprocess
import os

from hashlib import sha256


def main(dataset_name, repo_name, repo_url):
    h = sha256(repo_url.encode()).hexdigest()[:6]
    slug = f'{repo_name}-{h}'
    remote_name = f'{dataset_name}-{repo_name}-{h}'

    os.environ['GIT_TERMINAL_PROMPT'] = '0'
    result = subprocess.run(['git', 'remote', 'rm', remote_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0 and 'No such remote' not in result.stderr.decode():
        print("[!] git remote rm failed", file=sys.stderr)
        print("- stdout -", file=sys.stderr)
        sys.stderr.write(result.stdout)
        print("- stderr -", file=sys.stderr)
        sys.stderr.buffer.write(result.stderr)
        sys.exit(1)

    # from: https://moi.vonos.net/programming/git-multiple-remotes/
    subprocess.run(['git', 'remote', 'add', remote_name, repo_url], check=True)
    subprocess.run(['git', 'config', '--unset-all', f'remote.{remote_name}.fetch'], check=True)
    subprocess.run(['git', 'config', '--add', f'remote.{remote_name}.tagOpt', '--no-tags'], check=True)
    subprocess.run(['git', 'config', '--add', f'remote.{remote_name}.fetch', f'+refs/*:refs/repo/{remote_name}/*'], check=True)


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("usage: add-remote.py dataset_name repo_name repo_url", file=sys.stderr)
        sys.exit(1)

    os.chdir(os.getenv("OSS_SRC_GIT_STORE_DIR"))
    main(*sys.argv[1:])
