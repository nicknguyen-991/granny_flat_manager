from decimal import Decimal

from django.db.models import Count, DecimalField, Q, Sum, Value
from django.db.models.functions import Coalesce
from django.shortcuts import render

from accounts.models import Staff
from construction.models import Project, ProjectStageProgress
from crm.models import Commission, Lead


ZERO = Value(Decimal('0.00'), output_field=DecimalField(max_digits=14, decimal_places=2))


def _money(qs, **kwargs):
    return qs.aggregate(total=Coalesce(Sum('contract_value', **kwargs), ZERO))['total']


def _commission_sum(**kwargs):
    return Commission.objects.aggregate(
        total=Coalesce(Sum('commission_amount', **kwargs), ZERO)
    )['total']


def dashboard(request):
    total_leads = Lead.objects.count()
    won_leads = Lead.objects.filter(status=Lead.Status.WON).count()
    lost_leads = Lead.objects.filter(status=Lead.Status.LOST).count()
    conversion_pct = (won_leads / total_leads * 100) if total_leads else 0

    sales_rows = (
        Staff.objects.annotate(
            total_leads=Count('leads'),
            won_leads=Count('leads', filter=Q(leads__status=Lead.Status.WON)),
            lost_leads=Count('leads', filter=Q(leads__status=Lead.Status.LOST)),
        )
        .filter(total_leads__gt=0)
        .order_by('-won_leads', 'last_name', 'first_name')
    )
    for row in sales_rows:
        row.conversion_pct = (row.won_leads / row.total_leads * 100) if row.total_leads else 0

    unassigned_leads = Lead.objects.filter(assigned_sales__isnull=True).count()
    unassigned_won = Lead.objects.filter(
        assigned_sales__isnull=True,
        status=Lead.Status.WON,
    ).count()

    jobs = (
        Project.objects.filter(status=Project.Status.IN_PROGRESS)
        .select_related('client', 'sales_rep')
        .prefetch_related('stage_progress__stage')
    )
    jobs_in_progress = []
    for project in jobs:
        stages = sorted(
            project.stage_progress.all(),
            key=lambda item: item.stage.sequence_order,
        )
        current = next(
            (item for item in stages if item.status != ProjectStageProgress.Status.COMPLETED),
            stages[-1] if stages else None,
        )
        completed_count = sum(
            1 for item in stages if item.status == ProjectStageProgress.Status.COMPLETED
        )
        jobs_in_progress.append(
            {
                'project': project,
                'current_stage': current,
                'completed_count': completed_count,
                'stage_count': len(stages),
            }
        )

    revenue_by_status = [
        {
            'value': choice.value,
            'label': choice.label,
            'count': Project.objects.filter(status=choice.value).count(),
            'amount': _money(Project.objects.filter(status=choice.value)),
        }
        for choice in Project.Status
    ]
    revenue_total = _money(Project.objects.all())
    max_revenue = max((row['amount'] for row in revenue_by_status), default=Decimal('0'))
    for row in revenue_by_status:
        row['bar_pct'] = float(row['amount'] / max_revenue * 100) if max_revenue else 0

    commission_rows = (
        Staff.objects.annotate(
            commission_total=Coalesce(Sum('commissions__commission_amount'), ZERO),
            commission_paid=Coalesce(
                Sum('commissions__commission_amount', filter=Q(commissions__paid=True)),
                ZERO,
            ),
            commission_unpaid=Coalesce(
                Sum('commissions__commission_amount', filter=Q(commissions__paid=False)),
                ZERO,
            ),
        )
        .filter(commission_total__gt=0)
        .order_by('-commission_total', 'last_name')
    )

    return render(
        request,
        'reporting/dashboard.html',
        {
            'total_leads': total_leads,
            'won_leads': won_leads,
            'lost_leads': lost_leads,
            'conversion_pct': conversion_pct,
            'sales_rows': sales_rows,
            'unassigned_leads': unassigned_leads,
            'unassigned_won': unassigned_won,
            'unassigned_pct': (unassigned_won / unassigned_leads * 100) if unassigned_leads else 0,
            'jobs_in_progress': jobs_in_progress,
            'jobs_count': len(jobs_in_progress),
            'revenue_total': revenue_total,
            'revenue_by_status': revenue_by_status,
            'commission_total': _commission_sum(),
            'commission_paid': _commission_sum(filter=Q(paid=True)),
            'commission_unpaid': _commission_sum(filter=Q(paid=False)),
            'commission_rows': commission_rows,
        },
    )
