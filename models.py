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
    def __init__(self, **info):
        """Create a new `NearEarthObject`.
        :param info: keyword arguments supplied to the constructor.
        """
        self.designation = None if info.get('designation', '') == '' else info.get('designation')
        self.name = None if info.get('name', '') == '' else info.get('name')
        self.diameter = float('nan') if info.get('diameter', '') == '' else info.get('diameter')
        self.hazardous = False if info.get('hazardous', '') == '' else info.get('hazardous')
  
        # Create an empty initial collection of linked approaches.
        self.approaches =[]
    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        if self.designation is None or self.designation == "":
            return None
        else:
            return self.designation
    def strHazardous(self):
        """Return Hazardous Convert to a sentence that will fit into the __str__"""
        if self.hazardous:
            return "is"
        else :
            return "is not"

    def __str__(self):
        """Return `str(self)`."""
        return f"NEO {self.fullname} ({self.name}) has a diameter of {self.diameter:.3f} km and {self.strHazardous} potentially hazardous."



    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, " \
               f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"

    def serialize(self):
        """Return serialized neo object"""
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
    def __init__(self, **info):
        """Create a new `CloseApproach`
        :param info: keyword arguments supplied to the constructor.
        """
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
        return datetime_to_str(self.time)
    def __str__(self):
        """Return `str(self)`."""

        return f"On {self.time_str}, '{self.neo.fullname} ({self.neo.name})' approaches Earth at a distance of {self.distance:.2f} au and a velocity of {self.velocity:.2f}km/s."
    def __repr__(self):
        """Return repr(self), a computer-readable string representation of this object."""
        return f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, " f"velocity={self.velocity:.2f}, neo={self.neo!r})"
    def serialize(self):
        """Return serialized CloseApproach object"""
        Approach_dic = {
            "datetime_utc": datetime_to_str(self.time),
            "distance_au" : self.distance,
            "velocity_km_s" : self.velocity
        }
        return Approach_dic