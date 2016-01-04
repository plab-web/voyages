# -*- coding: utf-8 -*-
# List of basic variables
from django.utils.datastructures import SortedDict
import models
import lxml.html
from django.db.models import Max, Min
import re
from datetime import date
from django.utils.translation import ugettext_lazy as _

session_expire_minutes = 60

list_imputed_nationality_values = ['Spain / Uruguay', 'Portugal / Brazil', 'Great Britain',
                                   'Netherlands', 'U.S.A.', 'France', 'Denmark / Baltic',
                                   'Other (specify in note)']

list_months = [('01', 'Jan'), ('02', 'Feb'), ('03', 'Mar'), ('04', 'Apr'), ('05', 'May'), ('06', 'Jun'),
               ('07', 'Jul'), ('08', 'Aug'), ('09', 'Sep'), ('10', 'Oct'), ('11', 'Nov'), ('12', 'Dec')]

def structure_places(place_list):
    """
    Takes a list of places and then returns a tree of the places structured by region and broad region.
    Returns a dictionary(key=broad_region, value=dictionary(key=region, value=list of places))
    """
    # Dict keyed by region, value is a list of places
    # Distinct for foreign key returns a list (sort of) of tuples with the django id of the place.
    # I think it will only ever have one place in each tuple, though it would probably be best to just iterate through the tuple
    region_list = {}
    for tup in place_list:
        for idx in tup:
            if idx:
                place = models.Place.objects.get(id=idx)
                reg = place.region
                if reg not in region_list:
                    region_list[reg] = []
                region_list[reg].append(place)
    broad_region_list = {}
    for region, list_of_places in region_list.items():
        broad_reg = region.broad_region
        if broad_reg not in broad_region_list:
            broad_region_list[broad_reg] = {}
        broad_region_list[broad_reg][region] = list_of_places
    return broad_region_list

def structure_places_all(place_list):
    """
    Takes a list of places and then returns a tree of the places structured by region and broad region.
    Returns a dictionary(key=broad_region, value=dictionary(key=region, value=list of places))
    """
    # Dict keyed by region, value is a list of places
    # Distinct for foreign key returns a list (sort of) of tuples with the django id of the place.
    # I think it will only ever have one place in each tuple, though it would probably be best to just iterate through the tuple
    region_list = {}
    for place in place_list:
        reg = place.region
        if reg not in region_list:
            region_list[reg] = []
        region_list[reg].append(place)
    broad_region_list = {}
    for region, list_of_places in region_list.items():
        broad_reg = region.broad_region
        if broad_reg not in broad_region_list:
            broad_region_list[broad_reg] = {}
        broad_region_list[broad_reg][region] = list_of_places
    return broad_region_list

def display_yesno(value, voyageid=None):
    return 'Yes' if value else 'No'

def display_percent(value, voyageid=None):
    return str(round(value*100, 1)) + "%"
def display_sterling_price(value, voyageid=None):
    return "£" + str(round(value, 2))
def display_sterling_price_nopound(value, voyageid=None):
    return str(round(value, 2))
def display_xls_multiple_names(value, voyageid=None):
    return value.replace('<br/>', ';').replace('<br>', ';')
# Returns a list of the short form sources split by semicolons
def display_xls_sources(value, voyageid=None):
    if not value:
        return value
    srcs = []
    for i in value:
        split = i.split('<>')
        if split and len(split) > 0 and split[0] != '':
            srcs.append(split[0])
    return '; '.join(srcs)
def detail_display_sources(value, voyageid=None):
    if not value:
        return value
    srcs = []
    for i in value:
        parts = i.split('<>')
        if len(parts) > 1:
            parts[1] = '<span class="detail-data-rollover"> ' + parts[1] + " </span>\n"
            srcs.append(': '.join(parts))
    return ' <br/>'.join(srcs)
# Converts a text percentage to a decimal between 0 and 1
def mangle_percent(value, voyageid=None):
    return float(str(value).replace('%', '')) / 100.0
def mangle_source(value, voyageid=None):
    return re.sub(r'[,\s]', '', value)
def unmangle_percent(value, voyageid=None):
    if isinstance(value, (str, int, float)):
        return str(round(float(value) * 100, 1)) + "%"
    else:
        return str(value * 100) + "%"
def unmangle_date(value, voyageid=None):
    if isinstance(value, date):
        return unicode(value.month) + u'/' + unicode(value.day) + u'/' + unicode(value.year)
    splitstr = str(value).split(',')
    splitstr.reverse()
    return '/'.join(splitstr)
def unmangle_datem(value, voyageid=None):
    if isinstance(value, date):
        return unicode(value.month) + u'/' + unicode(value.year)
    splitstr = str(value).split(',')
    splitstr.reverse()
    return '/'.join(splitstr)
def unmangle_truncate(value, voyageid=None):
    val = float(value)
    return int(round(val))
def no_mangle(value, voyageid=None):
    return value

# Unmangle methods for select variables, since now the selections are stored as the numeric ids,
# in previous queries it needs to be converted back to the string representing the place.
# This will perform a lot of db queries, so all option tables should probably be stored into a dict on startup/every so often
def unmangle_place(value, voyageid=None):
    if isinstance(value, (list, tuple)):
        return map(unmangle_place, value)
    return unicode(_(models.Place.objects.get(value=int(value)).place))
def unmangle_nationality(value, voyageid=None):
    if isinstance(value, (list, tuple)):
        return map(unmangle_nationality, value)
    return unicode(_(models.Nationality.objects.get(value=int(value)).label))
def unmangle_rig(value, voyageid=None):
    if isinstance(value, (list, tuple)):
        return map(unmangle_rig, value)
    return unicode(models.RigOfVessel.objects.get(value=int(value)).label)
def unmangle_outcome_particular(value, voyageid=None):
    if isinstance(value, (list, tuple)):
        return map(unmangle_outcome_particular, value)
    return unicode(_(models.ParticularOutcome.objects.get(value=int(value)).label))
def unmangle_outcome_slaves(value, voyageid=None):
    if isinstance(value, (list, tuple)):
        return map(unmangle_outcome_slaves, value)
    return unicode(_(models.SlavesOutcome.objects.get(value=int(value)).label))
def unmangle_outcome_owner(value, voyageid=None):
    if isinstance(value, (list, tuple)):
        return map(unmangle_outcome_owner, value)
    return unicode(_(models.OwnerOutcome.objects.get(value=int(value)).label))
def unmangle_outcome_ship(value, voyageid=None):
    if isinstance(value, (list, tuple)):
        return map(unmangle_outcome_ship, value)
    return unicode(_(models.VesselCapturedOutcome.objects.get(value=int(value)).label))
def unmangle_resistance(value, voyageid=None):
    if isinstance(value, (list, tuple)):
        return map(unmangle_resistance, value)
    return unicode(_(models.Resistance.objects.get(value=int(value)).label))

def voyage_by_id(voyageid):
    fil = models.Voyage.objects.filter(voyage_id=voyageid)
    if len(fil) < 1:
        print("ERROR: Could not find voyage " + str(voyageid) + " in database, not displaying date")
        return None
    else:
        return fil[0]

# Take a comma separated date and convert it to a string in the form of (mm/dd/yyyy), and replace unknowns with "?"
def csd_to_str(csd):
    if not csd:
        return ''
    vl = csd.split(',')
    month = '??'
    day = '??'
    year = '????'
    if vl[0] != '': month = str(vl[0]).zfill(2)
    if vl[1] != '': day = str(vl[1]).zfill(2)
    if vl[2] != '': year = str(vl[2]).zfill(4)
    return year + '-' + month + '-' + day

def id_func(value, voyageid=None):
    return value

def trans_adapter(func=id_func):
    def adapted(value, voyageid=None):
        result = func(value, voyageid)
        if isinstance(result, basestring):
            return _(result)
        return result;
    return adapted

def default_prettifier(varname):
    """
    The default prettifier function simply applies the translation for fields
    that contain translatable names such as Port/Place/Region names as well as
    voyage outcomes.
    :param varname: the variable name.
    :return: a function that receives value, voyageid and outputs a converted value.
    """
    if 'idnum' not in varname and ('nation' in varname or
                                   'port' in varname or
                                   'place' in varname or
                                   'region' in varname or
                                   'outcome' in varname or
                                   'resistance' in varname):
        return trans_adapter()
    return id_func

# Returns the date as a string for display using the database fields
def gd_voyage_began(value, voyageid):
    # In production it should fail silently and just give the date based on the solr value
    # For now it should error on no voyageid
    vd = None
    if value.day == 1:
        vyg = voyage_by_id(voyageid)
        if vyg: vd = vyg.voyage_dates.voyage_began
    else:
        vd = ",".join([str(value.month), str(value.day), str(value.year)])
    return csd_to_str(vd)
def gd_slave_purchase_began(value, voyageid):
    vd = None
    if value.day == 1:
        vyg = voyage_by_id(voyageid)
        if vyg: vd = vyg.voyage_dates.slave_purchase_began
    else:
        vd = ",".join([str(value.month), str(value.day), str(value.year)])
    return csd_to_str(vd)
def gd_departed_africa(value, voyageid):
    vd = None
    if value.day == 1:
        vyg = voyage_by_id(voyageid)
        if vyg: vd = vyg.voyage_dates.date_departed_africa
    else:
        vd = ",".join([str(value.month), str(value.day), str(value.year)])
    return csd_to_str(vd)
def gd_first_dis_of_slaves(value, voyageid):
    vd = None
    if value.day == 1:
        vyg = voyage_by_id(voyageid)
        if vyg: vd = vyg.voyage_dates.first_dis_of_slaves
    else:
        vd = ",".join([str(value.month), str(value.day), str(value.year)])
    return csd_to_str(vd)
def gd_departure_last_landing(value, voyageid):
    vd = None
    if value.day == 1:
        vyg = voyage_by_id(voyageid)
        if vyg: vd = vyg.voyage_dates.departure_last_place_of_landing
    else:
        vd = ",".join([str(value.month), str(value.day), str(value.year)])
    return csd_to_str(vd)
def gd_voyage_completed(value, voyageid):
    vd = None
    if value.day == 1:
        vyg = voyage_by_id(voyageid)
        if vyg: vd = vyg.voyage_dates.voyage_completed
    else:
        vd = ",".join([str(value.month), str(value.day), str(value.year)])
    return csd_to_str(vd)

