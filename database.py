""""근접 지구 물체와 그 근접 접근 방법의 집합을 캡슐화하는 데이터베이스.

'NEO 데이터베이스'는 서로 연결된 NEO 데이터 세트와 근접 접근 방식을 보유하고 있습니다.
주 이름 또는 이름으로 NEO를 가져오는 방법도 제공합니다
다음의 집합과 일치하는 근접 접근법의 집합을 쿼리하는 방법으로서
사용자 지정 기준.

일반적인 상황에서 메인 모듈은 하나의 NEOD 데이터베이스를 생성합니다
'extract.load_neos'에 의해 추출된 NEO와 근접 접근법에 대한 데이터
extract.load_approachs.

작업 2와 작업 3에서 이 파일을 편집합니다.
"""
class NEODatabase:
    def __init__(self, neos, approaches):
        """새로운 `NEODatabase`를 생성합니다.
        이 생성자의 사전 조건으로는 NEO 및 근접 접근 정보의 컬렉션이 아직 연결되지 않았다고 가정합니다. 
        즉, 각 `NearEarthObject`의 `.approaches` 속성은 비어있는 컬렉션을 참조하고 있으며, 
        각 `CloseApproach`의 `.neo` 속성은 None입니다.
        그러나 각 `CloseApproach`에는 해당 NEO의 
        `.designation` 속성과 일치하는 `.designation` 
        속성을 가지고 있습니다. 이 생성자는 제공된 NEO와 근접 접근 정보(approaches)를 연결하여 
        NEO의 각 근접 접근 정보에 대한 컬렉션을 포함하고 각 근접 접근 정보의 
        `.neo` 속성이 해당 NEO를 참조하도록 수정합니다.
        :param neos: `NearEarthObject`의 컬렉션.
        :param approaches: `CloseApproach`의 컬렉션.
        """

        self._neos = neos
        self._approaches = approaches
        for neo in self._neos:
            for approache in self._approaches:
                if approache._designation == neo.designation:
                    neo.approaches.append(approache)
                    approache.neo = neo
    def get_neo_by_designation(self, designation):
        """주요 지정으로 NEO를 찾아서 반환합니다.
        일치하는 항목이 없으면 대신 `None`을 반환합니다.
        데이터 집합의 각 NEO는 문자열로 고유한 주요 지정을 가지고 있습니다.`
        일치는 정확해야 합니다 - 일치하는 항목을 찾을 수 없는 경우 철자와 대문자를 확인하세요.
        :param designation: 찾으려는 NEO의 주요 지정.
        :return: 원하는 주요 지정을 가진 `NearEarthObject` 또는 `None`.
        """
        for neo in self._neos:
            if neo.designation == designation:
                return neo
        return None

    def get_neo_by_name(self, name):
        """이름으로 NEO를 찾아서 반환합니다.

        일치하는 항목이 없으면 대신 `None`을 반환합니다.

        데이터 집합의 모든 NEO에 이름이 있는 것은 아닙니다. NEO와 빈 문자열 또는 `None` 싱글톤은 연결되지 않습니다.

        일치는 정확해야 합니다 - 일치하는 항목을 찾을 수 없는 경우 철자와 대문자를 확인하세요.

        :param name: 찾으려는 NEO의 이름(문자열)입니다.
        :return: 원하는 이름을 가진 `NearEarthObject` 또는 `None`.
        """
        for neo in self._neos:
            if neo.name == name:
                return neo            
        return None

    def query(self, filters=()):
        """일련의 필터와 일치하는 근접 접근을 쿼리하여 생성합니다.

        이는 제공된 모든 필터와 일치하는 `CloseApproach` 객체의 스트림을 생성합니다.

        인수를 제공하지 않으면 모든 알려진 근접 접근을 생성합니다.

        `CloseApproach` 객체는 내부 순서대로 생성되며 의미 있는 순서로 정렬되지 않을 수 있으며, 일반적으로 시간대로 정렬됩니다.

        :param filters: 사용자 지정 기준을 캡처하는 필터의 컬렉션입니다.
        :return: 일치하는 `CloseApproach` 객체의 스트림.
        """
        
        if filters:
            for approach in self._approaches:
                if all(map(lambda f: f(approach), filters)):
                    yield approach
        else:
            for approach in self._approaches:
                yield approach
