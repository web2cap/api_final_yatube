from django.utils import timezone


def year(request):
    """ Adds a variable with the current year """

    now = timezone.now()
    return {"year": now.year}
