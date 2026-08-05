from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import ConvertToClientForm, LeadForm
from .models import Lead


def lead_list(request):
    status = request.GET.get('status', '')
    search = request.GET.get('q', '').strip()

    leads = Lead.objects.select_related('assigned_sales')

    if status and status in Lead.Status.values:
        leads = leads.filter(status=status)

    if search:
        leads = leads.filter(
            Q(first_name__icontains=search)
            | Q(last_name__icontains=search)
            | Q(email__icontains=search)
            | Q(phone__icontains=search)
            | Q(mobile__icontains=search)
        )

    total_count = Lead.objects.count()
    status_tabs = [
        {
            'value': choice.value,
            'label': choice.label,
            'count': Lead.objects.filter(status=choice.value).count(),
        }
        for choice in Lead.Status
    ]

    return render(
        request,
        'crm/lead_list.html',
        {
            'leads': leads,
            'status_filter': status,
            'search_query': search,
            'status_tabs': status_tabs,
            'total_count': total_count,
        },
    )


def lead_detail(request, pk):
    lead = get_object_or_404(
        Lead.objects.select_related('assigned_sales'),
        pk=pk,
    )
    clients = lead.clients.all()

    return render(
        request,
        'crm/lead_detail.html',
        {
            'lead': lead,
            'clients': clients,
            'can_convert': lead.status == Lead.Status.WON and not clients.exists(),
        },
    )


@require_http_methods(['GET', 'POST'])
def lead_create(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save()
            messages.success(request, f'Lead "{lead.first_name} {lead.last_name}" created.')
            return redirect('crm:lead_detail', pk=lead.pk)
    else:
        form = LeadForm()

    return render(
        request,
        'crm/lead_form.html',
        {
            'form': form,
            'title': 'New Lead',
            'submit_label': 'Create Lead',
        },
    )


@require_http_methods(['GET', 'POST'])
def lead_edit(request, pk):
    lead = get_object_or_404(Lead, pk=pk)

    if request.method == 'POST':
        form = LeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lead updated.')
            return redirect('crm:lead_detail', pk=lead.pk)
    else:
        form = LeadForm(instance=lead)

    return render(
        request,
        'crm/lead_form.html',
        {
            'form': form,
            'lead': lead,
            'title': f'Edit Lead — {lead.first_name} {lead.last_name}',
            'submit_label': 'Save Changes',
        },
    )


@require_http_methods(['GET', 'POST'])
def lead_convert_to_client(request, pk):
    lead = get_object_or_404(Lead, pk=pk)

    if lead.status != Lead.Status.WON:
        messages.error(request, 'Only won leads can be converted to clients.')
        return redirect('crm:lead_detail', pk=lead.pk)

    if lead.clients.exists():
        messages.error(request, 'This lead has already been converted to a client.')
        return redirect('crm:lead_detail', pk=lead.pk)

    if request.method == 'POST':
        form = ConvertToClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.lead = lead
            client.first_name = lead.first_name
            client.last_name = lead.last_name
            client.phone = lead.phone
            client.mobile = lead.mobile
            client.email = lead.email
            client.save()
            messages.success(
                request,
                f'Client "{client.first_name} {client.last_name}" created from lead.',
            )
            return redirect('crm:lead_detail', pk=lead.pk)
    else:
        form = ConvertToClientForm()

    return render(
        request,
        'crm/lead_convert.html',
        {
            'lead': lead,
            'form': form,
        },
    )
