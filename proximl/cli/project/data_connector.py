import click
import os
import json
import base64
from pathlib import Path
from proximl.cli import pass_config
from proximl.cli.project import project


@project.group()
@pass_config
def data_connector(config):
    """proxiML project data_connector commands."""
    pass


@data_connector.command()
@pass_config
def list(config):
    """List project data_connectors."""
    data = [
        ["ID", "NAME", "TYPE", "REGION_UUID"],
        [
            "-" * 80,
            "-" * 80,
            "-" * 80,
            "-" * 80,
        ],
    ]
    project = config.proximl.run(
        config.proximl.client.projects.get(config.proximl.client.project)
    )

    data_connectors = config.proximl.run(project.data_connectors.list())

    for data_connector in data_connectors:
        data.append(
            [
                data_connector.id,
                data_connector.name,
                data_connector.type,
                data_connector.region_uuid,
            ]
        )

    for row in data:
        click.echo(
            "{: >38.36} {: >30.28} {: >15.13} {: >38.36}" "".format(*row),
            file=config.stdout,
        )


@data_connector.command()
@pass_config
def refresh(config):
    """
    Refresh project data_connector list.
    """
    project = config.proximl.run(config.proximl.client.projects.get_current())

    return config.proximl.run(project.data_connectors.refresh())
