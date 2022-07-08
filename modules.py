from __future__ import division
from urllib import parse
import math

import tornado.web


def update_querystring(url, **kwargs):
    split_result = parse.urlsplit(url)
    query_args = parse.parse_qs(split_result.query)
    query_args.update(kwargs)
    for arg_name, arg_value in kwargs.items():
        if arg_value is None:
            if hasattr(query_args, arg_name):
                del query_args[arg_name]

    k = list(query_args.items())[0][0]
    v = list(query_args.items())[0][1]
    query_string = k+"="+str(v)
    return parse.urlunsplit((split_result.scheme, split_result.netloc,
        split_result.path, query_string, split_result.fragment))


class Paginator(tornado.web.UIModule):
    """Pagination links display."""

    def render(self, page, page_size, results_count):
        pages = int(math.ceil(results_count / page_size)) if results_count else 0

        def get_page_url(page):
            # don't allow ?page=1
            if page <= 1:
                page = None
            return update_querystring(self.request.uri, page=page)

        next = page + 1 if page < pages else None
        previous = page - 1 if page > 1 else None

        return self.render_string('uimodules/pagination.html', page=page, pages=pages, next=next,
            previous=previous, get_page_url=get_page_url)