# Run against solr field values when displaying in results table
display_methods = {'var_imputed_percentage_men': display_percent,
                   'var_imputed_percentage_women': display_percent,
                   'var_imputed_percentage_boys': display_percent,
                   'var_imputed_percentage_girls': display_percent,
                   'var_imputed_percentage_male': display_percent,
                   'var_imputed_percentage_child': display_percent,
                   'var_imputed_mortality': display_percent,
                   'var_imputed_sterling_cash': display_sterling_price,
                   'var_tonnage': unmangle_truncate,
                   'var_tonnage_mod': unmangle_truncate,
                   'var_voyage_began': gd_voyage_began,
                   'var_slave_purchase_began': gd_slave_purchase_began,
                   'var_date_departed_africa': gd_departed_africa,
                   'var_first_dis_of_slaves': gd_first_dis_of_slaves,
                   'var_departure_last_place_of_landing': gd_departure_last_landing,
                   'var_voyage_completed': gd_voyage_completed,
                   'var_voyage_in_cd_rom': trans_adapter(display_yesno)
                   }
# Run against solr field values when creating an xls file
display_methods_xls = {'var_imputed_percentage_men': display_percent,
                       'var_imputed_percentage_women': display_percent,
                       'var_imputed_percentage_boys': display_percent,
                       'var_imputed_percentage_girls': display_percent,
                       'var_imputed_percentage_male': display_percent,
                       'var_imputed_percentage_child': display_percent,
                       'var_imputed_mortality': display_percent,
                       'var_imputed_sterling_cash': display_sterling_price_nopound,
                       'var_captain': display_xls_multiple_names,
                       'var_owner': display_xls_multiple_names,
                       'var_sources': display_xls_sources,
                       'var_voyage_began': gd_voyage_began,
                       'var_slave_purchase_began': gd_slave_purchase_began,
                       'var_date_departed_africa': gd_departed_africa,
                       'var_first_dis_of_slaves': gd_first_dis_of_slaves,
                       'var_departure_last_place_of_landing': gd_departure_last_landing,
                       'var_voyage_completed': gd_voyage_completed
                       }
# Run against solr field values when displaying values for a single voyage
#display_methods_details = {'var_sources': detail_display_sources,
#}
# Used to convert a form value to a proper value for searching with
search_mangle_methods = {'var_imputed_percentage_men': mangle_percent,
                         'var_imputed_percentage_women': mangle_percent,
                         'var_imputed_percentage_boys': mangle_percent,
                         'var_imputed_percentage_girls': mangle_percent,
                         'var_imputed_percentage_male': mangle_percent,
                         'var_imputed_percentage_child': mangle_percent,
                         'var_imputed_mortality': mangle_percent,
                         'var_sources': mangle_source}
#Used for display of previous queries
parameter_unmangle_methods = {'var_imputed_percentage_men': unmangle_percent,
                              'var_imputed_percentage_women': unmangle_percent,
                              'var_imputed_percentage_boys': unmangle_percent,
                              'var_imputed_percentage_girls': unmangle_percent,
                              'var_imputed_percentage_male': unmangle_percent,
                              'var_imputed_percentage_child': unmangle_percent,
                              'var_imputed_mortality': unmangle_percent,
                              'var_voyage_began': unmangle_datem,
                              'var_slave_purchase_began': unmangle_datem,
                              'var_date_departed_africa': unmangle_datem,
                              'var_first_dis_of_slaves': unmangle_datem,
                              'var_departure_last_place_of_landing': unmangle_datem,
                              'var_voyage_completed': unmangle_datem,
                              'var_tonnage': unmangle_truncate,
                              'var_tonnage_mod': unmangle_truncate,
                              'var_nationality_idnum': unmangle_nationality,
                              'var_imputed_nationality_idnum': unmangle_nationality,
                              'var_rig_of_vessel_idnum': unmangle_rig,
                              'var_vessel_construction_place_idnum': unmangle_place,
                              'var_registered_place_idnum': unmangle_place,
                              'var_imp_port_voyage_begin_idnum': unmangle_place,
                              'var_first_place_slave_purchase_idnum': unmangle_place,
                              'var_second_place_slave_purchase_idnum': unmangle_place,
                              'var_third_place_slave_purchase_idnum': unmangle_place,
                              'var_imp_principal_place_of_slave_purchase_idnum': unmangle_place,
                              'var_port_of_call_before_atl_crossing_idnum': unmangle_place,
                              'var_first_landing_place_idnum': unmangle_place,
                              'var_second_landing_place_idnum': unmangle_place,
                              'var_third_landing_place_idnum': unmangle_place,
                              'var_imp_principal_port_slave_dis_idnum': unmangle_place,
                              'var_place_voyage_ended_idnum': unmangle_place,
                              'var_outcome_voyage_idnum': unmangle_outcome_particular,
                              'var_outcome_slaves_idnum': unmangle_outcome_slaves,
                              'var_outcome_ship_captured_idnum': unmangle_outcome_ship,
                              'var_outcome_owner_idnum': unmangle_outcome_owner,
                              'var_resistance_idnum': unmangle_resistance,
                              }
# Run against solr field values when displaying values for a single voyage
display_unmangle_methods = {'var_imputed_percentage_men': unmangle_percent,
                            'var_imputed_percentage_women': unmangle_percent,
                            'var_imputed_percentage_boys': unmangle_percent,
                            'var_imputed_percentage_girls': unmangle_percent,
                            'var_imputed_percentage_male': unmangle_percent,
                            'var_imputed_percentage_child': unmangle_percent,
                            'var_imputed_mortality': unmangle_percent,
                            'var_voyage_began': gd_voyage_began,
                            'var_slave_purchase_began': gd_slave_purchase_began,
                            'var_date_departed_africa': gd_departed_africa,
                            'var_first_dis_of_slaves': gd_first_dis_of_slaves,
                            'var_departure_last_place_of_landing': gd_departure_last_landing,
                            'var_voyage_completed': gd_voyage_completed,
                            'var_tonnage': unmangle_truncate,
                            'var_tonnage_mod': unmangle_truncate,
                            'var_sources': detail_display_sources,
                            'var_voyage_in_cd_rom': trans_adapter(display_yesno),
                            'var_nationality': trans_adapter(),
                            'var_imputed_nationality': trans_adapter(),
                            'var_outcome_voyage': trans_adapter(),
                            'var_outcome_slaves': trans_adapter(),
                            'var_outcome_ship_captured': trans_adapter(),
                            'var_outcome_owner': trans_adapter(),
                            }

def graph_percent(ratio):
    return ratio * 100

graph_display_methods = {'var_imputed_percentage_men': graph_percent,
                         'var_imputed_percentage_women': graph_percent,
                         'var_imputed_percentage_boys': graph_percent,
                         'var_imputed_percentage_girls': graph_percent,
                         'var_imputed_percentage_male': graph_percent,
                         'var_imputed_percentage_child': graph_percent,
                         'var_imputed_mortality': graph_percent,}



def formatYear(year, month=0):
    """
    Format the passed year month to a YYYY,MM string
    :param year:
    :param month:
    :return:
    """
    return "%s,%s" % (str(year).zfill(4), str(month).zfill(2))

def calculate_maxmin_years():
    def_first = 1514
    def_last = 1866
    voyage_span_first_year = def_first
    voyage_span_last_year = def_last
    if models.VoyageDates.objects.count() > 1:
        voyage_span_first_year = models.VoyageDates.objects.all().aggregate(Min('imp_voyage_began'))['imp_voyage_began__min'][2:]
        voyage_span_last_year = models.VoyageDates.objects.all().aggregate(Max('imp_voyage_began'))['imp_voyage_began__max'][2:]

    return voyage_span_first_year or def_first, voyage_span_last_year or def_last

sfirst_year, slast_year = calculate_maxmin_years()
mfirst_year = int(sfirst_year)
mlast_year = int(slast_year)


# TODO: convert this to use get_each_from_list
def get_incremented_year_tuples(interval, first_year=mfirst_year, last_year=mlast_year):
    start_year = (int(first_year) - (int(first_year) % int(interval))) + 1
    current_year = start_year
    years = []
    while current_year <= last_year:
        # Range is exclusive of the start, and inclusive of the end, so a search for years 1800 to 1899 will need the range 1799-1899
        years.append([current_year, current_year + interval - 1])
        current_year += interval
    def year_labeler(years):
        if years[0] == years[1]:
            return years[1]
        else:
            return str(years[0]) + '-' + str(years[1])
    return get_each_from_list(years, 'var_imp_arrival_at_port_of_dis__range', year_labeler)

# Returns filter definition (list of tuples of (label_list, query_dict))
def get_each_from_list(lst, qdictkey, lmblbl=lambda x: unicode(x), lmbval=lambda x: x):
    result = []
    for i in lst:
        lbl = lmblbl(i)
        label_list = [(lbl, 1,),]
        val = lmbval(i)
        result.append((label_list, {qdictkey: val},))
    return result

# TODO: Convert calls to this into a call to the get_each_from_list function
def get_each_from_table(table, qdictkey, lmblbl=lambda x: x.label, lmbval=lambda x: x.value):
    result = []
    for i in table.objects.all():
        val = lmblbl(i)
        label_list = [(val, 1,),]
        result.append((label_list, {qdictkey: lmbval(i)}))
    return result

def impute_nat_fun(lst):
    output = []
    for i in lst:
        mods = models.Nationality.objects.filter(value=i)
        if mods.count() > 0 and len(mods) > 0:
            output.append(mods[0])
    return output

imputed_nationality_possibilities = impute_nat_fun([3, 6, 7, 8, 9, 10, 15, 30])

def make_regions_filter(varname):
    qdictkey = varname + '_idnum__exact'
    results = []
    label_list = []
    for broad in models.BroadRegion.objects.all():
        label_list.append((broad.broad_region, broad.region_set.count(),))
        for reg in broad.region_set.all():
            label_list.append((reg.region, 1,))
            results.append((label_list, {qdictkey: reg.value},))
            label_list = []
    return results

