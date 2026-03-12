from django.utils import timezone
from datetime import timedelta

def expense_date_filter(queryset, filter_type):
    today = timezone.now().date()

    if filter_type == "today":
        return queryset.filter(created_at__date=today)

    if filter_type == "this_week":
        start_week = today - timedelta(days=today.weekday())
        return queryset.filter(created_at__date__gte=start_week)

    if filter_type == "last_week":
        start_last = today - timedelta(days=today.weekday() + 7)
        end_last = start_last + timedelta(days=6)
        return queryset.filter(created_at__date__range=(start_last, end_last))

    if filter_type == "this_month":
        return queryset.filter(
            created_at__year=today.year,
            created_at__month=today.month
        )

    if filter_type == "this_year":
        return queryset.filter(created_at__year=today.year)

    return queryset