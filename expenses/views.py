import base64
import io
import urllib

from django.shortcuts import redirect, render
from .models import *
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
import datetime
import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


def dashboard(request):
    return render(request, 'dashboard.html')


@login_required(login_url='/auth/login/')
def expenses(request):
    data = Expenses.objects.filter(owner=request.user)
    paginator = Paginator(data, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'data': data, 'page_obj': page_obj}
    return render(request, 'expenses.html', context=context)


@login_required(login_url='/auth/login/')
def expensesadd(request):
    if request.method == 'POST':
        user = request.user
        amount = request.POST['amount']
        category = request.POST['category']
        date = request.POST['date']
        description = request.POST['description']
        user = User.objects.get(username=user)

        ent = Expenses.objects.create(owner=user, amount=amount, category=category, date=date, description=description)
        ent.save()
        messages.success(request, "New Record Added Successfully")
        return redirect('expenses:expenses')
    category = Category.objects.all()
    context = {
        'category': category
    }

    return render(request, 'expensesadd.html', context)


@login_required(login_url='/auth/login/')
def expensesedit(request, id):
    if request.method == 'GET':
        ele = Expenses.objects.get(id=id)
        context = {
            'edit': True,
            'ele': ele,
            'category': Category.objects.all()
        }
        return render(request, 'expensesadd.html', context)

    if request.method == 'POST':
        ele = Expenses.objects.get(id=id)
        ele.amount = request.POST['amount']
        ele.category = request.POST['category']
        ele.date = request.POST['date']
        ele.description = request.POST['description']
        ele.save()
        messages.success(request, "Editted Successfully")
        return redirect('expenses:expenses')


@login_required(login_url='/auth/login/')
def expensesdelete(request, id):
    ele = Expenses.objects.get(id=id)
    ele.delete()
    messages.success(request, "Deleted Successfully")
    return redirect('expenses:expenses')


def stat(request):
    return render(request, 'stats.html')


def getcat(exp):
    return exp.category


def stat_api(request):
    now = datetime.datetime.today()
    year = now - datetime.timedelta(days=30 * 12)
    exp = Expenses.objects.filter(owner=request.user, date__gte=year, date__lte=now)
    final = {}
    all_cat = []
    f = Category.objects.all()
    for i in f:
        all_cat.append(i.name)

    def get_amt(cat):
        ans = 0
        expd = exp.filter(category=cat)
        for i in expd:
            ans += int(i.amount)
        return ans

    for y in all_cat:
        final[y] = get_amt(y)

    return JsonResponse({'exp_result': final}, safe=False)


@login_required(login_url='/auth/login/')
def exportdata(request):
    data = Expenses.objects.filter(owner=request.user)
    res = HttpResponse(content_type='text/csv')
    res['Content-Disposition'] = 'attachment; filename=Expense_Data' + str(datetime.datetime.now()) + '.csv'
    writer = csv.writer(res)
    writer.writerow(['Amount', 'Category', 'Date', 'Description'])
    for i in data:
        writer.writerow([i.amount, i.category, i.date, i.description])
    return res

@login_required(login_url='/auth/login/')
def data_pred(request):
    data = Expenses.objects.filter(owner=request.user)
    response = HttpResponse(content_type="image/png")
    response['Content-Disposition'] = 'attachment; filename=pred' + str(datetime.datetime.now()) + '.png'
    asd = []
    for i in data:
        asd.append([int(i.amount), i.category, i.date.strftime("%d/%m/%Y"), i.description])

    numpy_array = np.asarray(asd)
    x = [i[2] for i in asd]
    y = [int(i[0]) for i in asd]
    y = np.asarray(y)
    x = pd.to_datetime(x, format="%d/%m/%Y")
    X = x.map(dt.datetime.toordinal)
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=.7, random_state=42)
    model = LinearRegression()
    model.fit(X_train.values.reshape(-1, 1), y_train)
    model.score(X_train.values.reshape(-1, 1), y_train)
    y_pred = model.predict(X_test.values.reshape(-1, 1))

    plt.scatter(X_train.values.reshape(-1, 1), y_train, color='red')
    plt.plot(X_train, model.predict(X_train.values.reshape(-1, 1)), color='blue')
    plt.title('Amount')
    plt.xlabel('Date')
    plt.ylabel('Amount')

    plt.scatter(X_test.values.reshape(-1, 1), y_test, color='red')
    plt.plot(X_train.values.reshape(-1, 1), model.predict(X_train.values.reshape(-1, 1)), color='blue')
    plt.title('Amount')
    plt.xlabel('Date')
    plt.ylabel('Amount')

    plt.savefig(response, format="png")
    return response