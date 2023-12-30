import operator

class UnsupportedCriterionError(NotImplementedError):
    """필터 기준은 지원되지 않습니다."""
    pass

class AttributeFilter:
    """비교 가능한 속성에 대한 필터링을 위한 일반적인 수퍼 클래스입니다.
    AttributeFilter는 가까운 접근(또는 연결된 NEO)의 특정 속성을 참조 값과 비교하는 검색 기준 패턴을 나타냅니다. 
    사실상 CloseApproach 객체가 인코딩된 기준을 만족하는지 여부를 확인하는 호출 가능한 조건자 역할을 합니다.
    비교 연산자와 참조 값으로 구성되며, 이 필터를 호출하면 (call 사용) get(approach) OP value (중위 표기법)를 실행합니다.
    구체적인 서브 클래스는 주어진 CloseApproach에서 원하는 속성을 검색하기 위해 get 클래스 메서드를 오버라이드하여 사용자 정의 동작을 제공할 수 있습니다.
    """
    def __init__(self, op, value):
        """
        이너리 술부 함수와 참조 값에서 새로운 AttributeFilter를 구성합니다.
        참조 값은 연산자 함수의 두 번째(오른쪽) 인자로 제공됩니다. 예를 들어, op=operator.le 및 value=10을 가진 AttributeFilter는 접근에 대해 호출되면 some_attribute <= 10을 평가합니다.
        :param op: 2-인자 술부 비교자(예: operator.le).
        :param value: 비교 대상이 되는 참조 값입니다.
        """
        self.op = op
        self.value = value

    def __call__(self, approach):
        """self(approach)를 호출합니다."""
        return self.op(self.get(approach), self.value)

    @classmethod
    def get(cls, approach):
        """
        가까운 접근에서 관심 있는 속성을 가져옵니다.
        구상 서브클래스는 이 메서드를 재정의하여 제공된 'CloseApproach'에서 관심 있는 속성을 가져와야 합니다.
        :param approach: 이 필터를 평가할 'CloseApproach'.
        :return: 'self.value'를 통해 'self.op'와 비교 가능한 관심 있는 속성의 값.
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
        "hazardous": False if hazardous == '--not-hazardous' else True
    }

    filters = []
    if filter_dic["date"]:
        filters.append(DateFilter(operator.eq, filter_dic["date"]))
    if filter_dic["start_date"]:
        filters.append(DateFilter(operator.ge, filter_dic["start_date"]))
    if filter_dic["end_date"]:
        filters.append(DateFilter(operator.le, filter_dic["end_date"]))
    if filter_dic["distance_min"]:
        filters.append(DistanceFilter(operator.ge, filter_dic["distance_min"]))
    if filter_dic["distance_max"]:
        filters.append(DistanceFilter(operator.le, filter_dic["distance_max"]))
    if filter_dic["velocity_min"]:
        filters.append(VelocityFilter(operator.ge, filter_dic["velocity_min"]))
    if filter_dic["velocity_max"]:
        filters.append(VelocityFilter(operator.le, filter_dic["velocity_max"]))
    if filter_dic["diameter_min"]:
        filters.append(DiameterFilter(operator.ge, filter_dic["diameter_min"]))
    if filter_dic["diameter_max"]:
        filters.append(DiameterFilter(operator.le, filter_dic["diameter_max"]))
    if filter_dic["hazardous"] is not None:
        filters.append(HazardousFilter(operator.eq, filter_dic["hazardous"]))

    return filters

def limit(iterator, n=None):
    if n == 0 or n is None:
        return iterator
    return [x for i, x in enumerate(iterator) if i < n]
