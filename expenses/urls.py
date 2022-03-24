from django.urls import path
from . import views
app_name = 'expenses'

urlpatterns = [
    path('', views.expenses, name='expenses'),
    path('expenses/add/', views.expensesadd, name='add'),
    path('expenses/edit/<int:id>', views.expensesedit, name='edit'),
    path('expenses/delete/<int:id>', views.expensesdelete, name='delete'),
    path('stat/', views.stat, name='stat'),
    path('expenses/statapi/', views.stat_api, name='statapi'),
    path('data/', views.exportdata, name='export'),
]