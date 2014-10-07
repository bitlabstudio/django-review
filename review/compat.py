try:
    from django.contrib.auth import get_user_model
except ImportError:  # Django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()


USER_MODEL = {
    'orm_label': '%s.%s' % (User._meta.app_label, User._meta.object_name),
    'model_label': '%s.%s' % (User._meta.app_label, User._meta.module_name),
    'object_name': User.__name__,
}
