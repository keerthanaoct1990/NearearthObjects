"""A database encapsulating collections of near-Earth objects and their close approaches.

A `NEODatabase` holds an interconnected data set of NEOs and close approaches.
It provides methods to fetch an NEO by primary designation or by name, as well
as a method to query the set of close approaches that match a collection of
user-specified criteria.

Under normal circumstances, the main module creates one NEODatabase from the
data on NEOs and close approaches extracted by `extract.load_neos` and
`extract.load_approaches`.
"""

import math


class NEODatabase:
    """A database of near-Earth objects and their close approaches.

    A `NEODatabase` contains a collection of NEOs and a collection of close
    approaches. It additionally maintains a few auxiliary data structures to
    help fetch NEOs by primary designation or by name and to help speed up
    querying for close approaches that match criteria.
    """

    def __init__(self, neos, approaches):
        """Create a new `NEODatabase`.

        :param neos: A collection of `NearEarthObject`s.
        :param approaches: A collection of `CloseApproach`es.
        """
        self._neos = neos
        self._approaches = approaches

        self.neo_with_designation = {}
        self.neo_with_name = {}

        for neo in self._neos:
            self.neo_with_designation[neo.designation] = neo
            # Not every NEO got a name.
            if neo.name:
                self.neo_with_name[neo.name] = neo

        for approach in self._approaches:
            neo = self.neo_with_designation[approach._designation]
            neo.approaches.append(approach)



# Get neo by primary designation
    def get_neo_by_designation(self, designation):
        """Find and return an NEO by its primary designation.

        If no match is found, return `None` instead.

        Each NEO in the data set has a unique primary designation, as a string.

        The matching is exact - check for spelling and capitalization if no match is found.

        :param designation: The primary designation of the NEO to search for.
        :return: The `NearEarthObject` with the desired primary designation, or `None`.
        """
        return self.neo_with_designation.get(designation)


    #  Fetch an NEO by its name.
    def get_neo_by_name(self, name):
        """Find and return an NEO by its name.

        If no match is found, return `None` instead.

        Not every NEO in the data set has a name. No NEOs are associated with
        the empty string nor with the `None` singleton.

        The matching is exact - check for spelling and capitalization if no match is found.

        :param name: The name, as a string, of the NEO to search for.
        :return: The `NearEarthObject` with the desired name, or `None`.
        """
        return self.neo_with_name.get(name)






    def query(self, filters=()):
        """Query close approaches to generate those that match a collection of filters.

        This generates a stream of `CloseApproach` objects that match all of the
        provided filters.If no arguments are provided, generate all known close approaches.

        The `CloseApproach` objects are generated in internal order, which isn't
        guaranteed to be sorted meaningfully, although is often sorted by time.

        :param filters: A collection of filters capturing user-specified criteria.
        :return: A stream of matching `CloseApproach` objects.
        """
        none_count = 0
        min_dist = filters['distance_min']
        max_dist = filters['distance_max']
        min_velocity = filters['velocity_min']
        max_velocity = filters['velocity_max']
        min_dia = filters['diameter_min']
        max_dia = filters['diameter_max']
        for value in filters.values():
            if value is None:
                none_count += 1
        if none_count != 10:
            for each_approach in self._approaches:

                apply_filters = False

                if filters['date']:  #filter based on date
                    app_date = each_approach.time.date()
                    if filters['date'] == app_date:
                        apply_filters = True
                    else:
                        apply_filters = False
                        continue

                app_date_range = each_approach.time.date()
                if filters['start_date'] and filters['end_date']:  #filter based on date range
                    if filters['start_date'] <= app_date_range <= filters['end_date']:
                        apply_filters = True
                    else:
                        apply_filters = False
                        continue

                elif filters['start_date']:
                    if filters['start_date'] <= app_date_range:
                        apply_filters = True
                    else:
                        apply_filters = False
                        continue

                elif filters['end_date']:
                    if app_date_range <= filters['end_date']:
                        apply_filters = True
                    else:
                        apply_filters = False
                        continue


        #------------------------------------------------------------------------------------------------------------
                if min_dist and max_dist:  #filter based on min and max distance
                    if float(min_dist) <= each_approach.distance <= float(max_dist):
                        apply_filters = True
                    else:
                        apply_filters = False
                        continue

                elif min_dist:    #filter based on min distance
                    if each_approach.distance >= float(min_dist):
                        apply_filters = True
                    else:
                        apply_filters = False
                        continue

                elif max_dist:     #filter based on max distance
                    if each_approach.distance <= float(max_dist):
                        apply_filters = True
                    else:
                        apply_filters = False
                        continue
#---------------------------------------------------------------------------------------------------------
                if min_velocity and max_velocity:
                    if float(min_velocity) <= each_approach.velocity <= float(max_velocity):
                        apply_filters = True
                    else:
                        apply_filters = False
                        continue

                elif min_velocity:
                    if each_approach.velocity >= float(min_velocity):
                        apply_filters = True
                    else:
                        apply_filters = False
                        continue

                elif max_velocity:
                    if each_approach.velocity <= float(max_velocity):
                        apply_filters = True
                    else:
                        apply_filters = False
                        continue
#-------------------------------------------------------------------------------------------------------------------
                if min_dia and max_dia:
                    if math.isnan(each_approach.neo.diameter):
                        continue
                    if float(min_dia) <= each_approach.neo.diameter <= float(max_dia):
                        apply_filters = True
                    else:
                        apply_filters = False
                        continue

                elif min_dia:
                    if math.isnan(each_approach.neo.diameter):
                        continue
                    if each_approach.neo.diameter >= float(min_dia):
                        apply_filters = True
                    else:
                        apply_filters = False
                        continue

                elif max_dia:
                    if math.isnan(each_approach.neo.diameter):
                        continue
                    if each_approach.neo.diameter <= float(max_dia):
                        apply_filters = True
                    else:
                        apply_filters = False
                        continue
    #--------------------------------------------------------------------------------------------------------------
                if filters['hazardous'] is not None:
                    if filters['hazardous'] == each_approach.neo.hazardous:
                        apply_filters = True
                    else:
                        apply_filters = False
                        continue

                if apply_filters:
                    yield each_approach


        else:
            for each_approach in self._approaches:
                yield each_approach
