from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import ProjectForm, ProjectPartnerForm, ProjectUpdateForm, StageProgressForm
from .models import Project, ProjectStage, ProjectStageProgress


def seed_stage_progress(project):
    """Ensure every standard stage has a progress row for this project."""
    for stage in ProjectStage.objects.all():
        ProjectStageProgress.objects.get_or_create(project=project, stage=stage)


def project_list(request):
    status = request.GET.get('status', '')
    search = request.GET.get('q', '').strip()

    projects = Project.objects.select_related('client', 'sales_rep')

    if status and status in Project.Status.values:
        projects = projects.filter(status=status)

    if search:
        projects = projects.filter(
            Q(client__first_name__icontains=search)
            | Q(client__last_name__icontains=search)
            | Q(client__site_address__icontains=search)
        )

    total_count = Project.objects.count()
    status_tabs = [
        {
            'value': choice.value,
            'label': choice.label,
            'count': Project.objects.filter(status=choice.value).count(),
        }
        for choice in Project.Status
    ]

    return render(
        request,
        'construction/project_list.html',
        {
            'projects': projects,
            'status_filter': status,
            'search_query': search,
            'status_tabs': status_tabs,
            'total_count': total_count,
        },
    )


def project_detail(request, pk):
    project = get_object_or_404(
        Project.objects.select_related('client', 'sales_rep'),
        pk=pk,
    )
    seed_stage_progress(project)

    stages = project.stage_progress.select_related('stage').order_by('stage__sequence_order')
    partners = project.project_partners.select_related('partner')
    updates = project.updates.select_related('posted_by')

    return render(
        request,
        'construction/project_detail.html',
        {
            'project': project,
            'stages': stages,
            'partners': partners,
            'updates': updates,
            'partner_form': ProjectPartnerForm(),
            'update_form': ProjectUpdateForm(),
            'stage_status_choices': ProjectStageProgress.Status.choices,
        },
    )


@require_http_methods(['GET', 'POST'])
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            seed_stage_progress(project)
            messages.success(request, f'Project #{project.pk} created.')
            return redirect('construction:project_detail', pk=project.pk)
    else:
        form = ProjectForm()

    return render(
        request,
        'construction/project_form.html',
        {
            'form': form,
            'title': 'New Project',
            'submit_label': 'Create Project',
        },
    )


@require_http_methods(['GET', 'POST'])
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated.')
            return redirect('construction:project_detail', pk=project.pk)
    else:
        form = ProjectForm(instance=project)

    return render(
        request,
        'construction/project_form.html',
        {
            'form': form,
            'project': project,
            'title': f'Edit Project #{project.pk}',
            'submit_label': 'Save Changes',
        },
    )


@require_http_methods(['POST'])
def project_update_stage(request, pk, stage_pk):
    project = get_object_or_404(Project, pk=pk)
    progress = get_object_or_404(
        ProjectStageProgress,
        pk=stage_pk,
        project=project,
    )
    form = StageProgressForm(request.POST, instance=progress)
    if form.is_valid():
        form.save()
        messages.success(request, f'{progress.stage.display_name} updated.')
    else:
        messages.error(request, 'Could not update that stage. Check the dates and status.')
    return redirect('construction:project_detail', pk=project.pk)


@require_http_methods(['POST'])
def project_add_partner(request, pk):
    project = get_object_or_404(Project, pk=pk)
    form = ProjectPartnerForm(request.POST)
    if form.is_valid():
        assignment = form.save(commit=False)
        assignment.project = project
        try:
            assignment.save()
        except IntegrityError:
            messages.error(request, 'That partner is already assigned for this trade role.')
        else:
            messages.success(request, f'{assignment.partner} assigned to this project.')
    else:
        messages.error(request, 'Could not assign partner. Check the form and try again.')
    return redirect('construction:project_detail', pk=project.pk)


@require_http_methods(['POST'])
def project_add_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    form = ProjectUpdateForm(request.POST)
    if form.is_valid():
        entry = form.save(commit=False)
        entry.project = project
        if not entry.update_text and not entry.photo_url:
            messages.error(request, 'Add a note or a photo URL before posting.')
        else:
            entry.save()
            messages.success(request, 'Site update posted.')
    else:
        messages.error(request, 'Could not post that site update.')
    return redirect('construction:project_detail', pk=project.pk)
