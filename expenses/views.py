from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import transaction
from datetime import timedelta
from .models import Expense
from .forms import ExpenseForm
import calendar
from django.db.models import Sum
from django.http import HttpResponse
import openpyxl

# ================= LIST =================
@login_required
def expenses_list(request):
    filter_type = request.GET.get('filter', '')
    selected_month = request.GET.get('month', '')
    selected_year = request.GET.get('year', '')

    today = timezone.localdate()
    expenses_qs = Expense.objects.all()

    # ===== Filters =====
    if filter_type == 'today':
        expenses_qs = expenses_qs.filter(created_at__date=today)
    elif filter_type == 'this_week':
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        expenses_qs = expenses_qs.filter(created_at__date__gte=start_of_week,
                                         created_at__date__lte=end_of_week)
    elif filter_type == 'last_week':
        start_of_last_week = today - timedelta(days=today.weekday() + 7)
        end_of_last_week = start_of_last_week + timedelta(days=6)
        expenses_qs = expenses_qs.filter(created_at__date__gte=start_of_last_week,
                                         created_at__date__lte=end_of_last_week)
    elif filter_type == 'this_year':
        expenses_qs = expenses_qs.filter(created_at__year=today.year)

    if selected_month:
        expenses_qs = expenses_qs.filter(created_at__month=int(selected_month))
    if selected_year:
        expenses_qs = expenses_qs.filter(created_at__year=int(selected_year))

    total_expenses = expenses_qs.aggregate(total=Sum('amount'))['total'] or 0

    month_choices = [(str(i).zfill(2), calendar.month_name[i]) for i in range(1, 13)]
    years = Expense.objects.dates('created_at', 'year', order='DESC')
    year_choices = [y.year for y in years]

    context = {
        'expenses': expenses_qs,
        'total_expenses': total_expenses,
        'filter_type': filter_type,
        'selected_month': selected_month,
        'selected_year': selected_year,
        'month_choices': month_choices,
        'year_choices': year_choices,
    }

    return render(request, 'expenses/expenses_list.html', context)


# ================= ADD =================
@login_required
@transaction.atomic
def expense_add(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expenses_list')
    else:
        form = ExpenseForm()
    return render(request, 'expenses/expense_form.html', {'form': form, 'title': 'Add Expense'})


# ================= EDIT =================
@login_required
@transaction.atomic
def expense_edit(request, pk):
    expense = get_object_or_404(Expense, id=pk)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expenses_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'expenses/expense_form.html', {'form': form, 'title': f'Edit Expense #{expense.id}'})


# ================= DELETE =================
@login_required
@transaction.atomic
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, id=pk)
    if request.method == 'POST':
        expense.delete()
        return redirect('expenses_list')
    return render(request, 'expenses/expense_confirm_delete.html', {'expense': expense})


# ================= EXPORT EXCEL =================
@login_required
def export_expenses_excel(request):
    month = request.GET.get('month')
    year = request.GET.get('year')

    expenses_qs = Expense.objects.all()

    if year:
        expenses_qs = expenses_qs.filter(created_at__year=int(year))
    if month:
        expenses_qs = expenses_qs.filter(created_at__month=int(month))

    total_expenses = expenses_qs.aggregate(total=Sum('amount'))['total'] or 0

    # Create workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Expenses"

    # Header
    ws.append(["ID", "Title", "Amount (UGX)", "Note", "Date"])

    # Expense rows
    for e in expenses_qs:
        ws.append([
            e.id,
            e.title,
            float(e.amount),
            e.note or "",
            e.created_at.strftime("%d %b %Y %H:%M")
        ])

    # Summary row
    ws.append([])
    ws.append(["TOTAL EXPENSES", "", float(total_expenses), "", ""])

    # Response
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = "attachment; filename=Expenses_Report.xlsx"
    wb.save(response)
    return response