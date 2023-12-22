"""가까운 접근을 조회하고 생성된 결과를 제한하는 필터를 제공합니다.
create_filters 함수는 query 메서드에서 사용되는 객체 컬렉션을 생성하여 원하는 모든 기준을 충족하는 CloseApproach 객체 스트림을 생성합니다. 
create_filters에 대한 인수는 메인 모듈에서 제공되며 사용자의 명령줄 옵션에서 유래합니다.
이 함수는 AttributeFilter의 하위 클래스 인스턴스 컬렉션을 반환하는 것으로 생각할 수 있습니다. 이 클래스는 1개의 인수 ( CloseApproach에 대한 호출)를 취하는 callable이며, 
이 callable은 operator 모듈의 comparator, 참조 값을, 그리고 하위 클래스가 제공된 CloseApproach에서 관심 있는 속성을 가져올 수 있는 클래스 메서드 get을 구성합니다.
limit 함수는 반복자에서 생성된 값의 최대 수를 제한합니다.
"""
import operator


class UnsupportedCriterionError(NotImplementedError):
    "필터 기준은 지원되지 않습니다."





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


def create_filters(
        date=None, start_date=None, end_date=None,
        distance_min=None, distance_max=None,
        velocity_min=None, velocity_max=None,
        diameter_min=None, diameter_max=None,
        hazardous=None
):
    """사용자 지정 기준으로부터 필터 컬렉션을 생성합니다.
    각 인자는 메인 모듈에서 명령줄의 사용자 옵션에서 값을 제공합니다. 각각은 다른 유형의 필터에 해당합니다. 예를 들어, 
    --date 옵션은 date 인자에 해당하며, 정확히 해당하는 날짜에 발생한 가까운 접근을 선택하는 필터를 나타냅니다. 마찬가지로, --min-distance 옵션은 distance_min 인자에 해당하며, 
    명목 접근 거리가 지정된 거리 이상인 가까운 접근을 선택하는 필터를 나타냅니다. 
    각 옵션은 명령줄에서 지정되지 않으면 None입니다(특히, --not-hazardous 플래그는 hazardous=False로 결과가 나오며, hazardous=None과 혼동해서는 안 됩니다).
    반환 값은 NEODatabase의 query 메서드와 호환되어야 합니다. 일단은 이것을 AttributeFilter의 컬렉션으로 생각할 수 있습니다.
    :param date: 일치하는 CloseApproach가 발생하는 date.
    :param start_date: 일치하는 CloseApproach가 발생하는 날짜 이후이거나 해당하는 date.
    :param end_date: 일치하는 CloseApproach가 발생하는 날짜 이전이거나 해당하는 date.
    :param distance_min: 일치하는 CloseApproach의 최소 명목 접근 거리.
    :param distance_max: 일치하는 CloseApproach의 최대 명목 접근 거리.
    :param velocity_min: 일치하는 CloseApproach의 최소 상대 접근 속도.
    :param velocity_max: 일치하는 CloseApproach의 최대 상대 접근 속도.
    :param diameter_min: 일치하는 CloseApproach의 NEO의 최소 지름.
    :param diameter_max: 일치하는 CloseApproach의 NEO의 최대 지름.
    :param hazardous: 일치하는 CloseApproach의 NEO가 잠재적으로 위험한지 여부.
    :return: query와 함께 사용할 필터 컬렉션."
    """
    
    filter_dic = {"date" : date, 
                  "start_date" :start_date, 
                  "end_date" : end_date, 
                  "distance_min" : distance_min, 
                  "distance_max":distance_max, 
                  "velocity_min":velocity_min, 
                  "velocity_max":velocity_max,
                  "diameter_min": diameter_min,
                  "diameter_max": diameter_max,
                  "hazardous": False if hazardous == '--not-hazardous' else True
                  }

    # TODO: Decide how you will represent your filters.
    
    return filter_dic


def limit(iterator, n=None):
    """반복자에서 제한된 값의 스트림을 생성합니다.

    n이 0이거나 None인 경우, 반복자를 전혀 제한하지 않습니다.

    :param iterator: 값의 반복자입니다.
    :param n: 생성할 최대 값 수입니다.
    :yield: 반복자에서 첫 번째 (최대) n개의 값."""
    # TODO: Produce at most `n` values from the given iterator.
    return iterator
