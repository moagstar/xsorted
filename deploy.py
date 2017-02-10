import sys
import subprocess
import click


version_spec = ['major', 'minor', 'release']


@click.command()
@click.argument('deployment_type', type=click.Choice(version_spec), default='minor')
def deploy(deployment_type):
    prev_tag = subprocess.check_output(['git', 'describe', '--abbrev=0', '--tags'])
    prev_tag = prev_tag.decode('ascii').strip()
    version = dict(zip(version_spec, map(int, prev_tag.split('.'))))
    version[deployment_type] += 1
    version = '.'.join(str(version[x]) for x in version_spec)
    subprocess.check_call(['git', 'tag', 'version'])
    subprocess.check_call(['git', 'push', 'origin', 'master', '--tags'])
    subprocess.check_call(['python', 'setup.py', 'sdist'])
    subprocess.check_call(['twine', './dist/xsorted-' + version + '.tar.gz'])


if __name__ == '__main__':
    deploy()