def make_places_filter(varname):
    qdictkey = varname + '_idnum__exact'
    results = []
    label_list = []
    for broad in models.BroadRegion.objects.all():
        label_list.append((broad.broad_region, sum(map(lambda x: x.place_set.count(), list(broad.region_set.all()))),))
        for reg in broad.region_set.all():
            label_list.append((reg.region, reg.place_set.count(),))
            for place in reg.place_set.all():
                label_list.append((place.place, 1,))
                # TODO: Change place filter to use numeric identifiers instead of text
                results.append((label_list, {qdictkey: place.value},))
                label_list = []
    return results

def make_regions_col_filter(filter_name, varname):
    qdictkey = varname + '_idnum__exact'
    results = []
    labels = [[], []]
    for broad in models.BroadRegion.objects.all():
        labels[0].append((broad.broad_region, broad.region_set.count(),))
        for reg in broad.region_set.all():
            labels[1].append((reg.region, 1,))
            results.append({qdictkey: reg.value})
    return (filter_name, results, labels,)

def make_places_col_filter(filter_name, varname):
    qdictkey = varname + '_idnum__exact'
    results = []
    labels = [[], [], []]
    for broad in models.BroadRegion.objects.all():
        labels[0].append((broad.broad_region, sum(map(lambda x: x.place_set.count(), list(broad.region_set.all()))),))
        for reg in broad.region_set.all():
            labels[1].append((reg.region, reg.place_set.count(),))
            for place in reg.place_set.all():
                labels[2].append((place.place, 1,))
                results.append({qdictkey: place.value})
    return (filter_name, results, labels,)

def get_each_from_list_col(filter_name, lst, qkey, lmblbl=lambda x: unicode(x), lmbval=lambda x: x):
    uziped = zip(*get_each_from_list(lst, qkey, lmblbl, lmbval))
    if len(uziped) > 1:
        return (filter_name, uziped[1], [map(lambda x: x[0], uziped[0])],)
    else:
        return (filter_name, [], [])

def get_each_from_table_col(filter_name, table, qkey, lmblbl=lambda x: x.label, lmbval=lambda x: x.value):
    uziped = zip(*get_each_from_table(table, qkey, lmblbl))
    if len(uziped) > 1:
        return (filter_name, uziped[1], [map(lambda x: x[0], uziped[0])],)
    else:
        return (filter_name, [], [])


# Defines the options selectable for filtering the rows/columns of the table section
# Each element is a triple with the filter_label, and a list of tuples of the label_list and query_dicts, and a number indicating the number of title columns need to be made
#  the row/column labels list is a list of lists of label tuples, which will typically just be a list of lists of one element. However for port and region filters, there will need to be multiple labels of the broadregion, region, and ports.
#  i.e. they are (filter_label, filter_definition)
table_rows = [(_('Flag*'), get_each_from_list(imputed_nationality_possibilities, 'var_imputed_nationality_idnum__exact', lambda x: x.label, lambda x: x.value), 0,),
              (_('Broad region where voyage began'), get_each_from_table(models.BroadRegion, 'var_imp_broad_region_voyage_begin_idnum__exact', lambda x: x.broad_region, lambda x: x.value), 0,),
              (_('Region where voyage began'), make_regions_filter('var_imp_region_voyage_begin'), 1,),
              (_('Port where voyage began'), make_places_filter('var_imp_port_voyage_begin'), 2,),
              (_('Embarkation Regions'), make_regions_filter('var_imp_principal_region_of_slave_purchase'), 1,),
              (_('Embarkation Ports'), make_places_filter('var_imp_principal_place_of_slave_purchase'), 2,),
              (_('Specific regions of disembarkation'), make_regions_filter('var_imp_principal_region_slave_dis'), 1,),
              (_('Broad regions of disembarkation'), get_each_from_table(models.BroadRegion, 'var_imp_principal_broad_region_disembark_idnum__exact', lambda x: x.broad_region, lambda x: x.value), 0,),
              (_('Disembarkation Ports'), make_places_filter('var_imp_principal_port_slave_dis'), 2,),
              (_('Individual Years'), get_incremented_year_tuples(1), 0,),
              (_('5-year periods'), get_incremented_year_tuples(5), 0,),
              (_('10-year periods'), get_incremented_year_tuples(10), 0,),
              (_('25-year periods'), get_incremented_year_tuples(25), 0,),
              (_('50-year periods'), get_incremented_year_tuples(50), 0,),
              (_('100-year periods'), get_incremented_year_tuples(100), 0,),]
# Column definitions will be a triple of the filter name, the filter definition (list of queries), and the list of column labels
table_columns = [get_each_from_list_col(_('Flag*'), imputed_nationality_possibilities, 'var_imputed_nationality_idnum__exact', lambda x: x.label, lambda x: x.value),
                 get_each_from_table_col(_('Broad region where voyage began'), models.BroadRegion, 'var_imp_broad_region_voyage_begin_idnum__exact', lambda x: x.broad_region, lambda x: x.value),
                 make_regions_col_filter(_('Region where voyage began'), 'var_imp_region_voyage_begin'),
                 make_places_col_filter(_('Port where voyage began'), 'var_imp_port_voyage_begin'),
                 make_regions_col_filter(_('Embarkation Regions'), 'var_imp_principal_region_of_slave_purchase'),
                 make_places_col_filter(_('Embarkation Ports'), 'var_imp_principal_place_of_slave_purchase'),
                 make_regions_col_filter(_('Specific regions of disembarkation'), 'var_imp_principal_region_slave_dis'),
                 get_each_from_table_col(_('Broad regions of disembarkation'), models.BroadRegion, 'var_imp_principal_broad_region_disembark_idnum__exact', lambda x: x.broad_region, lambda x: x.value),
                 make_places_col_filter(_('Disembarkation Ports'), 'var_imp_principal_port_slave_dis'),]
# Creates a function that takes a queryset and returns a summation of the given value with the display prettifier applied
def make_sum_fun(varname):
    prettifier = display_methods.get(varname, no_mangle)
    def sum_fun(queryset, rowset, colset, allset):
        stats = queryset.stats(varname).stats_results()
        if stats and stats[varname]:
            return prettifier(int(stats[varname]['sum']))
        else:
            return prettifier(0)
        #return prettifier(sum([i[varname] for i in list(queryset.values(varname)) if varname in i and i[varname] != None]))
    return sum_fun

def make_sum_nopretty_fun(varname):
    prettifier = graph_display_methods.get(varname, no_mangle)
    def sum_nopretty_fun(queryset, rowset=None, colset=None, allset=None):
        stats = queryset.stats(varname).stats_results()
        if stats and stats[varname]:
            return prettifier(int(stats[varname]['sum']))
        else:
            return prettifier(0)
    return sum_nopretty_fun

#return lambda queryset, rowset, colset, allset: prettifier(sum([i[varname] for i in queryset.values() if varname in i and i[varname] != None]))

def display_average(value):
    if value != None:
        return round(value, 1)
    else:
        return value

def make_avg_fun(varname):
    prettifier = display_methods.get(varname, display_average)
    def avg_fun(queryset, rowset=None, colset=None, allset=None):
        #lst = [i.get_stored_fields()[varname] for i in queryset.all() if varname in i.get_stored_fields() and i.get_stored_fields()[varname] != None]
        stats = queryset.stats(varname).stats_results()
        if stats and stats[varname]:
            return prettifier(stats[varname]['mean'])
        else:
            return None
#        if len(lst) == 0:
#            return None
#        else:
#            return prettifier(sum(lst)/len(lst))
    return avg_fun

def make_avg_nopretty_fun(varname):
    prettifier = graph_display_methods.get(varname, no_mangle)
    def avg_nopretty_fun(queryset, rowset=None, colset=None, allset=None):
        stats = queryset.stats(varname).stats_results()
        if stats and stats[varname]:
            return prettifier(stats[varname]['mean'])
        else:
            return None
    return avg_nopretty_fun

def make_row_tot_percent_fun(varname):
    def row_tot_fun(queryset, rowset, colset, allset):
        if rowset == None:
            if colset == None:
                return display_percent(1)
            else:
                rowset = allset
        rowstats = rowset.stats(varname).stats_results()
        qstats = queryset.stats(varname).stats_results()
        if qstats and qstats[varname]:
            return display_percent(float(qstats[varname]['sum'])/float(rowstats[varname]['sum']))
        else:
            return None
    return row_tot_fun

def make_col_tot_percent_fun(varname):
    def col_tot_fun(queryset, rowset, colset, allset):
        if colset == None:
            if rowset == None:
                return display_percent(1)
            else:
                colset = allset
        colstats = colset.stats(varname).stats_results()
        qstats = queryset.stats(varname).stats_results()
        if qstats and qstats[varname]:
            return display_percent(float(qstats[varname]['sum'])/float(colstats[varname]['sum']))
        else:
            return None
    return col_tot_fun

# Makes a function that counts how many of the voyages have that particular value defined
def make_num_fun(varname):
    def num_fun(queryset, rowset, colset, allset):
        stats = queryset.stats(varname).stats_results()
        if stats and stats[varname]:
            return stats[varname]['count']
        else:
            return 0
    return num_fun
emb_name = 'var_imp_total_num_slaves_purchased'
dis_name = 'var_imp_total_slaves_disembarked'
def sum_emb_dis(queryset, rowset, colset, allset):
    statsemb = queryset.stats(emb_name).stats_results()
    statsdis = queryset.stats(dis_name).stats_results()
    embs = 0
    diss = 0
    if statsemb[emb_name]:
        embs = int(statsemb[emb_name]['sum'])
    if statsdis[dis_name]:
        diss = int(statsdis[dis_name]['sum'])
    return (embs, diss)
#    return (sum([i.get_stored_fields()[emb_name] for i in queryset.all() if emb_name in i.get_stored_fields() and i.get_stored_fields()[emb_name] != None]),
#            sum([i.get_stored_fields()[dis_name] for i in queryset.all() if dis_name in i.get_stored_fields() and i.get_stored_fields()[dis_name] != None]))
def avg_emb_dis(queryset, rowset, colset, allset):
    statsemb = queryset.stats(emb_name).stats_results()
    statsdis = queryset.stats(dis_name).stats_results()
    embs = None
    diss = None
    if statsemb[emb_name]:
        embs = statsemb[emb_name]['mean']
    if statsdis[dis_name]:
        diss = statsdis[dis_name]['mean']
    return (embs, diss)
