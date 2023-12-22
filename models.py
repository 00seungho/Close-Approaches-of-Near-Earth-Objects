"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from helpers import cd_to_datetime, datetime_to_str

class NearEarthObject:
    """근지 행성 개체 (NEO).
    NEO는 주요 지정 (필수, 고유), IAU 이름 (선택 사항), 킬로미터 단위의 지름 (선택 사항 - 때로는 알려지지 않음) 
    및 지구에 잠재적으로 위험한지 여부와 같은 객체에 관한 의미론적 및 물리적 매개 변수를 캡슐화합니다.
    "NearEarthObject"는 또한 근접 접근의 컬렉션을 유지합니다. 초기화는 비어 있는 컬렉션입니다만, "NEODatabase" 생성자에서 최종적으로 채워집니다.
    """
    # TODO: How can you, and should you, change the arguments to this constructor?
    # If you make changes, be sure to update the comments in this file.
    def __init__(self, **info): #info는 가변형 인자
        """새로운 `NearEarthObject` 생성.

        :param info: 생성자에 제공된 초과 키워드 인수의 딕셔너리.
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
        # TODO: Use this object's attributes to return a human-readable string representation.
        # The project instructions include one possibility. Peek at the __repr__
        # method for examples of advanced string formatting.
    
        return f"NEO {self.fullname} ({self.name}) has a diameter of {self.diameter:.3f} km and {self.strHazardous} potentially hazardous."



    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, " \
               f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """
    # TODO: How can you, and should you, change the arguments to this constructor?
    # If you make changes, be sure to update the comments in this file.
    def __init__(self, **info):
        """Create a new `CloseApproach`.3
        

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        # TODO: 생성자로 전달된 인수에서 얻은 정보를 `_designation`, `time`, `distance`, 그리고 `velocity`라는 속성에 할당하세요. 
        # 이러한 값들을 적절한 데이터 유형으로 변환하고 예외 상황을 처리해야 합니다.
        # `cd_to_datetime` 함수가 유용할 것입니다.

        self._designation = None if info.get('_designation', '') == '' else info.get('_designation')
        self.time = info.get('time', '')  # TODO: Use the cd_to_datetime function for this attribute. cd_to_datetime이용해 문제 풀이
        self.distance = float('nan') if info.get('distance', '') == '' else info.get('distance')
        self.velocity = float('nan') if info.get('velocity', '') == '' else info.get('velocity')
        self.time = cd_to_datetime(self.time)

        # 참조된 NEO(근지 천체)를 위한 속성을 생성합니다. 원래 None이었습니다.
        self.neo = info.get('neo',None)

    @property
    def time_str(self):
        """이 'CloseApproach'의 접근 시간에 대한 형식화된 표현을 반환합니다.
        `self.time`의 값은 Python `datetime` 객체여야 합니다. `datetime` 객체는 문자열 표현을 가지고 있지만, 기본 표현에는 입력 데이터 세트에 존재하지 않는 소수점 이하 숫자도 포함되어 있습니다.
        `datetime_to_str` 메서드는 `datetime` 객체를 사람이 읽을 수 있는 표현 및 CSV 및 JSON 파일 직렬화에 사용할 수 있는 형식화된 문자열로 변환합니다.
        """
        # TODO: 이 객체의 `.time` 속성과 `datetime_to_str` 함수를 사용하여 접근 시간의 형식화된 표현을 작성하세요.
        # TODO: self.designation 및 self.name을 사용하여 이 객체에 대한 전체 이름을 작성하세요.
        return datetime_to_str(self.time)
    def __str__(self):
        """Return `str(self)`."""
        # TODO: Use this object's attributes to return a human-readable string representation.
        # The project instructions include one possibility. Peek at the __repr__
        # method for examples of advanced string formatting.
        return f"On {self.time_str}, '{self.neo.fullname} ({self.neo.name})' approaches Earth at a distance of {self.distance:.2f} au and a velocity of {self.velocity:.2f}km/s."
    def __repr__(self):
        """Return repr(self), a computer-readable string representation of this object."""
        return f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, " f"velocity={self.velocity:.2f}, neo={self.neo!r})"
