import click
from proximl.cli import cli, pass_config, search_by_id_name
from proximl.cli.cloudbender import cloudbender


@cloudbender.group()
@pass_config
def datastore(config):
    """proxiML CloudBender datastore commands."""
    pass


@datastore.command()
@click.option(
    "--provider",
    "-p",
    type=click.STRING,
    required=True,
    help="The provider ID of the region.",
)
@click.option(
    "--region",
    "-r",
    type=click.STRING,
    required=True,
    help="The region ID to list datastores for.",
)
@pass_config
def list(config, provider, region):
    """List datastores."""
    data = [
        ["ID", "NAME", "TYPE"],
        [
            "-" * 80,
            "-" * 80,
            "-" * 80,
        ],
    ]

    datastores = config.proximl.run(
        config.proximl.client.cloudbender.datastores.list(
            provider_uuid=provider, region_uuid=region
        )
    )

    for datastore in datastores:
        data.append(
            [
                datastore.id,
                datastore.name,
                datastore.type,
            ]
        )

    for row in data:
        click.echo(
            "{: >37.36} {: >29.28} {: >9.8} " "".format(*row),
            file=config.stdout,
        )


@datastore.command()
@click.option(
    "--provider",
    "-p",
    type=click.STRING,
    required=True,
    help="The provider ID of the region.",
)
@click.option(
    "--region",
    "-r",
    type=click.STRING,
    required=True,
    help="The region ID to create the datastore in.",
)
@click.option(
    "--type",
    "-t",
    type=click.Choice(
        [
            "nfs",
            "smb",
        ],
        case_sensitive=False,
    ),
    required=True,
    help="The type of datastore to create.",
)
@click.option(
    "--uri",
    "-u",
    type=click.STRING,
    required=True,
    help="The URI of the datastore",
)
@click.option(
    "--root",
    "-r",
    type=click.STRING,
    required=True,
    help="The root path to map within the datastore",
)
@click.argument("name", type=click.STRING, required=True)
@pass_config
def create(config, provider, region, type, uri, root, name):
    """
    Creates a datastore.
    """
    return config.proximl.run(
        config.proximl.client.cloudbender.datastores.create(
            provider_uuid=provider,
            region_uuid=region,
            name=name,
            uri=uri,
            root=root,
            type=type,
        )
    )


@datastore.command()
@click.option(
    "--provider",
    "-p",
    type=click.STRING,
    required=True,
    help="The provider ID of the region.",
)
@click.option(
    "--region",
    "-r",
    type=click.STRING,
    required=True,
    help="The region ID to remove the datastore from.",
)
@click.argument("datastore", type=click.STRING)
@pass_config
def remove(config, provider, region, datastore):
    """
    Remove a datastore.

    DATASTORE may be specified by name or ID, but ID is preferred.
    """
    datastores = config.proximl.run(
        config.proximl.client.cloudbender.datastores.list(
            provider_uuid=provider, region_uuid=region
        )
    )

    found = search_by_id_name(datastore, datastores)
    if None is found:
        raise click.UsageError("Cannot find specified datastore.")

    return config.proximl.run(found.remove())
