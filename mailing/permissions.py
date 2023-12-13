def is_manager(user):
    return user.groups.filter(name='Менеджер').exists()


def is_creator(creator, user):
    return creator == user


def is_su(user):
    return user.is_superuser