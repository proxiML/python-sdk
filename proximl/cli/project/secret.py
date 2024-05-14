import click
from proximl.cli import pass_config
from proximl.cli.project import project


@project.group()
@pass_config
def secret(config):
    """proxiML project secret commands."""
    pass


@secret.command()
@pass_config
def list(config):
    """List secrets."""
    data = [
        ["NAME", "CREATED BY", "UPDATED AT"],
        [
            "-" * 80,
            "-" * 80,
            "-" * 80,
        ],
    ]
    project = config.proximl.run(config.proximl.client.projects.get_current())
    secrets = config.proximl.run(project.secrets.list())

    for secret in secrets:
        data.append(
            [
                secret.name,
                secret.created_by,
                secret.updated_at.isoformat(timespec="seconds"),
            ]
        )

    for row in data:
        click.echo(
            "{: >38.36} {: >30.28} {: >28.26}" "".format(*row),
            file=config.stdout,
        )


@secret.command()
@click.argument("name", type=click.STRING)
@pass_config
def put(config, name):
    """
    Set a secret value.

    Secret is created with the specified NAME.
    """
    project = config.proximl.run(config.proximl.client.projects.get_current())

    value = click.prompt("Enter the secret value", type=str, hide_input=True)

    return config.proximl.run(project.secrets.put(name=name, value=value))


@secret.command()
@click.argument("name", type=click.STRING)
@pass_config
def remove(config, name):
    """
    Remove a secret.


    """
    project = config.proximl.run(config.proximl.client.projects.get_current())

    return config.proximl.run(project.secret.remove(name))
