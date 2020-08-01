def get_or_none(class_model, **kwargs):
    try:
        return class_model.objects.get(**kwargs)
    except class_model.DoesNotExist:
        return None
