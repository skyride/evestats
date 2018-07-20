import os
import requests

from django.core.management.base import BaseCommand
from django.db import transaction

from sde.models import Type


class Command(BaseCommand):
    help = "Downloads the SDE file from fuzzworks"

    def handle(self, *args, **options):
        id_chunks = self.chunks(
            list(
                Type.objects.filter(
                    published=True,
                    market_group__isnull=False
                ).values_list(
                    'id',
                    flat=True
                )
            ),
            500
        )

        for chunk in id_chunks:
            self.update_prices(chunk)
        print("Updated Prices")

    
    def chunks(self, l, n):
            for i in range(0, len(l), n):
                yield l[i:i + n]


    def update_prices(self, item_ids):
        r = requests.get(
            "https://market.fuzzwork.co.uk/aggregates/",
            params={
                "region": 10000002,
                "types": ",".join(map(str, item_ids))
            }
        ).json()

        with transaction.atomic():
            for key in r.keys():
                item = r[key]
                db_type = Type.objects.get(id=int(key))
                db_type.buy = item['buy']['percentile']
                db_type.sell = item['sell']['percentile']
                db_type.save()

        print("Price updates completed for %s:%s" % (
            item_ids[0],
            item_ids[-1]
        ))