def num_emb_dis(queryset, rowset, colset, allset):
    statsemb = queryset.stats(emb_name).stats_results()
    statsdis = queryset.stats(dis_name).stats_results()
    embc = 0
    disc = 0
    if statsemb[emb_name]:
        embc = statsemb[emb_name]['count']
    if statsdis[dis_name]:
        disc = statsdis[dis_name]['count']
    return (embc, disc)
#    return (len([None for i in queryset.all() if emb_name in i.get_stored_fields() and i.get_stored_fields()[emb_name] != None]),
#            len([None for i in queryset.all() if dis_name in i.get_stored_fields() and i.get_stored_fields()[dis_name] != None]))

# List of tuples that define a function for a cell value (label, mapping function)
table_functions = [(_('Number of Voyages'), lambda x, y, z, a: x.count(),),
                   (_('Sum of embarked slaves'), make_sum_fun('var_imp_total_num_slaves_purchased'),),
                   (_('Average number of embarked slaves'), make_avg_fun('var_imp_total_num_slaves_purchased'),),
                   (_('Number of voyages - embarked slaves'), make_num_fun('var_imp_total_num_slaves_purchased'),),
                   (_('Percent of embarked slaves (row total)'), make_row_tot_percent_fun('var_imp_total_num_slaves_purchased'),),
                   (_('Percent of embarked slaves (column total)'), make_col_tot_percent_fun('var_imp_total_num_slaves_purchased'),),
                   (_('Sum of disembarked slaves'), make_sum_fun('var_imp_total_slaves_disembarked'),),
                   (_('Average number of disembarked slaves'), make_avg_fun('var_imp_total_slaves_disembarked'),),
                   (_('Number of voyages - disembarked slaves'), make_num_fun('var_imp_total_slaves_disembarked')),
                   (_('Percent of disembarked slaves (row total)'), make_row_tot_percent_fun('var_imp_total_slaves_disembarked'),),
                   (_('Percent of disembarked slaves (column total)'), make_col_tot_percent_fun('var_imp_total_slaves_disembarked'),),
                   (_('Sum of embarked/disembarked slaves'), sum_emb_dis),
                   (_('Average number of embarked/disembarked slaves'), avg_emb_dis),
                   (_('Number of voyages - embarked/disembarked slaves'), num_emb_dis),
                   (_('Average percentage male'), make_avg_fun('var_imputed_percentage_male')),
                   (_('Number of voyages - percentage male'), make_num_fun('var_imputed_percentage_male')),
                   (_('Average percentage children'), make_avg_fun('var_imputed_percentage_child')),
                   (_('Number of voyages - percentage children'), make_num_fun('var_imputed_percentage_child')),
                   (_('Average percentage of slaves embarked who died during voyage'), make_avg_fun('var_imputed_mortality')),
                   (_('Number of voyages - percentage of slaves embarked who died during voyage'), make_num_fun('var_imputed_mortality')),
                   (_('Average middle passage (days)'), make_avg_fun('var_length_middle_passage_days'),),
                   (_('Number of voyages - middle passage (days)'), make_num_fun('var_length_middle_passage_days')),
                   (_('Average standarized tonnage'), make_avg_fun('var_tonnage_mod'),),
                   (_('Number of voyages - standarized tonnage'), make_num_fun('var_tonnage_mod')),
                   (_('Sterling cash price in Jamaica'), make_avg_fun('var_imputed_sterling_cash')),
                   (_('Number of voyages - sterling cash price in Jamaica'), make_num_fun('var_imputed_sterling_cash')),]
# Cell functions that return two values, embarked/disembarked
double_functions = [_('Sum of embarked/disembarked slaves'), _('Average number of embarked/disembarked slaves'), _('Number of voyages - embarked/disembarked slaves')]



# I don't think I should worry about Nones, since I should just not include them in the dataset
def averaging_fun(lst):
    sm = 0
    cnt = 0
    for i in lst:
        if i != None:
            cnt += 1
            sm += i
    if cnt > 0:
        return float(sm) / float(cnt)
    else:
        # Should I return None or 0? Should I just skip the values that have None?
        return None

summing_fun = sum
#def summing_fun(lst):
#    sm = 0
#    for i in lst:
#        if i != None:
#            sm += i
#    return sm

def rate_of_resistance_fun(queryset):
    qcount = queryset.count()
    if qcount <= 0:
        return None
    varname = 'var_resistance'
    # stats does not work with string fields, only numeric fields
    #stats = queryset.stats(varname).stats_results()
    rset = queryset.raw_search(varname + ': [* TO *]')
    rcount = rset.count()
    return (float(rcount)/float(qcount)) * 100

# Graphs

# Takes a searchqueryset and returns a number
# (description, varname, function on varname values)
# I don't think it uses the last function
graphs_y_functions = [(_('Number of voyages'), 'var_voyage_id', len, lambda x: x.count(),),
                      (_('Average voyage length, home port to slaves landing (days)*'), 'var_imp_length_home_to_disembark', averaging_fun, make_avg_nopretty_fun('var_imp_length_home_to_disembark'),),
                      (_('Average middle passage (days)*'), 'var_length_middle_passage_days', averaging_fun, make_avg_nopretty_fun('var_length_middle_passage_days'),),
                      (_('Standardized tonnage*'), 'var_tonnage_mod', averaging_fun, make_avg_nopretty_fun('var_tonnage_mod')),
                      (_('Average crew at voyage outset'), 'var_crew_voyage_outset', averaging_fun, make_avg_nopretty_fun('var_crew_voyage_outset'),),
                      (_('Average crew at first landing of slaves'), 'var_crew_first_landing', averaging_fun, make_avg_nopretty_fun('var_crew_first_landing'),),
                      (_('Total crew at voyage outset'), 'var_crew_voyage_outset', summing_fun, make_sum_nopretty_fun('var_crew_voyage_outset'),),
                      (_('Total crew at first landing of slaves'), 'var_crew_first_landing', summing_fun, make_sum_nopretty_fun('var_crew_first_landing'),),
                      (_('Average number of slaves embarked'), 'var_imp_total_num_slaves_purchased', averaging_fun, make_avg_nopretty_fun('var_imp_total_num_slaves_purchased'),),
                      (_('Average number of slaves disembarked'), 'var_imp_total_slaves_disembarked', averaging_fun, make_avg_nopretty_fun('var_imp_total_slaves_disembarked')),
                      (_('Total number of slaves embarked'), 'var_imp_total_num_slaves_purchased', summing_fun, make_sum_nopretty_fun('var_imp_total_num_slaves_purchased'),),
                      (_('Total number of slaves disembarked'), 'var_imp_total_slaves_disembarked', summing_fun, make_sum_nopretty_fun('var_imp_total_slaves_disembarked'),),
                      (_('Percentage men*'), 'var_imputed_percentage_men', averaging_fun, make_avg_nopretty_fun('var_imputed_percentage_men'),),
                      (_('Percentage women*'), 'var_imputed_percentage_women', averaging_fun, make_avg_nopretty_fun('var_imputed_percentage_women'),),
                      (_('Percentage boys*'), 'var_imputed_percentage_boys', averaging_fun, make_avg_nopretty_fun('var_imputed_percentage_boys'),),
                      (_('Percentage girls*'), 'var_imputed_percentage_girls', averaging_fun, make_avg_nopretty_fun('var_imputed_percentage_girls'),),
                      (_('Percentage children*'), 'var_imputed_percentage_child', averaging_fun, make_avg_nopretty_fun('var_imputed_percentage_child'),),
                      (_('Percentage male*'), 'var_imputed_percentage_male', averaging_fun, make_avg_nopretty_fun('var_imputed_percentage_male'),),
                      (_('Sterling cash price in Jamaica*'), 'var_imputed_sterling_cash', averaging_fun, make_avg_nopretty_fun('var_imputed_sterling_cash'),),
                      (_('Rate of resistance'), 'var_resistance', None, rate_of_resistance_fun),
                      (_('Percentage of slaves embarked who died during voyage*'), 'var_imputed_mortality', averaging_fun, make_avg_nopretty_fun('var_imputed_mortality'),),]


# get dicts for x and y values, then make a dictionary of x values, put y values into a list for each x value
def make_x_line_fun(xvar):
    def x_fun(sqs, ydef):
        yvar = ydef[1]
        # function when going against a list, probably not needed, will be slower and will be needed only if the next if statement falls through
        yfun = ydef[2]
        yqsetfun = ydef[3]
        xstats = sqs.stats(xvar).stats_results()
        dataset = []
        xfilter = xvar + "__exact"
        if xstats and xstats[xvar]:
            xmax = int(xstats[xvar]['max'])
            xmin = int(xstats[xvar]['min'])
            for x in range(xmin, xmax + 1):
                fsqs = sqs.filter(**{xfilter: x})
                yval = yqsetfun(fsqs)
                if yval != None:
                    dataset.append((x, yval))
        dataset = sorted(dataset, key=lambda x: x[0])
        return dataset
    return x_fun

# Takes a searchqueryset and a y function definition (description, varname, reduce function) and returns a dataset (list of tuples) in the form (x,y)
graphs_x_functions = [(_('Year arrived with slaves*'), make_x_line_fun('var_imp_arrival_at_port_of_dis')),
                      (_('Voyage length, home port to slaves landing (days)*'), make_x_line_fun('var_imp_length_home_to_disembark')),
                      (_('Middle passage (days)*'), make_x_line_fun('var_length_middle_passage_days')),
                      (_('Crew at voyage outset'), make_x_line_fun('var_crew_voyage_outset')),
                      (_('Crew at first landing of slaves'), make_x_line_fun('var_crew_first_landing')),
                      (_('Slaves embarked'), make_x_line_fun('var_imp_total_num_slaves_purchased')),
                      (_('Slaves disembarked'), make_x_line_fun('var_imp_total_slaves_disembarked')),]

