import itertools

from django.db.models import Count, Q
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

from sde.models import MarketGroup, Type, AttributeCategory

from core.helpers import generate_breadcrumb_trail


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
            types = marketgroup.types.filter(
                    published__isnull=False
                ).prefetch_related(
                    "icon", "skin_license", "skin_license__skin"
                ).order_by(
                    'skin_license__skin__material_id', 'name'
                ).distinct()

        context = {
            "node": marketgroup,
            "breadcrumbs": generate_breadcrumb_trail(marketgroup),
            "children": children,
            "types": types
        }
        return render(request, "core/marketgroup.html", context)



class TypeView(View):
    """Provides detailed information on a single type"""
    def get(self, request, type_id):

        type = Type.objects.get(id=type_id)

        categories = AttributeCategory.objects.filter(
            types__types__type_id=type_id    
        ).distinct()

        context = {
            "type": type,
            "breadcrumbs": generate_breadcrumb_trail(type),
            "categories": categories
        }
        return render(request, "core/type.html", context)