# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re

from django.db import models

from math import pow, sqrt


# Map
class Region(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100, db_index=True)
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    radius = models.FloatField(null=True)

    def __str__(self):
        return "%s:%s" % (self.id, self.name)


class Constellation(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100, db_index=True)
    region = models.ForeignKey(Region, related_name="constellations", on_delete=models.CASCADE)
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    radius = models.FloatField(null=True)

    def __str__(self):
        return "%s:%s" % (self.id, self.name)


class System(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100, db_index=True)
    region = models.ForeignKey(Region, related_name="systems", on_delete=models.CASCADE)
    constellation = models.ForeignKey(Constellation, related_name="systems", on_delete=models.CASCADE)
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    luminosity = models.FloatField()
    border = models.BooleanField()
    fringe = models.BooleanField()
    corridor = models.BooleanField()
    hub = models.BooleanField()
    international = models.BooleanField()
    security = models.FloatField()
    radius = models.FloatField(null=True)
    sun = models.ForeignKey('Type', null=True, default=None, on_delete=models.CASCADE)
    security_class = models.CharField(max_length=2, null=True)

    def __str__(self):
        return "%s:%s" % (self.id, self.name)


    # Compares distance between self and a target system
    def distance(self, target, ly=False):
        x = pow(target.x - self.x, 2)
        y = pow(target.y - self.y, 2)
        z = pow(target.z - self.z, 2)

        distance = sqrt(x + y + z)
        if ly:
            return distance / 9460730472580800
        else:
            return distance


class SystemJump(models.Model):
    origin = models.ForeignKey(System, related_name="jumps_origin", on_delete=models.CASCADE)
    destination = models.ForeignKey(System, related_name="jumps_destination", on_delete=models.CASCADE)


# Icons
path_pattern = re.compile("res:/ui/texture/icons/", re.IGNORECASE)
class Icon(models.Model):
    id = models.IntegerField(primary_key=True)
    icon_file = models.TextField()
    description = models.TextField()

    @property
    def path(self):
        return "https://img.skyride.org/eve/icons/items/%s" % path_pattern.sub("", self.icon_file).lower()


# Units
unit_pattern = re.compile("([0-9]+)=(\w+)")
class Unit(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=96)
    display_name = models.CharField(max_length=128, null=True)
    description = models.TextField(null=True)

    # Stick this unit on the end of a value
    def affix(self, value):
        if value is None:
            return value
        elif self.id == 108:
            return "%s%%" % round(((1 - value) * 100))
        elif self.id == 109:
            out = (value - 1) * 100
            out = '{0:.2f}'.format(out)
            if value >= 1.0:
                return ("+%s%%" % out).replace("0%", "%").replace(".0%", "%")
            else:
                return ("%s%%" % out).replace("0%", "%").replace(".0%", "%")
        elif self.id == 111:
            return '{0:.1f}%'.format((1 - value) * 100)
        elif self.id == 116:
            return Type.objects.get(id=value).name
        elif self.display_name is None:
            return str(value)
        elif unit_pattern.search(self.display_name):
            matches = unit_pattern.findall(self.display_name)
            enum = {key: value for key, value in matches}
            if str(int(value)) in enum:
                return enum[str(int(value))]
            else:
                return "Invalid Enum: %s" % value
        else:
            return "%s %s" % (value, self.display_name)


# Types
class MarketGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    parent = models.ForeignKey('self', null=True, related_name="children", default=None, db_constraint=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    icon = models.ForeignKey(Icon, related_name="market_groups", null=True, on_delete=models.SET_NULL)
    has_types = models.BooleanField()

    def __str__(self):
        return "%s:%s" % (self.id, self.name)

    class Meta:
        ordering = ('name', )


class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, db_index=True)
    icon_id = models.IntegerField(null=True)
    published = models.BooleanField()

    def __str__(self):
        return "%s:%s" % (self.id, self.name)


class Group(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, db_index=True)
    category = models.ForeignKey(Category, related_name="groups", on_delete=models.CASCADE)
    icon_id = models.IntegerField(null=True)
    anchored = models.BooleanField()
    anchorable = models.BooleanField()
    fittable_non_singleton = models.BooleanField()
    published = models.BooleanField()

    def __str__(self):
        return "%s:%s" % (self.id, self.name)