def get_year_bar_tuples(interval, first_year=mfirst_year, last_year=mlast_year):
    start_year = (int(first_year) - (int(first_year) % int(interval))) + 1
    current_year = start_year
    years = []
    while current_year <= last_year:
        # Range is exclusive of the start, and inclusive of the end, so a search for years 1800 to 1899 will need the range 1799-1899
        years.append([current_year, current_year + interval - 1])
        current_year += interval
    def year_labeler(years):
        if years[0] == years[1]:
            return years[1]
        else:
            return str(years[0]) + '-' + str(years[1])
    result = []
    for i in years:
        result.append((year_labeler(i), {'var_imp_arrival_at_port_of_dis__range': i}))
    return make_x_bar_fun('var_imp_arrival_at_port_of_dis', lst=result)

# Lst is a list of tuples of label, searchfilterdef
# Returns a function that can be run with a searchqueryset and a ydef, and will return a dataset of tuples of x,y
lbllblr = lambda x: x.label
def make_x_bar_fun(varname, table=None, tablelblr=lbllblr, lst=None):
    if table:
        lst = []
        for i in table.objects.all():
            varfilt = varname + '_idnum__exact'
            filt = {varfilt: i.value}
            lbl = tablelblr(i)
            lst.append((lbl, filt))
    def x_fun(sqs, ydef):
        dataset = []
        for lbl,filt in lst:
            fsqs = sqs.filter(**filt)
            yval = ydef[3](fsqs)
            dataset.append((lbl, yval))
        return dataset
    return x_fun


def make_x_bar_month_fun(varname):
    output = []
    for num, mon in list_months:
        varkey = varname + "_month__exact"
        output.append((mon, {varkey: int(num)}))
    return make_x_bar_fun(varname, lst=output)

# Convert a list of nationality objects into a list of tuples of (label, filterdef)
imp_nat_pos_bar = map(lambda x: (x.label, {'var_imputed_nationality_idnum__exact': x.value}), imputed_nationality_possibilities)

placelblr = lambda x: x.place
regionlblr = lambda x: x.region


graphs_bar_x_functions = [(_('Flag*'), make_x_bar_fun(_('var_imputed_nationality'), lst=imp_nat_pos_bar)),
                          (_('Rig'), make_x_bar_fun(_('var_rig_of_vessel'), table=models.RigOfVessel, tablelblr=lbllblr)),
                          (_('Particular outcome of the voyage'), make_x_bar_fun(_('var_outcome_voyage'), table=models.ParticularOutcome, tablelblr=lbllblr)),
                          (_('Outcome for slaves*'), make_x_bar_fun(_('var_outcome_slaves'), table=models.SlavesOutcome, tablelblr=lbllblr)),
                          (_('Outcome for owner*'), make_x_bar_fun(_('var_outcome_owner'), table=models.OwnerOutcome)),
                          (_('Outcome if ship captured*'), make_x_bar_fun(_('var_outcome_ship_captured'), table=models.VesselCapturedOutcome)),
                          (_('African resistance'), make_x_bar_fun(_('var_resistance'), table=models.Resistance)),
                          (_('Place where voyage began*'), make_x_bar_fun(_('var_imp_port_voyage_begin'), table=models.Place, tablelblr=placelblr)),
                          (_('Region where voyage began*'), make_x_bar_fun(_('var_imp_region_voyage_begin'), table=models.Region, tablelblr=regionlblr)),
                          (_('Principal place of slave purchase*'), make_x_bar_fun(_('var_imp_principal_place_of_slave_purchase'), table=models.Place, tablelblr=placelblr)),
                          (_('Principal region of slave purchase*'), make_x_bar_fun(_('var_imp_principal_region_of_slave_purchase'), table=models.Region, tablelblr=regionlblr)),
                          (_('Principal place of slave landing*'), make_x_bar_fun(_('var_imp_principal_port_slave_dis'), table=models.Place, tablelblr=placelblr)),
                          (_('Principal region of slave landing*'), make_x_bar_fun(_('var_imp_principal_region_slave_dis'), table=models.Region, tablelblr=regionlblr)),
                          (_('Broad region of slave landing*'), make_x_bar_fun(_('var_imp_principal_broad_region_disembark'), table=models.BroadRegion, tablelblr=lambda x: x.broad_region)),
                          (_('Place where voyage ended'), make_x_bar_fun(_('var_place_voyage_ended'), table=models.Place, tablelblr=placelblr)),
                          (_('Region where voyage ended'), make_x_bar_fun(_('var_region_voyage_ended'), table=models.Region, tablelblr=regionlblr)),
                          (_('Month voyage began'), make_x_bar_month_fun('var_voyage_began')),
                          (_('Month trade began in Africa'), make_x_bar_month_fun('var_slave_purchase_began')),
                          (_('Month vessel departed Africa'), make_x_bar_month_fun('var_date_departed_africa')),
                          (_('Month vessel arrived with slaves'), make_x_bar_month_fun('var_first_dis_of_slaves')),
                          (_('Month vessel departed for home port'), make_x_bar_month_fun('var_departure_last_place_of_landing')),
                          (_('Month voyage completed'), make_x_bar_month_fun('var_voyage_completed')),
                          (_('Year arrived with slaves (5 year periods)'), get_year_bar_tuples(5)),
                          (_('Year arrived with slaves (10 year periods)'), get_year_bar_tuples(10)),
                          (_('Year arrived with slaves (25 year periods)'), get_year_bar_tuples(25)),]



#print list(models.VoyageShip.objects.values_list('vessel_construction_place').distinct())
#print models.VoyageShip.objects.values('vessel_construction_place').distinct()

#all_place_list = structure_places_all(models.Place.objects.all())

additional_var_dict = [
    {'var_name': 'var_imp_principal_broad_region_disembark_idnum',
     'var_type': 'numeric'},
    {'var_name': 'var_imp_broad_region_voyage_begin_idnum',
     'var_type': 'numeric'},
    {'var_name': 'var_imputed_nationality_idnum',
     'var_type': 'numeric'}]

