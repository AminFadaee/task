import os

import click
from fpdf import FPDF

from cli_client.factory import ClientManagerFactory
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
    new_entry = click.prompt('Enter the new name for {entry}'.format(entry=entry), default=entry)
    try:
        ClientManagerFactory.create(group).edit_entry(entry, new_entry)
        click.echo(config.EDIT_SUCCESS.format(entry=entry, group=group, new_entry=new_entry))
    except LookupError:
        click.secho(config.FAILED_LOOKUP.format(entry=entry, group=group), fg='red')
    except ConflictError:
        click.secho(config.EDIT_FAILED_CONFLICT.format(entry=entry, group=group), fg='red')


@task.command(help=config.FINISH_HELP)
@click.argument('group', nargs=1)
@click.argument('entry', nargs=-1, required=True)
def finish(group, entry):
    entry = ' '.join(word for word in entry)
    ClientManagerFactory.create(group).finish_entry(entry)
    print(f'Congrats! Entry {entry} is finished!')


@task.command(help=config.GROUP_HELP)
@click.argument('name')
def group(name: str):
    ClientManagerFactory.create(name).retrieve()
    print(f'group {name} is added!')


@task.command(name='list', help=config.LIST_HELP)
@click.argument('group')
def list_entries(group):
    click.clear()
    tasks = ClientManagerFactory.create(group).retrieve()
    click.echo(TextPresenter(tasks, max_width=60).present())


@task.command(help=config.EXPORT_HELP)
@click.argument('group', nargs=1)
@click.option('--txt', 'format', flag_value='txt', default=True, help=config.EXPORT_TXT_HELP)
@click.option('--pdf', 'format', flag_value='pdf', help=config.EXPORT_PDF_HELP)
@click.option('--width', 'width', default=60, help=config.EXPORT_WIDTH)
@click.argument('path', type=click.Path())
def export(group, format, width, path):
    assert os.path.isdir(path)
    tasks = ClientManagerFactory.create(group).retrieve()
    presentation = TextPresenter(tasks, max_width=width).present()
    if format == 'txt':
        path = os.path.join(path, group + '.txt')
        with open(path, 'w') as file:
            file.write(presentation)
    elif format == 'pdf':
        path = os.path.join(path, group + '.pdf')
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font('Onuava', '', './assets/fonts/onuava__.ttf', uni=True)
        pdf.set_font('Onuava', size=12)
        pdf.multi_cell(0, 10, presentation)
        pdf.output(path, 'F')
