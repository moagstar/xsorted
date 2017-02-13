import sys
import subprocess
import click


version_spec = ['major', 'minor', 'release']


@click.command()
@click.argument('deployment_type', type=click.Choice(version_spec), default='minor')
def deploy(deployment_type):

    version = subprocess.check_output(['git', 'describe', '--abbrev=0', '--tags'])
    version = version.decode('ascii').strip()
    version = dict(zip(version_spec, map(int, version.split('.'))))
    version[deployment_type] += 1
    if deployment_type == 'major':
        version[1] = version[2] = 0
    elif deployment_type == 'minor':
        version[2] = 0
    version = '.'.join(str(version[x]) for x in version_spec)

    subprocess.check_call(['git', 'tag', '-a', version, '-m', version])
    subprocess.check_call(['git', 'push', 'origin', 'master', '--tags'])
    subprocess.check_call(['python', 'setup.py', 'sdist'])
    subprocess.check_call(['twine', 'upload', './dist/xsorted-' + version + '.tar.gz'])


if __name__ == '__main__':
    deploy()
