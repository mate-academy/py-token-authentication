from django.http import Http404


class NoDetailMixin:
    def retrieve(self, *args, **kwargs):
        raise Http404

    def update(self, *args, **kwargs):
        raise Http404

    def partial_update(self, *args, **kwargs):
        raise Http404

    def destroy(self, *args, **kwargs):
        raise Http404

# noqa