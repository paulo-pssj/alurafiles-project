import csv
import os
import xml.etree.ElementTree as ET
from datetime import datetime

from django.db.models import Sum

from .models import Dates, Transactions


def verifica_arquivo_vazio(file):
    """Verifica se arquivo csv está vazio."""
    if os.path.getsize(file) == 0:
        os.remove(file)
        return None
    return file


def csv_to_database(request, file):
    """Importa as transações do arquivo csv para o banco de dados"""
    with open(file) as csvfile:
        content = list(csv.reader(csvfile))
        first_date = content[0][-1]
        first_date = first_date.split('T')[0]

        date_exists = Transactions.objects.filter(
            transaction_date=first_date
        ).exists()
        if date_exists:
            return first_date

        for row in content:
            date_row = row[-1].split('T')[0]
            if len(row) == 8 and date_row == first_date:
                transaction = Transactions(
                    origin_bank=row[0],
                    origin_agency=row[1],
                    origin_account=row[2],
                    destiny_bank=row[3],
                    destiny_agency=row[4],
                    destiny_account=row[5],
                    value_transaction=float(row[6]),
                    transaction_date=date_row,
                    user_id=request.user,
                )
                transaction.save()

        table_dates = Dates(transaction_date=first_date, user_id=request.user)
        table_dates.save()


def xml_to_database(request, file):
    tree = ET.parse(file)
    root = tree.getroot()

    first_date = root.find('transacao').find('data').text
    first_date = first_date.split('T')[0]
    date_exists = Transactions.objects.filter(
        transaction_date=first_date
    ).exists()

    if date_exists:
        return first_date

    for t in root:
        date_transacao = t.find('data').text
        date_transacao = date_transacao.split('T')[0]
        if date_transacao == first_date:
            transaction = Transactions(
                origin_bank=t.find('origem').find('banco').text,
                origin_agency=t.find('origem').find('agencia').text,
                origin_account=t.find('origem').find('conta').text,
                destiny_bank=t.find('destino').find('banco').text,
                destiny_agency=t.find('destino').find('banco').text,
                destiny_account=t.find('destino').find('banco').text,
                value_transaction=float(t.find('valor').text),
                transaction_date=date_transacao,
                user_id=request.user,
            )
            transaction.save()
    table_dates = Dates(transaction_date=first_date, user_id=request.user)
    table_dates.save()


def transacoes_suspeitas(mes, ano):
    return Transactions.objects.filter(
        transaction_date__year=ano,
        transaction_date__month=mes,
        value_transaction__gte=100000,
    ).all()


def contas_suspeitas(mes, ano):
    contas_suspeitas = []
    for contas in Transactions.objects.filter(
        transaction_date__year=ano,
        transaction_date__month=mes,
    ).distinct('origin_account'):

        result = (
            Transactions.objects.filter(
                transaction_date__year=ano,
                transaction_date__month=mes,
            )
            .filter(origin_account=contas.origin_account)
            .aggregate(Sum('value_transaction'))
        )
        contas_suspeitas_origem = (
            contas.origin_account,
            contas.origin_bank,
            contas.origin_agency,
            'Saída',
            result['value_transaction__sum'],
        )

        if result['value_transaction__sum'] >= 1000000:
            contas_suspeitas.append(contas_suspeitas_origem)

    for contas in Transactions.objects.filter(
        transaction_date__year=ano,
        transaction_date__month=mes,
    ).distinct('destiny_account'):

        result = (
            Transactions.objects.filter(
                transaction_date__year=ano,
                transaction_date__month=mes,
            )
            .filter(destiny_account=contas.destiny_account)
            .aggregate(Sum('value_transaction'))
        )
        contas_suspeitas_destino = (
            contas.destiny_account,
            contas.destiny_bank,
            contas.destiny_agency,
            'Entrada',
            result['value_transaction__sum'],
        )
        if result['value_transaction__sum'] >= 1000000:
            contas_suspeitas.append(contas_suspeitas_destino)

    if contas_suspeitas != []:
        return contas_suspeitas
    else:
        contas_suspeitas = None
        return contas_suspeitas


def agencias_suspeitas(mes, ano):
    agencias_suspeitas = []
    for agencia in Transactions.objects.filter(
        transaction_date__year=ano,
        transaction_date__month=mes,
    ).distinct('origin_agency'):

        result = (
            Transactions.objects.filter(
                transaction_date__year=ano,
                transaction_date__month=mes,
            )
            .filter(origin_agency=agencia.origin_agency)
            .aggregate(Sum('value_transaction'))
        )
        agencias_suspeitas_origem = (
            agencia.origin_bank,
            agencia.origin_agency,
            'Saída',
            result['value_transaction__sum'],
        )

        if result['value_transaction__sum'] >= 1000000:
            agencias_suspeitas.append(agencias_suspeitas_origem)

    for agencia in Transactions.objects.filter(
        transaction_date__year=ano,
        transaction_date__month=mes,
    ).distinct('destiny_agency'):

        result = (
            Transactions.objects.filter(
                transaction_date__year=ano,
                transaction_date__month=mes,
            )
            .filter(destiny_agency=agencia.destiny_agency)
            .aggregate(Sum('value_transaction'))
        )
        agencias_suspeitas_destino = (
            agencia.destiny_bank,
            agencia.destiny_agency,
            'Entrada',
            result['value_transaction__sum'],
        )

        if result['value_transaction__sum'] >= 1000000:
            agencias_suspeitas.append(agencias_suspeitas_destino)

    if agencias_suspeitas != []:
        return agencias_suspeitas
    else:
        agencias_suspeitas = None
        return agencias_suspeitas
