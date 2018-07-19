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
            "children": children,
            "breadcrumbs": self._generate_breadcrumb_trail(marketgroup)
        }
        return render(request, "core/marketgroup.html", context)


    def _generate_breadcrumb_trail(self, marketgroup):
        def recurse(node):
            """Return an list containing the path to this trail"""
            if isinstance(node, dict):
                return []
            elif node.parent is None:
                return [node]
            else:
                return [*recurse(node.parent), node]

        return [
            {
                "name": "Market",
                "root": True
            },
            *recurse(marketgroup)
        ]