class Type(models.Model):
    id = models.IntegerField(primary_key=True)
    group = models.ForeignKey(Group, related_name="types", null=True, default=None, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField()
    mass = models.FloatField(null=True)
    volume = models.FloatField(null=True)
    capacity = models.FloatField(null=True)
    published = models.BooleanField()
    market_group = models.ForeignKey(MarketGroup, related_name="types", null=True, on_delete=models.CASCADE)
    icon = models.ForeignKey(Icon, related_name="types", null=True, on_delete=models.SET_NULL)

    buy = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    sell = models.DecimalField(max_digits=16, decimal_places=2, default=0)

    @property
    def icon_url(self):
        if self.skin_license.count() > 0:
            return "https://img.skyride.org/eve/icons/ui/skinicons/%s.png" % self.skin_license.first().skin.material_id
        else:
            return "https://imageserver.eveonline.com/Type/%s_64.png" % self.id

    def __str__(self):
        return "%s:%s" % (self.id, self.name)


class AttributeCategory(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, null=True)
    description = models.CharField(max_length=200, null=True)


class AttributeType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=400)
    category = models.ForeignKey(AttributeCategory, null=True, db_constraint=False, related_name="types", on_delete=models.CASCADE)

    description = models.CharField(max_length=1000, null=True)
    icon = models.ForeignKey(Icon, null=True, on_delete=models.CASCADE)
    default_value = models.IntegerField(null=True)
    published = models.BooleanField(db_index=True)
    display_name = models.CharField(max_length=150, null=True)
    unit = models.ForeignKey(Unit, null=True, on_delete=models.SET_NULL)
    stackable = models.BooleanField()
    high_is_good = models.BooleanField()


class TypeAttribute(models.Model):
    type = models.ForeignKey(Type, related_name="attributes", on_delete=models.CASCADE)
    attribute = models.ForeignKey(AttributeType, related_name="types", on_delete=models.CASCADE)
    value_int = models.IntegerField(null=True)
    value_float = models.FloatField(null=True)

    def __str__(self):
        return "%s (%s)" % (
            self.attribute.name,
            self.value
        )

    def value(self):
        if self.value_int != None:
            return self.value_int
        else:
            return self.value_float

    def display_value(self):
        if self.attribute.unit is not None:
            return self.attribute.unit.affix(self.value())
        else:
            return self.value()


class Station(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100, db_index=True)
    type = models.ForeignKey(Type, null=True, default=None, on_delete=models.CASCADE)
    system = models.ForeignKey(System, null=True, default=None, on_delete=models.CASCADE)
    x = models.FloatField(default=0)
    y = models.FloatField(default=0)
    z = models.FloatField(default=0)

    # Is the station a structure or an NPC station
    structure = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True, db_index=True)

    # Used to add structures
    @staticmethod
    def get_or_create(id, api):
        # Check database for station/structure
        station = Station.objects.filter(id=id).first()
        if station != None:
            return station

        # Check for structure
        if id > 71000914:
            r = api.get("/v1/universe/structures/%s/" % id)
            if r != None:
                station = Station(
                    id=id,
                    name=r['name'],
                    type_id=r['type_id'],
                    system_id=r['solar_system_id'],
                    x=r['position']['x'],
                    y=r['position']['y'],
                    z=r['position']['z']
                )
                station.save()
            else:
                station = Station(
                    id=id,
                    name="**UNKNOWN**"
                )
                station.save()
            return station
        else:
            # Try regular station
            r = api.get("/v2/universe/stations/%s/" % id)
            if r != None:
                station = Station(
                    id=id,
                    name=r['name'],
                    type_id=r['type_id'],
                    system_id=r['system_id'],
                    x=r['position']['x'],
                    y=r['position']['y'],
                    z=r['position']['z']
                )
                station.save()
                return station


# Skins
class Skin(models.Model):
    """A skin e.g. Sansha Victory, IGC"""
    id = models.IntegerField(primary_key=True)
    name = models.CharField(null=True, max_length=128, db_index=True)
    material_id = models.IntegerField(null=True, db_index=True)


class SkinLicense(models.Model):
    """A skin license that maps typeIDs to skins"""
    type = models.ForeignKey(Type, related_name="skin_license", null=True, on_delete=models.CASCADE)
    duration = models.IntegerField(null=True)
    skin = models.ForeignKey(Skin, related_name="licenses", null=True, on_delete=models.CASCADE)