var_dict = [
    # Ship, Nation, Owners
    {'var_name': 'var_voyage_id',
     'spss_name': 'voyageid',
     'var_full_name': 'Voyage identification number',
     'var_type': 'numeric',
     'var_category': 'Ship, nation, owners',
     "is_estimate": False,
     "is_basic": True,
     "is_general": True},
    {'var_name': 'var_voyage_in_cd_rom',
     'spss_name': 'evgreen',
     'var_full_name': 'Voyage in 1999 CD-ROM',
     'var_type': 'boolean',
     'var_category': 'Ship, nation, owners',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True},
    {'var_name': 'var_ship_name',
     'spss_name': 'shipname',
     'var_full_name': 'Vessel name',
     'var_type': 'plain_text',
     'var_category': 'Ship, nation, owners',
     "is_estimate": False,
     "is_basic": True,
     "is_general": True},
    {'var_name': 'var_nationality',
     'spss_name': 'national',
     'var_full_name': 'Flag',
     'var_type': 'select',
     'var_category': 'Ship, nation, owners',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True},
    {'var_name': 'var_imputed_nationality',
     'spss_name': 'natinimp',
     'var_full_name': 'Flag' + "*",
     'var_type': 'select',
     'var_category': 'Ship, nation, owners',
     "is_estimate": True,
     "is_basic": True,
     "is_general": True,
     "note" : "Flag regrouped into seven major national carriers"},
    {'var_name': 'var_vessel_construction_place',
     'spss_name': 'placcons',
     'var_full_name': 'Place constructed',
     'var_type': 'select_three_layers',
     'var_category': 'Ship, nation, owners',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True,
     'choices': structure_places(models.VoyageShip.objects.values_list('vessel_construction_place').distinct())},
#     'choices': all_place_list},
    {'var_name': 'var_year_of_construction',
     'spss_name': 'yrcons',
     'var_full_name': 'Year constructed',
     'var_type': 'numeric',
     'var_category': 'Ship, nation, owners',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True},
    {'var_name': 'var_registered_place',
     'spss_name': 'placreg',
     'var_full_name': 'Place registered',
     'var_type': 'select_three_layers',
     'var_category': 'Ship, nation, owners',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True,
     'choices': structure_places(models.VoyageShip.objects.values_list('registered_place').distinct())},
#     'choices': all_place_list},
    {'var_name': 'var_registered_year',
     'spss_name': 'yrreg',
     'var_full_name': 'Year registered',
     'var_type': 'numeric',
     'var_category': 'Ship, nation, owners',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True},
    {'var_name': 'var_rig_of_vessel',
     'spss_name': 'rig',
     'var_full_name': 'Rig',
     'var_type': 'select',
     'var_category': 'Ship, nation, owners',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True},
    {'var_name': 'var_tonnage',
     'spss_name': 'tonnage',
     'var_full_name': 'Tonnage',
     'var_type': 'numeric',
     'var_category': 'Ship, nation, owners',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True},
    {'var_name': 'var_tonnage_mod',
     'spss_name': 'tonmod',
     'var_full_name': 'Standardized tonnage*',
     'var_type': 'numeric',
     'var_category': 'Ship, nation, owners',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True,
     "note": "Converted to pre-1786 British registered tons"},
    {'var_name': 'var_guns_mounted',
     'spss_name': 'guns',
     'var_full_name': 'Guns mounted',
     'var_type': 'numeric',
     'var_category': 'Ship, nation, owners',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True},
    {'var_name': 'var_owner',
     'spss_name': 'owner',
     'var_full_name': 'Vessel owners',
     'var_type': 'plain_text',
     'var_category': 'Ship, nation, owners',
     "is_estimate": False,
     "is_basic": True,
     "is_general": True},

    # Voyage outcome
    {'var_name': 'var_outcome_voyage',
     'spss_name': 'fate',
     'var_full_name': 'Particular outcome of voyage',
     'var_type': 'select',
     'var_category': 'Voyage Outcome',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True},
    {'var_name': 'var_outcome_slaves',
     'spss_name': 'fate2',
     'var_full_name': 'Outcome of voyage for slaves*',
     'var_type': 'select',
     'var_category': 'Voyage Outcome',
     "is_estimate": False,
     "is_basic": True,
     "is_general": True,
     "note": "Derived from particular outcome"},
    {'var_name': 'var_outcome_ship_captured',
     'spss_name': 'fate3',
     'var_full_name': 'Outcome of voyage if ship captured*',
     'var_type': 'select',
     'var_category': 'Voyage Outcome',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True,
     "note": "Derived from particular outcome"},
    {'var_name': 'var_outcome_owner',
     'spss_name': 'fate4',
     'var_full_name': 'Outcome of voyage for owner*',
     'var_type': 'select',
     'var_category': 'Voyage Outcome',
     "is_estimate": False,
     "is_basic": True,
     "is_general": True,
     "note": "Derived from particular outcome"},
    {'var_name': 'var_resistance',
     'spss_name': 'resistance',
     'var_full_name': 'African resistance',
     'var_type': 'select',
     'var_category': 'Voyage Outcome',
     "is_estimate": False,
     "is_basic": True,
     "is_general": True},

    # Voyage Itinerary
    {'var_name': 'var_imp_port_voyage_begin',
     'spss_name': 'ptdepimp',
     'var_full_name': 'Place where voyage began*',
     'var_type': 'select_three_layers',
     'var_category': 'Voyage Itinerary',
     "is_estimate": False,
     "is_basic": True,
     "is_general": True,
     'choices': structure_places(models.VoyageItinerary.objects.values_list('imp_port_voyage_begin').distinct()),
#     'choices': all_place_list,
     "note": "Same as data variable in most cases, but derived from "
             "port of return for certain Brazilian voyages"},

    {'var_name': 'var_first_place_slave_purchase',
     'spss_name': 'plac1tra',
     'var_full_name': 'First place of slave purchase',
     'var_type': 'select_three_layers',
     'var_category': 'Voyage Itinerary',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True,
     'choices': structure_places(models.VoyageItinerary.objects.values_list('first_place_slave_purchase').distinct())},
#     'choices': all_place_list},

    {'var_name': 'var_second_place_slave_purchase',
     'spss_name': 'plac2tra',
     'var_full_name': 'Second place of slave purchase',
     'var_type': 'select_three_layers',
     'var_category': 'Voyage Itinerary',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True,
     'choices': structure_places(models.VoyageItinerary.objects.values_list('second_place_slave_purchase').distinct())},
#     'choices': all_place_list},

    {'var_name': 'var_third_place_slave_purchase',
     'spss_name': 'plac3tra',
     'var_full_name': 'Third place of slave purchase',
     'var_type': 'select_three_layers',
     'var_category': 'Voyage Itinerary',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True,
     'choices': structure_places(models.VoyageItinerary.objects.values_list('third_place_slave_purchase').distinct())},
#     'choices': all_place_list},

    {'var_name': 'var_imp_principal_place_of_slave_purchase',
     'spss_name': 'mjbyptimp',
     'var_full_name': 'Principal place of slave purchase*',
     'var_type': 'select_three_layers',
     'var_category': 'Voyage Itinerary',
     "is_estimate": True,
     "is_basic": True,
     "is_general": True,
     'choices': structure_places(models.VoyageItinerary.objects.values_list('imp_principal_place_of_slave_purchase').distinct()),
#     'choices': all_place_list,
     "note": "Place where largest number of captives embarked"},

    {'var_name': 'var_port_of_call_before_atl_crossing',
     'spss_name': 'npafttra',
     'var_full_name': 'Places of call before Atlantic crossing',
     'var_type': 'select_three_layers',
     'var_category': 'Voyage Itinerary',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True,
     'choices': structure_places(models.VoyageItinerary.objects.values_list('port_of_call_before_atl_crossing').distinct())},
#     'choices': all_place_list},

    {'var_name': 'var_first_landing_place',
     'spss_name': 'sla1port',
     'var_full_name': 'First place of slave landing',
     'var_type': 'select_three_layers',
     'var_category': 'Voyage Itinerary',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True,
     'choices': structure_places(models.VoyageItinerary.objects.values_list('first_landing_place').distinct())},
#     'choices': all_place_list},

    {'var_name': 'var_second_landing_place',
     'spss_name': 'adpsale1',
     'var_full_name': 'Second place of slave landing',
     'var_type': 'select_three_layers',
     'var_category': 'Voyage Itinerary',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True,
     'choices': structure_places(models.VoyageItinerary.objects.values_list('second_landing_place').distinct())},
#     'choices': all_place_list},

    {'var_name': 'var_third_landing_place',
     'spss_name': 'adpsale2',
     'var_full_name': 'Third place of slave landing',
     'var_type': 'select_three_layers',
     'var_category': 'Voyage Itinerary',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True,
     'choices': structure_places(models.VoyageItinerary.objects.values_list('third_landing_place').distinct())},
#     'choices': all_place_list},

    {'var_name': 'var_imp_principal_port_slave_dis',
     'spss_name': 'mjslptimp',
     'var_full_name': 'Principal place of slave landing*',
     'var_type': 'select_three_layers',
     'var_category': 'Voyage Itinerary',
     "is_estimate": True,
     "is_basic": True,
     "is_general": True,
     'choices': structure_places(models.VoyageItinerary.objects.values_list('imp_principal_port_slave_dis').distinct()),
#     'choices': all_place_list,
     "note": "Place where largest number of captives embarked"},

    {'var_name': 'var_place_voyage_ended',
     'spss_name': 'portret',
     'var_full_name': 'Place where voyage ended',
     'var_type': 'select_three_layers',
     'var_category': 'Voyage Itinerary',
     "is_estimate": False,
     "is_basic": True,
     "is_general": True,
     'choices': structure_places(models.VoyageItinerary.objects.values_list('place_voyage_ended').distinct())},
#     'choices': all_place_list},

    # Itinerary - region variables
    {'var_name': 'var_imp_region_voyage_begin',
     'spss_name': 'deptregimp',
     'var_full_name': 'Region where voyage began*',
     'var_category': 'Voyage Itinerary',
     "is_estimate": False,
     "is_basic": False,
     "is_general": False},

    {'var_name': 'var_first_region_slave_emb',
     'spss_name': 'regem1',
     'var_full_name': 'First region of slave purchase',
     'var_category': 'Voyage Itinerary',
     "is_estimate": False,
     "is_basic": False,
     "is_general": False},


    {'var_name': 'var_second_region_slave_emb',
     'spss_name': 'regem2',
     'var_full_name': 'Second region of slave purchase',
     'var_category': 'Voyage Itinerary',
     "is_estimate": False,
     "is_basic": False,
     "is_general": False},

    {'var_name': 'var_third_region_slave_emb',
     'spss_name': 'regem3',
     'var_full_name': 'Third region of slave purchase',
     'var_category': 'Voyage Itinerary',
     "is_estimate": False,
     "is_basic": False,
     "is_general": False},

    {'var_name': 'var_imp_principal_region_of_slave_purchase',
     'spss_name': 'majbyimp',
     'var_full_name': 'Principal region of slave purchase*',
     'var_category': 'Voyage Itinerary',
     "is_estimate": False,
     "is_basic": False,
     "is_general": False},

    {'var_name': 'var_first_landing_region',
     'spss_name': 'regdis1',
     'var_full_name': 'First region of slave landing',
     'var_category': 'Voyage Itinerary',
     "is_estimate": False,
     "is_basic": False,
     "is_general": False},

    {'var_name': 'var_second_landing_region',
     'spss_name': 'regdis2',
     'var_full_name': 'Second region of slave landing',
     'var_category': 'Voyage Itinerary',
     "is_estimate": False,
     "is_basic": False,
     "is_general": False},

    {'var_name': 'var_third_landing_region',
     'spss_name': 'regdis3',
     'var_full_name': 'Third region of slave landing',
     'var_category': 'Voyage Itinerary',
     "is_estimate": False,
     "is_basic": False,
     "is_general": False},

    {'var_name': 'var_imp_principal_region_slave_dis',
     'spss_name': 'mjselimp',
     'var_full_name': 'Principal region of slave landing*',
     'var_category': 'Voyage Itinerary',
     "is_estimate": False,
     "is_basic": False,
     "is_general": False},

    {'var_name': 'var_region_voyage_ended',
     'spss_name': 'retrnreg',
     'var_full_name': 'Region where voyage ended',
     'var_category': 'Voyage Itinerary',
     "is_estimate": False,
     "is_basic": False,
     "is_general": False},

    # Voyage Dates
    {'var_name': 'var_imp_arrival_at_port_of_dis',
     'spss_name': 'yearam',
     'var_full_name': 'Year arrived with slaves*',
     'var_type': 'numeric',
     'var_category': 'Voyage Dates',
     "is_estimate": True,
     "is_basic": True,
     "is_general": True,
     "note": "Standard variable for classification by year of voyage"},
    {'var_name': 'var_voyage_began',
     'spss_name': 'date_dep',
     'var_full_name': 'Date voyage began',
     'var_type': 'date',
     'var_category': 'Voyage Dates',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True},
    {'var_name': 'var_slave_purchase_began',
     'spss_name': 'date_buy',
     'var_full_name': 'Date trade began in Africa',
     'var_type': 'date',
     'var_category': 'Voyage Dates',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True},
    {'var_name': 'var_date_departed_africa',
     'spss_name': 'date_leftAfr',
     'var_full_name': 'Date vessel departed Africa',
     'var_type': 'date',
     'var_category': 'Voyage Dates',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True},
    {'var_name': 'var_first_dis_of_slaves',
     'spss_name': 'date_land1',
     'var_full_name': 'Date vessel arrived with slaves',
     'var_type': 'date',
     'var_category': 'Voyage Dates',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True},
    {'var_name': 'var_departure_last_place_of_landing',
     'spss_name': 'date_depam',
     'var_full_name': 'Date vessel departed for homeport',
     'var_type': 'date',
     'var_category': 'Voyage Dates',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True},
    {'var_name': 'var_voyage_completed',
     'spss_name': 'date_end',
     'var_full_name': 'Date voyage completed',
     'var_type': 'date',
     'var_category': 'Voyage Dates',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True},
    {'var_name': 'var_imp_length_home_to_disembark',
     'spss_name': 'voy1imp',
     'var_full_name': 'Voyage length, homeport to slaves landing (days)*',
     'var_type': 'numeric',
     'var_category': 'Voyage Dates',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True,
     "note": "Difference between date voyage began and date vessel "
             "arrived with slaves"},
    {'var_name': 'var_length_middle_passage_days',
     'spss_name': 'voy2imp',
     'var_full_name': 'Middle passage (days)*',
     'var_type': 'numeric',
     'var_category': 'Voyage Dates',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True,
     "note": "Difference between date vessel left Africa "
             "and date it arrived with slaves"},
    # Captain and Crew
    {'var_name': 'var_captain',
     'spss_name': 'captain',
     'var_full_name': 'Captain\'s name',
     'var_type': 'plain_text',
     'var_category': 'Captain and Crew',
     "is_estimate": False,
     "is_basic": True,
     "is_general": True},
    {'var_name': 'var_crew_voyage_outset',
     'spss_name': 'crew1',
     'var_full_name': 'Crew at voyage outset',
     'var_type': 'numeric',
     'var_category': 'Captain and Crew',
     "is_estimate": False,
     "is_basic": True,
     "is_general": True},
    {'var_name': 'var_crew_first_landing',
     'spss_name': 'crew3',
     'var_full_name': 'Crew at first landing of slaves',
     'var_type': 'numeric',
     'var_category': 'Captain and Crew',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True},
    {'var_name': 'var_crew_died_complete_voyage',
     'spss_name': 'crewdied',
     'var_full_name': 'Crew deaths during voyage',
     'var_type': 'numeric',
     'var_category': 'Captain and Crew',
     "is_estimate": False,
     "is_basic": True,
     "is_general": True},

    # Slaves (numbers)
    {'var_name': 'var_num_slaves_intended_first_port',
     'spss_name': 'slintend',
     'var_full_name': 'Number of slaves intended at first place of purchase',
     'var_type': 'numeric',
     'var_category': 'Slave (numbers)',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True},
    {'var_name': 'var_num_slaves_carried_first_port',
     'spss_name': 'ncar13',
     'var_full_name': 'Slaves carried from first port of purchase',
     'var_type': 'numeric',
     'var_category': 'Slave (numbers)',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True},
    {'var_name': 'var_num_slaves_carried_second_port',
     'spss_name': 'ncar15',
     'var_full_name': 'Slaves carried from second port of purchase',
     'var_type': 'numeric',
     'var_category': 'Slave (numbers)',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True},
    {'var_name': 'var_num_slaves_carried_third_port',
     'spss_name': 'ncar17',
     'var_full_name': 'Slaves carried from third port of purchase',
     'var_type': 'numeric',
     'var_category': 'Slave (numbers)',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True},
    {'var_name': 'var_total_num_slaves_purchased',
     'spss_name': 'tslavesd',
     'var_full_name': 'Total slaves embarked',
     'var_type': 'numeric',
     'var_category': 'Slave (numbers)',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True},
    {'var_name': 'var_imp_total_num_slaves_purchased',
     'spss_name': 'slaximp',
     'var_full_name': 'Total slaves embarked*',
     'var_type': 'numeric',
     'var_category': 'Slave (numbers)',
     "is_estimate": True,
     "is_basic": True,
     "is_general": True,
     "note": "Estimated embarkations"},
    {'var_name': 'var_total_num_slaves_arr_first_port_embark',
     'spss_name': 'slaarriv',
     'var_full_name': 'Number of slaves arriving at first place of landing',
     'var_type': 'numeric',
     'var_category': 'Slave (numbers)',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True},
    {'var_name': 'var_num_slaves_disembark_first_place',
     'spss_name': 'slas32',
     'var_full_name': 'Number of slaves disembarked at first place of landing',
     'var_type': 'numeric',
     'var_category': 'Slave (numbers)',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True},
    {'var_name': 'var_num_slaves_disembark_second_place',
     'spss_name': 'slas36',
     'var_full_name': 'Number of slaves disembarked at second place of landing',
     'var_type': 'numeric',
     'var_category': 'Slave (numbers)',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True},
    {'var_name': 'var_num_slaves_disembark_third_place',
     'spss_name': 'slas39',
     'var_full_name': 'Number of slaves disembarked at third place of landing',
     'var_type': 'numeric',
     'var_category': 'Slave (numbers)',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True},
    {'var_name': 'var_imp_total_slaves_disembarked',
     'spss_name': 'slamimp',
     'var_full_name': 'Total slaves disembarked*',
     'var_type': 'numeric',
     'var_category': 'Slave (numbers)',
     "is_estimate": True,
     "is_basic": True,
     "is_general": True,
     "note": "Estimated embarkations"},

    # Slaves (characteristics)
    {'var_name': 'var_imputed_percentage_men',
     'spss_name': 'menrat7',
     'var_full_name': 'Percentage men*',
     'var_type': 'numeric',
     'var_category': 'Slave (characteristics)',
     "is_estimate": False,
     "is_basic": True,
     "is_general": True,
     "note" : "Captives identified by age and gender"},
    {'var_name': 'var_imputed_percentage_women',
     'spss_name': 'womrat7',
     'var_full_name': 'Percentage women*',
     'var_type': 'numeric',
     'var_category': 'Slave (characteristics)',
     "is_estimate": False,
     "is_basic": True,
     "is_general": True,
     "note" : "Captives identified by age and gender"},
    {'var_name': 'var_imputed_percentage_boys',
     'spss_name': 'boyrat7',
     'var_full_name': 'Percentage boys*',
     'var_type': 'numeric',
     'var_category': 'Slave (characteristics)',
     "is_estimate": False,
     "is_basic": True,
     "is_general": True,
     "note" : "Captives identified by age and gender"},
    {'var_name': 'var_imputed_percentage_girls',
     'spss_name': 'girlrat7',
     'var_full_name': 'Percentage girls*',
     'var_type': 'numeric',
     'var_category': 'Slave (characteristics)',
     "is_estimate": False,
     "is_basic": True,
     "is_general": True,
     "note" : "Captives identified by age and gender"},
    {'var_name': 'var_imputed_percentage_male',
     'spss_name': 'malrat7',
     'var_full_name': 'Percentage male*',
     'var_type': 'numeric',
     'var_category': 'Slave (characteristics)',
     "is_estimate": False,
     "is_basic": True,
     "is_general": True,
     "note" : "Captives identified by gender (males/females)"},
    {'var_name': 'var_imputed_percentage_child',
     'spss_name': 'chilrat7',
     'var_full_name': 'Percentage children*',
     'var_type': 'numeric',
     'var_category': 'Slave (characteristics)',
     "is_estimate": False,
     "is_basic": True,
     "is_general": True,
     "note" : "Captives identified by age group (adults/children)"},
    {'var_name': 'var_imputed_sterling_cash',
     'spss_name': 'jamcaspr',
     'var_full_name': 'Sterling cash price in Jamaica*',
     'var_type': 'numeric',
     'var_category': 'Slave (characteristics)',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True},
    {'var_name': 'var_imputed_death_middle_passage',
     'spss_name': 'vymrtimp',
     'var_full_name': 'Slave deaths during middle passage*',
     'var_type': 'numeric',
     'var_category': 'Slave (characteristics)',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True,
     "note": "Documented or difference between embarked "
             "and disembarked captives (data variables)"},
    {'var_name': 'var_imputed_mortality',
     'spss_name': 'vymrtrat',
     'var_full_name': 'Mortality rate*',
     'var_type': 'numeric',
     'var_category': 'Slave (characteristics)',
     "is_estimate": False,
     "is_basic": True,
     "is_general": True,
     "note": "Slave deaths during Middle Passage divided by number of "
             "captives leaving Africa"},

    # Source
    {'var_name': 'var_sources',
     'spss_name': 'source',
     'var_full_name': 'Sources',
     'var_type': 'plain_text',
     'var_category': 'Source',
     "is_estimate": False,
     "is_basic": True,
     "is_general": True}
]

