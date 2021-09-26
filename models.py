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

        :param info: A dictionary of excess keyword arguments supplied to the constructor.

        - pdes: the designation attribute (str), let it be None if not found
        - name: the name attribute (str), let it be None if not found
        - diameter: the diameter attribute (float), let it be float("nan") if not found
        - hazardous: the hazardous atribute (bool, converted at extraction), let it be None if not found
        - approaches: the placeholder for linking the NEO to corresponding approaches at the Database step
        """
        self.designation = info.get("pdes", None)
        self.name = info.get("name", None)
        self.diameter = info.get("diameter", float("nan"))
        self.hazardous = info.get("pha", None)

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        if self.name:
            return f"{self.designation} {self.name}"
        else:
            return f"{self.designation}"

    def __str__(self):
        """Return `str(self)`."""
        diameter = self.diameter if self.diameter != float("nan") else "unknown"
        is_hazardous = "is hazardous" if self.hazardous == "Y" else "is not hazardous"
        if self.diameter:
            return f"A NearEarthObject is called {self.fullname}, \
                with a diameter of {diameter}. It {is_hazardous}."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        diameter = self.diameter if self.diameter != float("nan") else "unknown"
        if self.diameter:
            return (
                f"NearEarthObject(designation={self.designation!r}, name={self.fullname!r}, "
                f"diameter={diameter}, hazardous={self.hazardous!r})"
            )

    def serialize(self):
        """Return a dictionary the key features of a neo to prepare saving to csv / json file."""
        return {
            "designation": self.designation,
            "name": self.name,
            "diameter_km": self.diameter,
            "potentially_hazardous": self.hazardous,
        }


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

    def __init__(self, neo=None, **info):
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.

        - pes: the designation attribute (str), let it be None if not found
        - cd: the time attribute (str, to datetime right after), let it be None if not found
        - distance: the distance attribute (float), let it be float("nan") if not found
        - velocity: the velocity atribute (float), let it be float("nan") if not found
        """
        self._designation = info.get("des", None)
        self.time = info.get("cd", None)
        if self.time:
            self.time = cd_to_datetime(self.time)
        self.distance = info.get("dist", float("nan"))
        self.velocity = info.get("v_rel", float("nan"))

        # Create an attribute for the referenced NEO, originally None.
        self.neo = neo

    @property
    def designation(self):
        """Return the designation as a property."""
        return self._designation

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
        time_cad = self.time_str if self.time else "an unknown time"
        return f"The close approach was observed, as {self.neo.fullname} \
            approaches the Earth at {time_cad}, with the closest distance \
                {self.distance:.2f} au at {self.velocity:.2f} KM per second."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (
            f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, "
            f"velocity={self.velocity:.2f}, neo={self.neo!r})"
        )

    def serialize(self):
        """Return a dictionary the key features of a close approach to prepare saving to csv / json file."""
        return {
            "datetime_utc": datetime_to_str(self.time),
            "distance_au": self.distance,
            "velocity_km_s": self.velocity,
        }
