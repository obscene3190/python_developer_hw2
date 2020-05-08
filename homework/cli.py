import click
import sqlite3
from patient import Patient, PatientCollection


@click.group()
def cli():
    pass


@click.command()
@click.argument('first_name')
@click.argument('last_name')
@click.option('--birth-date', 'birth_date', required=True)
@click.option('--phone', 'phone', required=True)
@click.option('--document-type', 'doc_type', required=True)
@click.option('--document-id', 'doc_id', required=True)
def create(first_name, last_name, birth_date, phone, doc_type, doc_id):
    patient = Patient(first_name, last_name, birth_date, phone, doc_type, doc_id)
    patient.save()


@click.command()
@click.argument('value', default=10)
def show(value):
    collection1 = PatientCollection()
    for patient in collection1.limit(value):
        print(patient)


@click.command()
def count():
    table = sqlite3.connect('PatientsCollection.db')
    with table:
        cursor = table.cursor()
        cursor.execute("SELECT COUNT(*) FROM PatientsCollection")
        print(cursor.fetchone()[0])


cli.add_command(create)
cli.add_command(show)
cli.add_command(count)

if __name__ == '__main__':
    cli()