# This variable has only these field visible
var_imp_principal_place_of_slave_purchase_fields = ["Africa", "Other"]

paginator_range_factors = [-4, -3, -2, -1, 0, 1, 2, 3, 4]
option_results_per_page = [10, 15, 20, 30, 50, 100, 200]

basic_variables = []
for item in var_dict:
    if item['is_basic']:
        basic_variables.append(item)

general_variables = []
for item in var_dict:
    if item['is_general']:
        general_variables.append(item)

list_text_fields = []
for item in var_dict:
    if 'var_type' in item and item['var_type'] == 'plain_text':
        list_text_fields.append(item['var_name'])

list_select_fields = []
for item in var_dict:
    if 'var_type' in item and item['var_type'] == 'select':
        list_select_fields.append(item['var_name'])

list_numeric_fields = []
for item in var_dict:
    if 'var_type' in item and item['var_type'] == 'numeric':
        list_numeric_fields.append(item['var_name'])

list_date_fields = []
for item in var_dict:
    if 'var_type' in item and item['var_type'] == 'date':
        list_date_fields.append(item['var_name'])

list_place_fields = []
for item in var_dict:
    if 'var_type' in item and item['var_type'] == 'select_three_layers':
        list_place_fields.append(item['var_name'])

list_boolean_fields = []
for item in var_dict:
    if 'var_type' in item and item['var_type'] == 'boolean':
        list_boolean_fields.append(item['var_name'])

# List of default result columns
default_result_columns = [
    'var_voyage_id',
    'var_ship_name',
    'var_captain',
    'var_imp_arrival_at_port_of_dis',
    'var_imp_principal_region_of_slave_purchase',
    'var_imp_principal_region_slave_dis',
]

# Dictionary of sources
sources_id = {
    'documentary': 0,
    'newspapers': 1,
    'published_sources': 2,
    'unpublished_secondary_sources': 3,
    'private_notes_and_collections': 4
}


# Source types sorted by letters
letters_sorted_source_types = [
    "published_sources"
]

summary_statistics_columns = [
    '',
    'Total slaves',
    'Total voyages',
    'Average',
    'Standard deviation'
]

