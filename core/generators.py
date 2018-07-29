import itertools

from sde.models import AttributeCategory, AttributeType, TypeAttribute


class TypeViewGenerator(object):
    """
    Generates formatted information for the front end so we can keep
    fiddly view logic outside our models, view functions and html
    """
    def __init__(self, type):
        self.type = type

        # Pre-calculate info required for view funcs
        self._type_attributes = self.__type_attributes()
        self._categories = self.__categories()


    def categories(self):
        """Return categories for display with types are displayed elsewhere or shouldn't be displayed pruned"""
        categories = self._categories.copy()
        for category in self._categories:
            if category.name == "NULL":
                del categories[category]
            #elif category.name in ["Shield", "Armor", "Structure"]:
            #    del categories[category]

        return categories


    def defense(self):
        """Returns info for defense panel"""
        


    def __categories(self):
        """
        Builds a dict with the following structure:
        {
            "Attribute Category 1": {
                "Attribute Type 1": "Type Attribute 1",
                "Attribute Type 2": "Type Attribute 2",
            }, 
            "Attribute Category 2": {
                "Attribute Type 3": "Type Attribute 3",
                "Attribute Type 4": "Type Attribute 4",
            }
        }
        """
        attributes = {type_attribute.attribute: type_attribute for type_attribute in self._type_attributes}
        
        categories = {}
        for attribute_type, type_attribute in attributes.items():
            if attribute_type.category not in categories:
                categories[attribute_type.category] = {}

            categories[attribute_type.category][attribute_type] = type_attribute

        return categories


    def __type_attributes(self):
        type_attributes = TypeAttribute.objects.filter(
            type=self.type,
            attribute__published=True
        ).exclude(
            attribute__category__name="NULL"
        ).prefetch_related(
            'attribute',
            'attribute__category',
            'attribute__unit'
        ).all()

        return type_attributes