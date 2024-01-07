import operator

class UnsupportedCriterionError(NotImplementedError):
    """필터 기준은 지원되지 않습니다."""
    pass

class AttributeFilter:
    """A general superclass for filters on comparable attributes.

    An `AttributeFilter` represents the search criteria pattern comparing some
    attribute of a close approach (or its attached NEO) to a reference value. It
    essentially functions as a callable predicate for whether a `CloseApproach`
    object satisfies the encoded criterion.

    It is constructed with a comparator operator and a reference value, and
    calling the filter (with __call__) executes `get(approach) OP value` (in
    infix notation).

    Concrete subclasses can override the `get` classmethod to provide custom
    behavior to fetch a desired attribute from the given `CloseApproach`.
    """

    def __init__(self, op, value):
        """Construct a new `AttributeFilter` from an binary predicate and a reference value.

        The reference value will be supplied as the second (right-hand side)
        argument to the operator function. For example, an `AttributeFilter`
        with `op=operator.le` and `value=10` will, when called on an approach,
        evaluate `some_attribute <= 10`.

        :param op: A 2-argument predicate comparator (such as `operator.le`).
        :param value: The reference value to compare against.
        """
        self.op = op
        self.value = value

    def __call__(self, approach):
        """Invoke `self(approach)`."""
        return self.op(self.get(approach), self.value)

    @classmethod
    def get(cls, approach):
        """Get an attribute of interest from a close approach.

        Concrete subclasses must override this method to get an attribute of
        interest from the supplied `CloseApproach`.

        :param approach: A `CloseApproach` on which to evaluate this filter.
        :return: The value of an attribute of interest, comparable to `self.value` via `self.op`.
        """
        raise UnsupportedCriterionError

    def __repr__(self):
        return f"{self.__class__.__name__}(op=operator.{self.op.__name__}, value={self.value})"

class DistanceFilter(AttributeFilter):
    @classmethod
    def get(cls, approach):
        return approach.distance

class DateFilter(AttributeFilter):
    @classmethod
    def get(cls, approach):
        return approach.time.date()

class VelocityFilter(AttributeFilter):
    @classmethod
    def get(cls, approach):
        return approach.velocity

class DiameterFilter(AttributeFilter):
    @classmethod
    def get(cls, approach):
        return approach.neo.diameter

class HazardousFilter(AttributeFilter):
    @classmethod
    def get(cls, approach):
        return approach.neo.hazardous

def create_filters(
        date=None, start_date=None, end_date=None,
        distance_min=None, distance_max=None,
        velocity_min=None, velocity_max=None,
        diameter_min=None, diameter_max=None,
        hazardous=None
):
    filter_dic = {
        "date": date,
        "start_date": start_date,
        "end_date": end_date,
        "distance_min": distance_min,
        "distance_max": distance_max,
        "velocity_min": velocity_min,
        "velocity_max": velocity_max,
        "diameter_min": diameter_min,
        "diameter_max": diameter_max,
        "hazardous": hazardous
    }

    filters = []
    if filter_dic["date"] is not None:
        filters.append(DateFilter(operator.eq, filter_dic["date"]))

    if filter_dic["start_date"] is not None:
        filters.append(DateFilter(operator.ge, filter_dic["start_date"]))

    if filter_dic["end_date"] is not None:
        filters.append(DateFilter(operator.le, filter_dic["end_date"]))

    if filter_dic["distance_min"] is not None:
        filters.append(DistanceFilter(operator.ge, filter_dic["distance_min"]))

    if filter_dic["distance_max"] is not None:
        filters.append(DistanceFilter(operator.le, filter_dic["distance_max"]))

    if filter_dic["velocity_min"] is not None:
        filters.append(VelocityFilter(operator.ge, filter_dic["velocity_min"]))

    if filter_dic["velocity_max"] is not None:
        filters.append(VelocityFilter(operator.le, filter_dic["velocity_max"]))

    if filter_dic["diameter_min"] is not None:
        filters.append(DiameterFilter(operator.ge, filter_dic["diameter_min"]))

    if filter_dic["diameter_max"] is not None:
        filters.append(DiameterFilter(operator.le, filter_dic["diameter_max"]))
        
    if filter_dic["hazardous"] is not None:
        filters.append(HazardousFilter(operator.eq, filter_dic["hazardous"]))

    return filters

def limit(iterator, n=None):
    if n == 0 or n is None:
        return iterator
    return [x for i, x in enumerate(iterator) if i < n]
