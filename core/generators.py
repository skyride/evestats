import itertools
from collections import OrderedDict

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
            elif category.name in ["Shield", "Armor", "Structure", "Fitting", "Drones", "Required Skills"]:
                del categories[category]

        return categories


    def fitting(self):
        for category, attributes in self._categories.items():
            if category.name == "Fitting":
                return attributes

    def drones(self):
        for category, attributes in self._categories.items():
            if category.name == "Drones":
                return attributes


    def shield(self):
        attributes = self.__get_attribute_dict([
            "shieldEmDamageResonance",
            "shieldThermalDamageResonance",
            "shieldKineticDamageResonance",
            "shieldExplosiveDamageResonance",
            "shieldCapacity"
        ])
        if len(attributes) < 5:
            return None

        return {
            "em": attributes["shieldEmDamageResonance"],
            "thermal": attributes["shieldThermalDamageResonance"],
            "kinetic": attributes["shieldKineticDamageResonance"],
            "explosive": attributes["shieldExplosiveDamageResonance"],
            "hp": attributes["shieldCapacity"]
        }


    def armor(self):
        attributes = self.__get_attribute_dict([
            "armorEmDamageResonance",
            "armorThermalDamageResonance",
            "armorKineticDamageResonance",
            "armorExplosiveDamageResonance",
            "armorHP"
        ])
        if len(attributes) < 5:
            return None

        return {
            "em": attributes["armorEmDamageResonance"],
            "thermal": attributes["armorThermalDamageResonance"],
            "kinetic": attributes["armorKineticDamageResonance"],
            "explosive": attributes["armorExplosiveDamageResonance"],
            "hp": attributes["armorHP"]
        }

    
    def structure(self):
        attributes = self.__get_attribute_dict([
            "emDamageResonance",
            "thermalDamageResonance",
            "kineticDamageResonance",
            "explosiveDamageResonance",
            "hp"
        ])
        if len(attributes) < 5:
            return None

        return {
            "em": attributes["emDamageResonance"],
            "thermal": attributes["thermalDamageResonance"],
            "kinetic": attributes["kineticDamageResonance"],
            "explosive": attributes["explosiveDamageResonance"],
            "hp": attributes["hp"]
        }


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
            type_id=self.type.id,
            attribute__published=True
        ).exclude(
            attribute__category__name="NULL"
        ).prefetch_related(
            'attribute',
            'attribute__category',
            'attribute__unit'
        ).all()

        return type_attributes


    def __get_attribute_dict(self, attribute_names):
        attributes = TypeAttribute.objects.filter(
            type_id=self.type.id,
            attribute__name__in=attribute_names
        ).prefetch_related(
            'attribute'
        ).all()
        return {attribute.attribute.name: attribute for attribute in attributes}