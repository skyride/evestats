from django.db.models import Count, Q
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
            children = MarketGroup.objects.annotate(
                    children_count=Count('children'),
                    types_count=Count('types')
                ).filter(
                    Q(children_count__gt=0) | Q(types_count__gt=0),
                    parent__isnull=True
                )
            types = []
        else:
            marketgroup = MarketGroup.objects.get(id=marketgroup_id)
            children = marketgroup.children.annotate(
                    children_count=Count('children'),
                    types_count=Count('types')
                ).filter(
                    Q(children_count__gt=0) | Q(types_count__gt=0)
                )
            types = marketgroup.types.prefetch_related("icon", "skin_license", "skin_license__skin").order_by('name')

        context = {
            "node": marketgroup,
            "breadcrumbs": self._generate_breadcrumb_trail(marketgroup),
            "children": children,
            "types": types
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