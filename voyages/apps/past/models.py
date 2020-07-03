from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from voyages.apps.voyage.models import Place, Voyage, VoyageSources

class EnslaverInfoAbstractBase(models.Model):
    principal_alias = models.CharField(max_length=255)

    # Personal info.
    birth_year = models.IntegerField(null=True)
    birth_month = models.IntegerField(null=True)
    birth_day = models.IntegerField(null=True)
    birth_place = models.CharField(max_length=255, null=True)

    death_year = models.IntegerField(null=True)
    death_month = models.IntegerField(null=True)
    death_day = models.IntegerField(null=True)
    death_place = models.CharField(max_length=255, null=True)

    father_name = models.CharField(max_length=255, null=True)
    father_occupation = models.CharField(max_length=255, null=True)
    mother_name = models.CharField(max_length=255, null=True)
    
    first_spouse_name = models.CharField(max_length=255, null=True)
    first_marriage_date = models.CharField(max_length=12, null=True)
    second_spouse_name = models.CharField(max_length=255, null=True)
    second_marriage_date = models.CharField(max_length=12, null=True)

    probate_date = models.CharField(max_length=12, null=True)
    will_value_pounds = models.CharField(max_length=12, null=True)
    will_value_dollars = models.CharField(max_length=12, null=True)
    will_court = models.CharField(max_length=12, null=True)

    class Meta:
        abstract = True

class EnslaverIdentity(EnslaverInfoAbstractBase):
    class Meta:
        verbose_name = 'Enslaver unique identity and personal info'

class EnslaverIdentitySourceConnection(models.Model):
    identity = models.ForeignKey(EnslaverIdentity, on_delete=models.CASCADE)
    # Sources are shared with Voyages.
    source = models.ForeignKey(VoyageSources, related_name="+", null=False)
    source_order = models.IntegerField()
    text_ref = models.CharField(max_length=255, null=False, blank=True)

class EnslaverAlias(models.Model):
    """
    An alias represents a name appearing in a record that is mapped to
    a consolidated identity. The same individual may appear in multiple
    records under different names (aliases).
    """
    identity = models.ForeignKey(EnslaverIdentity, on_delete=models.CASCADE)
    alias = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Enslaver alias'

class EnslaverMerger(EnslaverInfoAbstractBase):
    """
    Represents a merger of two or more identities.
    We inherit from EnslaverInfoAbstractBase so that all personal fields
    are also contained in the merger.
    """
    comments = models.CharField(max_length=1024)

class EnslaverMergerItem(models.Model):
    """
    Represents a single identity that is part of a merger.
    """
    merger = models.ForeignKey('EnslaverMerger', null=False, on_delete=models.CASCADE)
    # We do not use a foreign key to the identity since if the merger
    # is accepted, some/all of the records may be deleted and the keys
    # would either be invalid or set to null.
    enslaver_identity_id = models.IntegerField(null=False)

class EnslaverVoyageConnection(models.Model):
    """
    Associates an enslaver with a voyage at some particular role.
    """

    class Role:
        CAPTAIN = 1
        OWNER = 2
        BUYER = 3
        SELLER = 4

    enslaver_alias = models.ForeignKey('EnslaverAlias', null=False, on_delete=models.CASCADE)
    voyage = models.ForeignKey('voyage.Voyage', null=False, on_delete=models.CASCADE)
    role = models.IntegerField(null=False)
    # There might be multiple persons with the same role for the same voyage
    # and they can be ordered (ranked) using the following field.
    order = models.IntegerField(null=True)
    # NOTE: we will have to substitute VoyageShipOwner and VoyageCaptain
    # models/tables by this entity.

