import click

from cli_client.factory import ClientManagerFactory
from exporter.pdf_exporter import PDFExporter
from exporter.text_exporter import TXTExporter
from presenter.presenter import TextPresenter
from tasks.errors import UniqueViolationError, ConflictError
from . import config


@click.group(help=config.TASK_HELP)
def task():
    pass


@task.command(help=config.ADD_HELP)
@click.argument('group', nargs=1)
@click.argument('entry', nargs=-1, required=True)
def add(group, entry):
    entry = ' '.join(word for word in entry)
    try:
        ClientManagerFactory.create(group).add_entry(entry)
        click.echo(config.ADD_SUCCESS.format(group=group, entry=entry))
    except UniqueViolationError:
        click.secho(config.ADD_FAILED.format(group=group, entry=entry), fg='red')


@task.command(help=config.EDIT_HELP)
@click.argument('group', nargs=1)
@click.argument('entry', nargs=-1, required=True)
def edit(group, entry):
    entry = ' '.join(word for word in entry)
    manager = ClientManagerFactory.create(group)
    try:
        full_name = manager.get_entry_full_name(partial_name=entry)
        new_entry = click.prompt(config.EDIT_NEW_NAME_PROMPT.format(entry=full_name), default=full_name)
        task_name = manager.edit_entry(full_name, new_entry)
        click.echo(config.EDIT_SUCCESS.format(entry=full_name, group=group, new_entry=task_name))
    except LookupError:
        click.secho(config.FAILED_LOOKUP.format(entry=entry, group=group), fg='red')
    except ConflictError:
        click.secho(config.EDIT_FAILED_CONFLICT.format(entry=entry, group=group), fg='red')


@task.command(name='list', help=config.LIST_HELP)
@click.argument('group')
@click.option('--unfinished-tasks', '-u', is_flag=True, help=config.LIST_UNFINISHED)
def list_entries(group, unfinished_tasks):
    click.clear()
    tasks = ClientManagerFactory.create(group).retrieve()
    presentation = TextPresenter(tasks, max_width=60).present(only_unfinished_tasks=unfinished_tasks)
    click.echo(presentation)


@task.command(help=config.FINISH_HELP)
@click.argument('group', nargs=1)
@click.argument('entry', nargs=-1, required=True)
def finish(group, entry):
    entry = ' '.join(word for word in entry)
    manager = ClientManagerFactory.create(group)
    full_name = manager.get_entry_full_name(entry)
    manager.finish_entry(full_name)
    click.secho(config.FINISH_SUCCESS.format(entry=full_name))


@task.command(help=config.UNDO_HELP)
@click.argument('group', nargs=1)
@click.argument('entry', nargs=-1, required=True)
def undo(group, entry):
    entry = ' '.join(word for word in entry)
    manager = ClientManagerFactory.create(group)
    full_name = manager.get_entry_full_name(entry)
    manager.undo_entry(full_name)
    click.secho(config.UNDO_SUCCESS.format(entry=full_name))


@task.command(help=config.EXPORT_HELP)
@click.argument('group', nargs=1)
@click.option('--txt', 'format', flag_value='txt', default=True, help=config.EXPORT_TXT_HELP)
@click.option('--pdf', 'format', flag_value='pdf', help=config.EXPORT_PDF_HELP)
@click.option('--width', 'width', default=60, help=config.EXPORT_WIDTH)
@click.argument('path', type=click.Path())
def export(group, format, width, path):
    tasks = ClientManagerFactory.create(group).retrieve()
    presentation = TextPresenter(tasks, max_width=width).present()
    if format == 'pdf':
        exporter = PDFExporter(path, file_name=group)
    else:
        exporter = TXTExporter(path, file_name=group)
    exporter.export(presentation)
    click.echo(config.EXPORT_SUCCESS.format(group=group, path=exporter.path))
