from django.contrib.humanize.templatetags.humanize import intcomma
from django.http import JsonResponse
from django.views import View

from sde.models import Type


class TypeDump(View):
    """Dump of types for autocomplete"""
    def get(self, request):
        return JsonResponse(list(Type.objects.values_list('id', 'name', 'sell')), safe=False)


class TypeSearch(View):
    """Search types"""
    def get(self, request, search):
        types = Type.objects.filter(name__istartswith=search).exclude(market_group__isnull=True).order_by('-mass')
        return JsonResponse(
            [
                {
                    "id": type.id,
                    "name": type.name,
                    "sell": "%s ISK" % intcomma(type.sell),
                    "icon_url": type.icon_url
                } for type in types[:50]
            ],
            safe=False
        )