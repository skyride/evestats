from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

from sde.models import MarketGroup


class MarketGroupView(View):
    """List view of market groups"""
    def get(self, request, marketgroup_id=None):
        if marketgroup_id is None:
            marketgroup = {
                "name": "Market Groups",
                "description": "Browse through the market groups below",

            }
            children = MarketGroup.objects.filter(parent__isnull=True)
        else:
            marketgroup = MarketGroup.objects.get(id=marketgroup_id)
            children = marketgroup.children

        context = {
            "node": marketgroup,
            "children": children
        }
        return render(request, "core/marketgroup.html", context)