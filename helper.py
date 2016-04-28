import constants


def check_domain(user):
    domain = user.email().split('@')[1]
    return domain == constants.DOMAIN

