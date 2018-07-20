from sde.models import Type


def generate_breadcrumb_trail(marketgroup):
    def recurse(node):
        """Return an list containing the path to this trail"""
        if isinstance(node, dict):
            return []
        elif isinstance(node, Type):
            return [*recurse(node.market_group), node]
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