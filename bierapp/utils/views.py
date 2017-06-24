from django.core import paginator

from bierapp.utils.types import get_int


class Paginator(paginator.Paginator):
    def pages_to_show(self, page):
        # pages_wanted stores the pages we want to see, e.g.
        #  - first and second page always
        #  - two pages before selected page
        #  - the selected page
        #  - two pages after selected page
        #  - last two pages always
        #
        # Turning the pages into a set removes duplicates for edge
        # cases where the "context pages" (before and after the
        # selected) overlap with the "always show" pages.
        pages_wanted = set([1,2,
                            page-3, page-2, page-1,
                            page,
                            page+1, page+2, page+3,
                            self.num_pages-1, self.num_pages])

        # The intersection with the page_range trims off the invalid
        # pages outside the total number of pages we actually have.
        # Note that includes invalid negative and >page_range "context
        # pages" which we added above.
        pages_to_show = set(self.page_range).intersection(pages_wanted)
        pages_to_show = sorted(pages_to_show)

        # skip_pages will keep a list of page numbers from
        # pages_to_show that should have a skip-marker inserted
        # after them.  For flexibility this is done by looking for
        # anywhere in the list that doesn't increment by 1 over the
        # last entry.
        skip_pages = [
            x[1] for x in zip(pages_to_show[:-1], pages_to_show[1:])
            if (x[1] - x[0] != 1)
        ]

        # Each page in skip_pages should be follwed by a skip-marker
        # sentinel (e.g. -1).
        for i in skip_pages:
            pages_to_show.insert(pages_to_show.index(i), -1)

        return pages_to_show


def paginate(request, objects, limit=15):
    # Build paginator with specific limit
    limit = get_int(request.GET, 'limit', limit)
    pages = Paginator(objects, limit)

    # Navigate to the requested page
    try:
        objects = pages.page(request.GET.get('page'))
    except (paginator.PageNotAnInteger, paginator.EmptyPage):
        objects = pages.page(1)

    # Calculate pages to show
    pages.show_page_range = pages.pages_to_show(objects.number)

    # Done
    return objects