class NamedModelAbstractBase(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        abstract = True

class ModernCountry(NamedModelAbstractBase):
    pass

class RegisterCountry(NamedModelAbstractBase):
    pass

class LanguageGroup(NamedModelAbstractBase):
    longitude = models.DecimalField("Longitude of point",
                                     max_digits=10, decimal_places=7,
                                     null=False)
    latitude = models.DecimalField("Latitude of point",
                                     max_digits=10, decimal_places=7,
                                     null=False)
    modern_country = models.ForeignKey(ModernCountry, null=False, related_name='language_groups')

class AltLanguageGroupName(NamedModelAbstractBase):
    language_group = models.ForeignKey(LanguageGroup, null=False, related_name='alt_names')

class Ethnicity(NamedModelAbstractBase):
    language_group = models.ForeignKey(LanguageGroup, null=False, related_name='ethnicities')

class AltEthnicityName(NamedModelAbstractBase):
    ethnicity = models.ForeignKey(Ethnicity, null=False, related_name='alt_names')

# TODO: this model will replace resources.AfricanName
class Enslaved(models.Model):
    """
    Enslaved person.
    """
    enslaved_id = models.IntegerField(primary_key=True)

    documented_name = models.CharField(max_length=25, blank=True)
    name_first = models.CharField(max_length=25, null=True, blank=True)
    name_second = models.CharField(max_length=25, null=True, blank=True)
    name_third = models.CharField(max_length=25, null=True, blank=True)

    # Personal data
    age = models.IntegerField(null=True)
    # For some records, the exact age may be unknown and only
    # an adult/child status is determined.
    is_adult = models.NullBooleanField(null=True)
    gender = models.IntegerField(null=True)
    height = models.FloatField(null=True, verbose_name="Height in inches")

    # The ethnicity, language and country could be null.
    # The possibility of including 'Unknown' values in the
    # reference tables and using them instead of null was
    # proposed and discarded.
    ethnicity = models.ForeignKey(Ethnicity, null=True)
    language_group = models.ForeignKey(LanguageGroup, null=True)
    register_country = models.ForeignKey(RegisterCountry, null=True)

    post_disembark_location = models.ForeignKey(Place, null=True)

    voyage = models.ForeignKey(Voyage, null=False)
    sources = models.ManyToManyField \
        (VoyageSources, through='EnslavedSourceConnection', related_name='+')

class EnslavedSourceConnection(models.Model):
    enslaved = models.ForeignKey(Enslaved, on_delete=models.CASCADE)
    # Sources are shared with Voyages.
    source = models.ForeignKey(VoyageSources, on_delete=models.CASCADE, related_name='+', null=False)
    source_order = models.IntegerField()
    text_ref = models.CharField(max_length=255, null=False, blank=True)

class EnslavedContribution(models.Model):
    enslaved = models.ForeignKey(Enslaved, on_delete=models.CASCADE)
    contributor = models.ForeignKey(User, null=True, related_name='+')
    date = models.DateField(auto_now_add=True)
    notes = models.CharField(max_length=255, null=True, blank=True)
    
class EnslavedContributionNameEntry(models.Model):
    contribution = models.ForeignKey(EnslavedContribution, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False, blank=False)
    order = models.IntegerField()
    notes = models.CharField(max_length=255, null=True, blank=True)

class EnslavedContributionLanguageEntry(models.Model):
    contribution = models.ForeignKey(EnslavedContribution, on_delete=models.CASCADE)
    ethnicity = models.ForeignKey(Ethnicity, null=True)
    language_group = models.ForeignKey(LanguageGroup, null=True)
    order = models.IntegerField()
    notes = models.CharField(max_length=255, null=True, blank=True)

class EnslavedSearch:
    """
    Search parameters for enslaved persons.
    """

    def __init__(self, searched_name=None, exact_name_search=False, age_gender=None, \
            age_range=None, year_range=None, embarkation_ports=None, disembarkation_ports=None, \
            post_disembark_location=None, language_groups=None, modern_country=None, 
            ship_name=None, voyage_id=None, source=None, order_by=None):
        """
        Search the Enslaved database. If a parameter is set to None, it will not
        be included in the search.
        @param: searched_name A name string to be searched
        @param: exact_name_search Boolean indicating whether the search is exact or fuzzy
        @param: age_gender A list of pairs (bool is_adult, male = 1/female = 2) with
                all combinations filtered.
        @param: age_range A pair (a, b) where a is the min and b is maximum age
        @param: is_adult Whether the search is for adults or children only
        @param: year_range A pair (a, b) where a is the min voyage year and b the max
        @param: embarkation_ports A list of port ids where the enslaved embarked
        @param: disembarkation_ports A list of port ids where the enslaved disembarked
        @param: post_disembark_location A list of place ids where the enslaved was located after disembarkation
        @param: language_groups A list of language groups ids for the enslaved
        @param: modern_country A list of country ids
        @param: ship_name The ship name that the enslaved embarked
        @param: voyage_id A pair (a, b) where the a <= voyage_id <= b
        @param: source A text fragment that should match Source's text_ref or full_ref
        @param: order_by TODO: Spec/impl.
        """
        self.searched_name = searched_name
        self.exact_name_search = exact_name_search
        self.age_gender = age_gender
        self.age_range = age_range
        self.year_range = year_range
        self.embarkation_ports = embarkation_ports
        self.disembarkation_ports = disembarkation_ports
        self.post_disembark_location = post_disembark_location
        self.language_groups = language_groups
        self.modern_country = modern_country
        self.ship_name = ship_name
        self.voyage_id = voyage_id
        self.source = source

    def execute(self):
        """
        Execute the search. If we require fuzzy name search, then this is done
        outside of the database on our special search data structure and then
        filter the ids on the db query.
        """
        q = Enslaved.objects \
            .select_related('ethnicity') \
            .select_related('language_group') \
            .select_related('language_group__modern_country') \
            .select_related('register_country') \
            .all()
        ranking = None
        if self.searched_name and len(self.searched_name):
            if self.exact_name_search:
                q = q.filter(Q(documented_name=self.searched_name) | Q(name_first=self.searched_name) | \
                    Q(name_second=self.searched_name) | Q(name_third=self.searched_name))
            else:
                from name_search import NameSearchCache
                # Perform a fuzzy search on our cached names.
                NameSearchCache.load()
                fuzzy_ids = NameSearchCache.search(self.searched_name)
                ranking = {x[1]: x[0] for x in enumerate(fuzzy_ids)}
                q = q.filter(pk__in=fuzzy_ids)
        if self.age_gender:
            conditions = [Q(is_adult=a, gender=g) for (a, g) in self.age_gender]
            q = q.filter(reduce(operator.or_, conditions))
        if self.age_range:
            q = q.filter(age__range=self.age_range)
        if self.modern_country:
            q = q.filter(modern_country__pk__in=self.modern_country)
        if self.post_disembark_location:
            q = q.filter(post_disembark_location__pk__in=self.post_disembark_location)
        if self.source:
            q = q.filter(Q(sources__text_ref__contains=self.source) | Q(sources__source__full_ref__contains=self.source))
        if self.voyage_id:
            q = q.filter(voyage__pk__range=self.voyage_id)
        if self.year_range:
            # Search on YEARAM field.
            q = q.filter(voyage__voyage_dates__imp_arrival_at_port_of_dis__range=self.year_range)
        if self.embarkation_ports:
            # Search on MJBYPTIMP field.
            q = q.filter(voyage__voyage_itinerary__imp_principal_place_of_slave_purchase__pk__in=self.embarkation_ports)
        if self.disembarkation_ports:
            # Search on MJSLPTIMP field.
            q = q.filter(voyage__voyage_itinerary__imp_principal_port_slave_dis__pk__in=self.disembarkation_ports)
        if self.language_groups:
            q = q.filter(language_group__pk__in=self.language_groups)
        if self.ship_name:
            q = q.filter(voyage__voyage_ship__ship_name__icontains=self.ship_name)
        if self.source:
            q = q.filter()
        return q, ranking