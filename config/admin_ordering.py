"""
Custom ordering for apps and models shown in Django Admin sidebars.
"""

from django.contrib import admin

# App sections order in the Admin index / sidebar
APP_ORDER = {
    'auth': 10,  # Authentication and Authorization
    'accounts': 20,
    'crm': 30,
    'construction': 40,
    'partners': 50,
    'reporting': 60,
}

# Within each app: model object_name -> sort rank
MODEL_ORDER = {
    'crm': {
        'Lead': 1,
        'Client': 2,
        'Commission': 3,
    },
    # Option B: daily ops first, lookup tables last
    'construction': {
        'Project': 1,
        'ProjectStageProgress': 2,
        'ProjectUpdate': 3,
        'ProjectStage': 4,
    },
}

_original_get_app_list = admin.site.get_app_list


def get_app_list(request, app_label=None):
    app_list = _original_get_app_list(request, app_label)

    for app in app_list:
        order_map = MODEL_ORDER.get(app.get('app_label'), {})
        if order_map:
            app['models'].sort(
                key=lambda model: order_map.get(model['object_name'], 99)
            )

    app_list.sort(
        key=lambda app: APP_ORDER.get(app.get('app_label'), 999)
    )

    return app_list


admin.site.get_app_list = get_app_list
