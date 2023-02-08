from math import ceil

from django.core.paginator import Paginator


def make_pagination_range(page_range, qt_pages, current_page):
    total_pages = len(page_range)
    middle_range = ceil(qt_pages / 2)
    start_range = min(total_pages - qt_pages,
                      max(0, current_page - middle_range))
    stop_range = min(total_pages,
                     max(qt_pages, current_page + middle_range))
    pagination = page_range[start_range:stop_range]
    return {
        'pagination': pagination,
        'page_range': page_range,
        'qt_pages': qt_pages,
        'current_page': current_page,
        'total_pages': total_pages,
        'start_range': start_range,
        'stop_range': stop_range,
        'first_page_out_of_range': current_page > middle_range,
        'last_page_out_of_range': stop_range < total_pages,
    }


def make_pagination(request, queryset, per_page, qt_pages=4):
    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1
    paginator = Paginator(queryset, per_page)
    page_obj = paginator.get_page(current_page)
    pagination_range = make_pagination_range(
        paginator.page_range, qt_pages, current_page,
    )
    return page_obj, pagination_range
