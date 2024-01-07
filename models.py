"""근지 천체와 그들의 근접 접근을 나타내는 모델을 표현합니다.

`NearEarthObject` 클래스는 근지 천체를 나타냅니다. 각각의 천체는 고유한 기본 지정, 선택적인 고유한 이름, 선택적인 지름, 그리고 천체가 잠재적으로 위험한지를 나타내는 플래그를 가지고 있습니다.

`CloseApproach` 클래스는 NEO에 의한 지구 근접 접근을 나타냅니다. 각각의 접근은 접근 일시, 명목적인 접근 거리, 상대적인 접근 속도를 가지고 있습니다.

`NearEarthObject`는 자신의 근접 접근들의 컬렉션을 유지하며, `CloseApproach`는 그것이 참조하는 NEO를 유지합니다.

이러한 객체를 구성하는 함수들은 NASA의 데이터 파일에서 추출된 정보를 사용하므로, 이러한 객체들은 이름이 누락되거나 알려지지 않은 지름과 같은 데이터 세트의 모든 특이성을 처리할 수 있어야 합니다.

이 파일은 작업 1에서 편집할 예정입니다.
"""

from helpers import cd_to_datetime, datetime_to_str

class NearEarthObject:
    """A near-Earth object (NEO).

        An NEO encapsulates semantic and physical parameters about the object, such
        as its primary designation (required, unique), IAU name (optional), diameter
        in kilometers (optional - sometimes unknown), and whether it's marked as
        potentially hazardous to Earth.

        A `NearEarthObject` also maintains a collection of its close approaches -
        initialized to an empty collection, but eventually populated in the
        `NEODatabase` constructor.
    """
    # TODO: 이 생성자의 인수를 어떻게 변경할 수 있으며, 변경해야 할까요?
    # 변경한 경우, 이 파일의 주석을 업데이트해야 합니다.

    def __init__(self, **info): #info는 가변형 인자
        """Create a new `NearEarthObject`.
        :param info: keyword arguments supplied to the constructor.
        """
        # TODO: Assign information from the arguments passed to the constructor
        # 생성자에 전달된 인수에서 정보를 가져와서
        # 'designation', 'name', 'diameter', 및 'hazardous'라는 속성에 할당합니다.
        # 이러한 값을 적절한 데이터 유형으로 강제 형변환하고 빈 이름은 `None`으로, 지름이 알려지지 않은 경우에는 `float('nan')`으로 처리해야 합니다.
        self.designation = None if info.get('designation', '') == '' else info.get('designation')
        self.name = None if info.get('name', '') == '' else info.get('name')
        self.diameter = float('nan') if info.get('diameter', '') == '' else info.get('diameter')
        self.hazardous = False if info.get('hazardous', '') == '' else info.get('hazardous')
  
        # Create an empty initial collection of linked approaches.
        self.approaches =[]
    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        # TODO: Use self.designation and self.name to build a fullname for this object.
        if self.designation is None or self.designation == "":
            return None
        else:
            return self.designation
    def strHazardous(self):
        if self.hazardous:
            return "is"
        else :
            return "is not"

    def __str__(self):
        """Return `str(self)`."""
    # TODO: 이 객체의 속성을 사용하여 사람이 읽기 쉬운 문자열 표현을 반환합니다.
    # 프로젝트 지침에는 한 가지 가능성이 포함되어 있습니다. 고급 문자열 형식화의 예는 __repr__ 메서드를 참조하세요.

    
        return f"NEO {self.fullname} ({self.name}) has a diameter of {self.diameter:.3f} km and {self.strHazardous} potentially hazardous."



    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, " \
               f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"

    def serialize(self):
        neo_dic = {
            "designation" : self.designation,
            "name" : self.name,
            "diameter_km" : self.diameter,
            "potentially_hazardous" : self.hazardous
        }
        return neo_dic

class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initally, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """
    # TODO: 이 생성자의 인수를 어떻게 변경할 수 있으며, 변경해야 할까요?
    # 변경한 경우, 이 파일의 주석을 업데이트해야 합니다.
    def __init__(self, **info):
        """Create a new `CloseApproach`
        :param info: keyword arguments supplied to the constructor.
        """
        # TODO: 생성자로 전달된 인수에서 얻은 정보를 `_designation`, `time`, `distance`, 그리고 `velocity`라는 속성에 할당하세요. 
        # 이러한 값들을 적절한 데이터 유형으로 변환하고 예외 상황을 처리해야 합니다.
        # `cd_to_datetime` 함수가 유용할 것입니다.

        self._designation = None if info.get('_designation', '') == '' else info.get('_designation')
        self.time = info.get('time', '')  # TODO: Use the cd_to_datetime function for this attribute. cd_to_datetime이용해 문제 풀이
        self.distance = float('nan') if info.get('distance', '') == '' else info.get('distance')
        self.velocity = float('nan') if float(info.get('velocity', '')) == '' else float(info.get('velocity'))
        self.time = cd_to_datetime(self.time)

        # 참조된 NEO(근지 천체)를 위한 속성을 생성합니다. 원래 None이었습니다.
        self.neo = info.get('neo',None)

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        # TODO: 이 객체의 `.time` 속성과 `datetime_to_str` 함수를 사용하여 접근 시간의 형식화된 표현을 작성하세요.
        # TODO: self.designation 및 self.name을 사용하여 이 객체에 대한 전체 이름을 작성하세요.
        return datetime_to_str(self.time)
    def __str__(self):
        """Return `str(self)`."""
    # TODO: 이 객체의 속성을 사용하여 사람이 읽기 쉬운 문자열 표현을 반환합니다.
    # 프로젝트 지침에는 한 가지 가능성이 포함되어 있습니다. 고급 문자열 형식화의 예는 __repr__ 메서드를 참조하세요.

        return f"On {self.time_str}, '{self.neo.fullname} ({self.neo.name})' approaches Earth at a distance of {self.distance:.2f} au and a velocity of {self.velocity:.2f}km/s."
    def __repr__(self):
        """Return repr(self), a computer-readable string representation of this object."""
        return f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, " f"velocity={self.velocity:.2f}, neo={self.neo!r})"
    def serialize(self):
        Approach_dic = {
            "datetime_utc": datetime_to_str(self.time),
            "distance_au" : self.distance,
            "velocity_km_s" : self.velocity
        }
        return Approach_dic