summary_statistics = [
    {'display_name' : 'Slaves embarked *', 'var_name': 'var_imp_total_num_slaves_purchased',
     'has_total': True, 'is_percentage' : False},
    {'display_name' : 'Slaves disembarked *', 'var_name': 'var_imp_total_slaves_disembarked',
     'has_total' : True, 'is_percentage' : False},
    {'display_name' : 'Percentage of slaves embarked who died during voyage *',
     'var_name': 'var_imputed_mortality', 'has_total' : False, 'is_percentage' : True},
    {'display_name' : 'Length of Middle Passage (in days) *',
     'var_name': 'var_length_middle_passage_days',
     'has_total' : False, 'is_percentage' : False},
    {'display_name' : 'Percentage male *', 'var_name': 'var_imputed_percentage_male',
     'has_total' : False, 'is_percentage' : True},
    {'display_name' : 'Percentage children*', 'var_name': 'var_imputed_percentage_child',
     'has_total' : False, 'is_percentage' : True},
    {'display_name' : 'Tonnage of vessel', 'var_name': 'var_tonnage',
     'has_total' : False, 'is_percentage' : False},
]

methodology_items = [
    {'number': 1,
     'name': "Introduction",
     'page': "methodology-1"},
    {'number': 2,
     'name': "Coverage of the Slave Trade",
     'page': "methodology-2"},
    {'number': 3,
     'name': "Nature of Sources",
     'page': "methodology-3"},
    {'number': 4,
     'name': "Cases and Variables",
     'page': "methodology-4"},
    {'number': 5,
     'name': "Data Variables",
     'page': "methodology-5"},
    {'number': 6,
     'name': "Age Categories",
     'page': "methodology-6"},
    {'number': 7,
     'name': "Dates",
     'page': "methodology-7"},
    {'number': 8,
     'name': "Names",
     'page': "methodology-8"},
    {'number': 9,
     'name': "Imputed Variables",
     'page': "methodology-9"},
    {'number': 10,
     'name': "Geographic Data",
     'page': "methodology-10"},
    {'number': 11,
     'name': "Imputed Voyage Dates",
     'page': "methodology-11"},
    {'number': 12,
     'name': "Classification as a Trans-Atlantic Slavic Voyage",
     'page': "methodology-12"},
    {'number': 13,
     'name': "Voyage Outcomes",
     'page': "methodology-13"},
    {'number': 14,
     'name': "Inferring Places of Trade",
     'page': "methodology-14"},
    {'number': 15,
     'name': "Imputed Numbers of Slaves",
     'page': "methodology-15"},
    {'number': 16,
     'name': "Regions of Embarkation and Disembarkation",
     'page': "methodology-16"},
    {'number': 17,
     'name': "Age and Gender Ratios",
     'page': "methodology-17"},
    {'number': 18,
     'name': "National Carriers",
     'page': "methodology-18"},
    {'number': 19,
     'name': "Tonnage",
     'page': "methodology-19"},
    {'number': 20,
     'name': "Resistance and Price of Slaves",
     'page': "methodology-20"},
    {'number': 21,
     'name': "Appendix",
     'page': "methodology-21"},
    {'number': 22,
     'name': "Notes",
     'page': "methodology-22"},
]


# Timeline part
def get_average_set_timeline(query_dict, var_name, start_year, stop_year):
    """Calculate average of var and create a list divided by years

    :param query_dict: Query dictionary, on which based on
    calculation will be performed
    :param var_name: Appropriate name of solr variable
    :return: list of values [['year', 'value'],]
    """

    timeline_list = []

    for i in range(start_year, stop_year):
        # For each year, get stats on var_name
        value = query_dict.filter(var_imp_arrival_at_port_of_dis=i).stats(var_name).stats_results()

        # If results available, store mean
        if value[var_name] is not None:
            timeline_list.append([i, round(value[var_name]['mean'], 1)])

    # Sort based on years and return
    timeline_list.sort(key=lambda tup: tup[0])
    return timeline_list


def get_sum_set_timeline(query_dict, var_name, start_year, stop_year):
    """Calculate sum of var and create a list divided by years

    :param query_dict: Query dictionary, on which based on
    calculation will be performed
    :param var_name: Appropriate name of solr variable
    :return: list of values [['year', 'value'],]
    """

    timeline_list = []

    for i in range(start_year, stop_year):
        # For each year, get stats on var_name
        value = query_dict.filter(var_imp_arrival_at_port_of_dis=i).stats(var_name).stats_results()

        # If results available, store sum
        if value[var_name] is not None:
            timeline_list.append([i, round(value[var_name]['sum'], 1)])

    # Sort based on years and return
    timeline_list.sort(key=lambda tup: tup[0])
    return timeline_list


def get_exist_set_timeline(query_dict, var_name, start_year, stop_year):
    """Calculate exist/nonexist ratio of var and create a list divided by years

    :param query_dict: Query dictionary, on which based on
    calculation will be performed
    :param var_name: Appropriate name of solr variable
    :return: list of values [['year', 'value'],]
    """

    timeline_list = []

    for i in range(start_year, stop_year):
        # For each year, get stats on var_name
        value = query_dict.filter(var_imp_arrival_at_port_of_dis=i).stats(var_name)
        value_result = value.stats_results()

        # If results available, calculate not_null/all and get percent of this (*100)
        if value_result[var_name] is not None:
            timeline_list.append([i, round((float(value_result[var_name]['count'])/float(len(value))*100), 1)])

    # Sort based on years and return
    timeline_list.sort(key=lambda tup: tup[0])
    return timeline_list


def get_percentage_set_timeline(query_dict, var_name, start_year, stop_year):
    """Calculate mean of var (in percent scale) and create a list divided by years

    :param query_dict: Query dictionary, on which based on
    calculation will be performed
    :param var_name: Appropriate name of solr variable
    :return: list of values [['year', 'value'],]
    """

    timeline_list = []

    for i in range(start_year, stop_year):
        # For each year, get stats on var_name
        value = query_dict.filter(var_imp_arrival_at_port_of_dis=i).stats(var_name).stats_results()

        # If results available, get mean and present as percent (*100)
        if value[var_name] is not None:
            timeline_list.append([i, round(value[var_name]['mean']*100, 1)])

    # Sort based on years and return
    timeline_list.sort(key=lambda tup: tup[0])
    return timeline_list


def get_simple_set_timeline(query_dict, var_name, start_year=None, stop_year=None):
    """Create a list of values divided by years

    :param query_dict: Query dictionary, on which based on
    calculation will be performed
    :param var_name: Appropriate name of solr variable
    :return: list of values [['year', 'value'],]
    """

    # Facet on var_name, minimum 1 and limit 500 (first year is 1514, last 1866,
    # so '500' is fine
    timeline_list = query_dict.facet(var_name, mincount=1, limit=500).facet_counts()

    # Create list of lists, where inner list is in form of: [year, value]
    timeline_list = [[int(v[0]), v[1]] for v in timeline_list['fields'][var_name]]

    # Sort based on years and return
    timeline_list.sort(key=lambda tup: tup[0])
    return timeline_list

# List of options and settings for timeline in form of:
# (index, name, function_to_get_set, variable in solr, [extra_dict])
voyage_timeline_variables = [
    ('0', _('Number of voyages'), get_simple_set_timeline, 'var_imp_arrival_at_port_of_dis'),
    ('1', _('Average tonnage'), get_average_set_timeline, 'var_tonnage'),
    ('2', _('Average tonnage (standardized)'), get_average_set_timeline, 'var_tonnage_mod'),
    ('3', _('Average number of guns'), get_average_set_timeline, 'var_guns_mounted'),
    ('4', _('Rate of resistance'), get_exist_set_timeline, 'var_resistance_idnum',
     {"suffix": "%", 'tickInterval': 10, 'min': 0, 'max': 100}),
    ('5', _('Average duration of voyage from home port to disembarkation (days)'),
     get_average_set_timeline, "var_imp_length_home_to_disembark", {"no_numeric_symbol:" : True}),
    ('6', _('Average duration of middle passage (days)'), get_average_set_timeline, 'var_length_middle_passage_days'),
    ('7', _('Average crew at outset'), get_average_set_timeline, 'var_crew_voyage_outset'),
    ('8', _('Average crew at first landing of slaves'), get_average_set_timeline, 'var_crew_first_landing'),
    ('9', _('Number of crew deaths'), get_sum_set_timeline, 'var_crew_died_complete_voyage'),
    ('10', _('Average crew deaths'), get_average_set_timeline, 'var_crew_died_complete_voyage'),
    ('11', _('Intended number of purchases'), get_sum_set_timeline, 'var_num_slaves_intended_first_port'),
    ('12', _('Average intended purchases'), get_average_set_timeline, 'var_num_slaves_intended_first_port'),
    ('13', _('Total number of captives embarked'), get_sum_set_timeline, 'var_imp_total_num_slaves_purchased'),
    ('14', _('Average number of captives embarked'), get_average_set_timeline, 'var_imp_total_num_slaves_purchased'),
    ('15', _('Total number of captives disembarked'), get_sum_set_timeline, 'var_imp_total_slaves_disembarked'),
    ('16', _('Average number of captives disembarked'), get_average_set_timeline, 'var_imp_total_slaves_disembarked'),
    ('17', _('Percentage men (among captives)'), get_percentage_set_timeline, 'var_imputed_percentage_men',
     {"suffix": "%"}),
    ('18', _('Percentage women (among captives)'), get_percentage_set_timeline, 'var_imputed_percentage_women',
     {"suffix": "%"}),
    ('19', _('Percentage boys (among captives)'), get_percentage_set_timeline, 'var_imputed_percentage_boys',
     {"suffix": "%"}),
    ('20', _('Percentage girls (among captives)'), get_percentage_set_timeline, 'var_imputed_percentage_girls',
     {"suffix": "%"}),
    ('21', _('Percentage female (among captives)'), get_percentage_set_timeline, 'var_imputed_percentage_female',
     {"suffix": "%"}),
    ('22', _('Percentage male (among captives)'), get_percentage_set_timeline, 'var_imputed_percentage_male',
     {"suffix": "%", "max": 100}),
    ('23', _('Sterling cash price in Jamaica*'), get_average_set_timeline, 'var_imputed_sterling_cash',
     {'max': 90, 'tickInterval': 10}),
    ('24', _('Number of slave deaths'), get_sum_set_timeline, 'var_imputed_death_middle_passage'),
    ('25', _('Average slave deaths'), get_average_set_timeline, 'var_imputed_death_middle_passage'),
    ('26', _('Average percentage of slaves embarked who died during the voyage'), get_percentage_set_timeline, 'var_imputed_mortality',
     {"suffix": "%", "max": 100})
]