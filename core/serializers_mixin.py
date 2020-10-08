from django.db.models import QuerySet
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.db.models.fields import Point


class DistanceSerializerMixin:

    out_field_name = 'distance'
    point_field_name = 'coordinates'
    measure = 'km'
    srid = 4326

    def __init__(self, instance_or_qs=None, *args, **kwargs):
        self._initial_coordinates = kwargs.pop('c', None)
        super().__init__(instance_or_qs, *args, **kwargs)

    def __new__(cls, instance_or_qs=None, coordinates=None, **kwargs):
        if coordinates is None:
            return super().__new__(cls, instance_or_qs, **kwargs)

        pnt = Point(coordinates, srid=cls.srid)
        query = {cls.out_field_name: Distance(cls.point_field_name, pnt)}

        if kwargs.get('many', False) and isinstance(instance_or_qs, QuerySet):
            qs = instance_or_qs.exclude(**{cls.point_field_name: None})
            qs = qs.annotate(**query).order_by(cls.out_field_name)
            serializer = super().__new__(cls, qs, c=coordinates, **kwargs)
        else:
            if getattr(instance_or_qs, cls.point_field_name) is None:
                raise RuntimeError(f'Instance field *{cls.point_field_name}*  has NULL value')

            instance = cls.Meta.model.filter(pk=instance_or_qs.pk).annotate(**query).get()
            serializer = super().__new__(cls, instance, c=coordinates, **kwargs)

        return serializer

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if not hasattr(instance, self.out_field_name):
            return ret

        distance = getattr(instance, self.out_field_name)
        ret['geo'] = {'from': tuple(self._initial_coordinates),
                      'to': getattr(instance, self.point_field_name).tuple,
                      'distance': getattr(distance, self.measure),
                      'measure': self.measure}
        return ret
