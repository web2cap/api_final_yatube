from django.conf import settings
from django.core.paginator import Paginator

POST_PER_PAGE = getattr(settings, "POST_PER_PAGE", None)


def paginations(request, data_list):
    """Pagination of data on the pages.
    Acceps to the input REQUEST and LIST with data elements.
    Returns the object of the page."""

    paginator = Paginator(data_list, POST_PER_PAGE)
    page_number = request.GET.get("page")

    return  paginator.get_page(page_number)
