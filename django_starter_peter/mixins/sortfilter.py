from django.db.models.functions import Lower

# TODO:
# - Sort choices need to become properties somehow
# - Derive initial ordering from initial sort_by
# - sortablelist.html should somehow iterate to make its sort-button choices


class SortableListMixin(object):
    ordering = [Lower("name")]
    sort_by = "name"
    _sort_tag = ""

    def __init__(self):
        super().__init__()
        self._sort_tag = self.model.__name__.lower() + "_sort"

    def get_ordering(self):
        # Use session variables to persist sort settings, override with query-args
        self.sort_by = self.request.GET.get(
            "sort", self.request.session.get(self._sort_tag, "name")
        )
        self.request.session[self._sort_tag] = self.sort_by
        if self.sort_by == "-name":
            result = [Lower("name").desc()]
        elif self.sort_by == "name":
            result = [Lower("name")]
        else:
            result = self.sort_by
        return result

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["sort"] = self.sort_by
        return context


class FilterableListMixin(object):
    filter_by = ""
    _filter_tag = ""

    def __init__(self):
        super().__init__()
        self._filter_tag = self.model.__name__.lower() + "_filter"

    def get_queryset(self):
        qs = super().get_queryset()
        # Use session variables to persist filter settings, override with query-args
        self.filter_by = self.request.GET.get(
            "filter", self.request.session.get(self._filter_tag, "")
        )
        self.request.session[self._filter_tag] = self.filter_by
        if self.filter_by:
            qs = qs.filter(name__icontains=self.filter_by)
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["unfiltered_count"] = self.model.objects.count
        context["filter"] = self.filter_by
        return context
