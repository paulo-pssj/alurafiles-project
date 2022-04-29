import os

from django.contrib import messages
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect, render

from alurafiles.models import Dates, Transactions

from .utils import (agencias_suspeitas, contas_suspeitas, csv_to_database,
                    transacoes_suspeitas, verifica_arquivo_vazio,
                    xml_to_database)


def index(request):
    if request.user.is_authenticated:
        if request.method == 'POST' and request.FILES['file']:
            upload = request.FILES['file']
            fss = FileSystemStorage()

            if not os.path.isfile(f'./media/{upload.name}'):
                fss.save(upload.name, upload)
                file = verifica_arquivo_vazio(f'./media/{upload.name}')
                if file == None:
                    messages.error(request, 'Arquivo vazio.')
                    return redirect('index')
            else:
                messages.error(
                    request,
                    'Arquivo está na base de dados, tente outro arquivo.',
                )
                return redirect('index')

            if file.endswith('.csv'):
                csv = csv_to_database(request, file)
                if csv is None:
                    messages.success(request, 'Arquivo enviado com sucesso.')
                    return redirect('index')
                else:
                    messages.error(
                        request,
                        f'Transações do dia {csv} já estão no banco de dados.',
                    )
                    os.remove(file)

            if file.endswith('.xml'):
                xml = xml_to_database(request, file)
                if xml is None:
                    messages.success(request, 'Arquivo enviado com sucesso.')
                    return redirect('index')
                else:
                    messages.error(
                        request,
                        f'Transações do dia {xml} já estão no banco de dados.',
                    )
                    os.remove(file)

        data = Dates.objects.all().order_by('-transaction_date')
        context = {'data': data}
        return render(request, 'alurafiles/index.html', context=context)
    else:
        return render(request, 'usuarios/login.html')


def detalhes(request, date):
    if request.user.is_authenticated:
        data = Transactions.objects.filter(transaction_date=date).all()
        print(len(data))
        user = User.objects.filter(id=data[0].user_id_id).get()
        date_import = Dates.objects.filter(transaction_date=date).get()
        if data:
            context = {'data': data, 'user': user, 'date_import': date_import}
            return render(request, 'alurafiles/detalhes.html', context)
        else:
            return redirect(index)
    else:
        return redirect(index)


def analise(request):
    if request.user.is_authenticated:
        return render(request, 'alurafiles/suspeitos.html')


def analise_suspeitos(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            date = request.POST['data_analise']
            ano, mes = date.split('-')

            if (
                transacoes_suspeitas(mes, ano).exists() == False
                and contas_suspeitas(mes, ano) == None
                and agencias_suspeitas(mes, ano) == None
            ):
                messages.error(request, 'Nenhum dado encontrado.')
                return redirect('analise')

            context = {
                'transacoes_suspeitas': transacoes_suspeitas(mes, ano),
                'contas_suspeitas': contas_suspeitas(mes, ano),
                'agencias_suspeitas': agencias_suspeitas(mes, ano),
            }
            return render(request, 'alurafiles/suspeitos.html', context)

        return redirect(analise)
