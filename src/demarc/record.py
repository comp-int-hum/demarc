import json
import re
from importlib.resources import files

def subcodes(v):
    for sf in v.get("subfields", []):
        for subcode, subval in sf.items():
            yield (subcode, subval)

def parse_timestamp(ts, ind1, ind2, field_code):
    year = int(ts[0:4])
    month = int(ts[4:6])
    day = int(ts[6:8])
    hour = int(ts[8:10])
    minute = int(ts[10:12])
    second = float(ts[12:16])        
    return {
        "year" : year,
        "month" : month,
        "day" : day,
        "hour" : hour,
        "minute" : minute,
        "second" : second
    }

def parse_year(y, ind1, ind2, field_code):
    m = re.match(r"^\D*(\d{4})\D*$", y)
    if m:
        return int(m.group(1))
    else:
        #print(field_code, y)
        return None

def parse_years(y, ind1, ind2, field_code):
    m = re.match(r"^.*(\d{4})\D*$", y)
    if m:
        return int(m.group(1))
    else:
        #print(field_code, y)
        return None
    
def parse_entry_date(ed, ind1, ind2, field_code):
    year = int(ed[:2])
    month = int(ed[2:4])
    day = int(ed[4:6])
    year = year + (1900 if year > 30 else 2000)
    return {"year" : year, "month" : month, "day" : day}

def parse_update(ed, ind1, ind2, field_code):
    year = int(ed[:4])
    month = int(ed[4:6])
    day = int(ed[6:8])
    return {"year" : year, "month" : month, "day" : day}


def id(val, ind1, ind2, field_code):
    return val

def parse_relation(val, ind1, ind2, field_code):
    if "author" in val.lower():
        return "author"
    else:
        return None

def parse_relator(val, ind1, ind2, field_code):
    #print(val)
    return val

    
value_parsers = {
    "years" : parse_years,
    "year" : parse_year,
    "timestamp" : parse_timestamp,
    "relation" : parse_relation,
    "relator" : parse_relator
}

field_specs = json.loads(re.sub(r"#.*", "", files("demarc").joinpath("data/field_specs.json").read_text()))


# fixed_widths = {
#     "001" : "control_number",
#     "003" : "control_number_organization",
#     "005" : ("latest_change", parse_timestamp), # = v # yyyymmddhhmmss.f
#     "006" : { # additional material characteristics
#         (0, 1) : { # Form of Material
#             ("a", "c") : { # Books
#                 (5, 6) : "target_audience",
#                 (6, 7) : "form_of_item",
#                 (7, 11) : "nature_of_contents",
#                 (11, 12) : "government_publication",
#                 (12, 13) : "conference_publication",
#                 (13, 14) : "festschrift",
#                 (14, 15) : "index",
#                 (15, 16) : "undefined",
#                 (16, 17) : "literary_form",
#                 (17, 18) : "biography"
#             },
#             ("c", "d", "i", "j") : { # Music
#             },
#             ("e", "f") : { # Maps
#             },
#             ("g", "k") : { # Visual Materials
#             },
#             ("m",) : { # Computer Files
#             },
#             ("p",) : { # Mixed Materials
#             },
#             ("s",) : { # Continuing Resources
#             }
#         }
#     },
#     "007" : { # physical description
#         (0, 1) : { # Category of Material
#             "a" : {
#             },
#             "c" : {
#             },
#             "d" : {
#             },
#             "f" : {
#             },
#             "g" : {
#             },
#             "h" : {
#             },
#             "k" : {
#             },
#             "m" : {
#             },
#             "o" : {
#             },
#             "q" : {
#             },
#             "r" : {
#             },
#             "s" : {
#             },
#             "t" : {
#             },
#             "v" : {
#             },
#             "z" : {
#             }
#         }
#     },
#     "008" : { # data elements
#         (0, 6) : ("date_entered", parse_entry_date),
#         (6, 7) : "type_of_date",
#         (7, 11) : ("first_date", parse_year),
#         (11, 15) : ("second_date", parse_year),
#         (15, 18) : "place_of_publication",
#         (35, 38) : "language",
#         (38, 39) : "modified_record",
#         (39, 40) : "cataloguing_source",
#         "ht_type" : {
#             "BK" : { # Books
#                 (22, 23) : "target_audience",
#                 (23, 24) : "form_of_item",
#                 (24, 28) : "nature_of_contents",
#                 (28, 29) : "government_publication",
#                 (29, 30) : "conference_publication",
#                 (30, 31) : "festschrift",
#                 (31, 32) : "index",
#                 (32, 33) : "undefined",
#                 (33, 34) : "literary_form",
#                 (34, 35) : "biography"
#             },
#             "CF" : { # Computer Files
#             },
#             "MP" : { # Maps
#             },
#             "MU" : { # Music
#             },
#             "CR" : { # Continuing Resources
#             },
#             "VM" : { # Visual Materials
#             },
#             "MX" : { # Mixed Materials
#             }
#         }
#     },
#     "009" : "local_use",
# }

# non_fixed_widths = {
#     # 010-09x for identifiers/classifiers
#     "100" : {
#         "a" : "author_name",
#         "b" : "author_numeration",
#         "c" : "author_titles",
#         "d" : ("dates_associated_with_a_name", parse_years),
#         "e" : "author_relator_term",
#         "f" : "work_date",
#         "j" : "attribution_qualifier",
#         "l" : "work_language",
#         "q" : "fuller_form_of_author_name",
#         "t" : "title_of_work",
#         "0" : "author_authority_record_control_number",
#         "1" : None, # "author_real_world_object_uri", # duplicates
#         "6" : "linkage"
#     },
#     "110" : {
#         "a" : "corporate_name",
#         "b" : None, #"subordinate_unit", # duplicates
#         "e" : None, # "corporate_relator_term", # duplicates
#         "f" : "corporate_date_of_work",
#         "k" : "form_subheading",
#         "w" : None, # error?
#         "0" : "corporate_authority_record_control_number",
#         "1" : None, # "corporate_real_world_object_uri" # duplicates
#     },
#     "111" : {
#         "a" : "meeting_name",
#         "c" : None, # "meeting_location", # duplicates
#         "d" : "meeting_date",
#         "n" : "meeting_part_number",
#         "0" : "meeting_authority_record_control_number",
#         "1" : "meeting_real_world_object_uri"
#     },
#     "130" : {
#         "a" : "uniform_title",
#         "f" : "uniform_title_date",
#         "k" : "uniform_title_subheading",
#         "l" : "uniform_title_language",
#         "n" : "uniform_section_number",
#         "p" : None, # "uniform_title_subsection_name" # duplicates
#         "0" : None, # "authority_record_control_number", # duplicates
#         "1" : None, # "real_world_object_uri", # duplicates
#         "6" : None # "linkage" # duplicates
#     },
#     "240" : {
#         "a" : "uniform_title",
#         "d" : "date_of_treaty_signing",
#         "f" : "date_of_a_work",
#         "g" : "miscellaneous_information",
#         "h" : "medium",
#         "k" : "form_subheading",
#         "l" : "language_of_a_work"
#     },
#     "245" : {
#         "a" : "title",
#         "f" : "inclusive_dates",
#         "g" : "bulk_dates"
#     },
#     #         # 260 (264?) pub (a loc) (c year)
#     #         # 250 edition
#     "410" : {
#     },
#     "490" : {
#     },
#     #         # 300 dimensions?
#     #         # 5XX notes open description
#     #"600" : {
#     #    "a" : "personal_name",
#     #    "f" : "date_of_a_work"
#     #},
#     "880" : { # alternate graphical representation
#         "a" : None,
#         "b" : None,
#         "c" : None,
#         "d" : None,
#         "q" : None,        
#     },
#     "899" : { # local (non-standard) series
#         "a" : None, # "local_series_uniform_title",
#         "b" : None, # unknown
#         "c" : None, # unknown
#         "7" : None  # "local_series_control_subfield",        
#     },
#     "970" : {
#         "a" : "type"
#     },
#     "974" : {
#         "a" : None, # also digitization source?
#         "b" : None, # also collection code?
#         "c" : "collection_code",
#         "d" : "update_date",
#         "q" : "rights_reason",
#         "r" : "rights_attribute",
#         "s" : "digitization_source",
#         "u" : "id",
#         "y" : "publication_date",
#         "z" : "chronology_enumeration_information"
#     }
# }

class Record(dict):

    def get_first(self, fields):
        for field in fields:
            if self.get(field):
                return self[field]
        return None

    @property
    def is_translated(self):
        return "tr" in self.get("added_entry_personal_name relator_term", "").lower()
    
    @property
    def htid(self):
        return self.get("hathitrust id")

    @property
    def language(self):
        fields = ["data_elements language"]
        return self.get_first(fields)
    
    @property
    def title(self):
        fields = ["uniform_title uniform_title", "title_statement title", "main_entry_personal_name title_of_work"]
        return self.get_first(fields)

    @property
    def relation(self):
        fields = ["main_entry_personal_name relator_term"]
        return self.get_first(fields)

    @property
    def person_date(self):
        fields = ["main_entry_personal_name dates_associated_with_a_name"]
        return self.get_first(fields)
    
    @property
    def date(self):
        fields = [
            "main_entry_personal_name date_of_a_work",
            "main_entry_uniform_title date_of_a_work",
            "uniform_title date_of_a_work",
            "title_statement inclusive_dates",
            "title_statement bulk_dates",
            #"publication_distribution_etc date_of_publication",
            #"hathitrust publication_date"
        ]        
        retval = self.get_first(fields)
        if not retval and not self.is_translated:
            retval = self.get("main_entry_personal_name dates_associated_with_a_name")
        return retval

    @property
    def literary_form(self):
        litforms = {"0" : "nonfiction", "1" : "fiction", "d" : "drama", "e" : "essays", "f" : "novels", "h" : "humor", "i" : "letters", "j" : "short stories", "m" : "mixed", "p" : "poetry", "s" : "speeches", "u" : "unknown"}
        val = self.get_first(["data_elements literary_form"])
        return litforms.get(val, val)
    
    @property
    def author(self):
        fields = ["main_entry_personal_name personal_name"]
        return self.get_first(fields)
    
    def append(self, field_name, name, value, ind1=None, ind2=None, value_type=None):
        final_value = value_parsers.get(value_type, id)(value, ind1, ind2, field_name)
        final_key = "{} {}".format(field_name, name)
        self[final_key] = self.get(final_key, [])
        self[final_key].append(final_value)
            
    def __init__(self, j):
        self.type_of_record = j["leader"][6]
        for field in sorted(j["fields"], reverse=True, key=lambda x : list(x.keys())[0]):            
            for field_code, field_value in field.items():
                #field_name = field_names.get(field_code, "")
                #if field_name == None:
                #    continue
                #prefix = [] if field_name == "" else [field_name]
                field_spec = field_specs.get(field_code, {})
                field_name = field_spec.get("name", "")
                prefix = [] if field_name == "" else [field_name]
                if field_spec.get("fixed_width", False):
                    for fw_name, fw_spec in field_spec.get("mappings", {}).items():
                        self.append(
                            field_name=field_name,
                            name=fw_name,
                            value=field_value[fw_spec["start"]:fw_spec["end"]],
                            value_type=fw_spec.get("type", None)
                        )
                    for cmap_spec in field_spec.get("conditional_mappings", []):
                        switch_val = self.get(cmap_spec["switch_name"])[0] if "switch_name" in cmap_spec else field_value[cmap_spec["start"]:cmap_spec["end"]]
                        if switch_val in cmap_spec["values"]:
                            for fw_name, fw_spec in cmap_spec.get("mappings", {}).items():
                                self.append(
                                    field_name=field_name,
                                    name=fw_name,
                                    value=field_value[fw_spec["start"]:fw_spec["end"]],
                                    value_type=fw_spec.get("type")
                                )                                
                elif field_spec:
                    ind1 = field_value.get("ind1")
                    ind2 = field_value.get("ind2")
                    for subfield in field_value.get("subfields", []):
                        for subfield_code, subfield_value in subfield.items():
                            #print(field_code, subfield_code)
                            subfield_spec = field_spec.get("subfields", {}).get(subfield_code, {})
                            if isinstance(subfield_spec, str):
                                self.append(
                                    field_name=field_name,
                                    name=subfield_spec,
                                    value=subfield_value,
                                    ind1=ind1,
                                    ind2=ind2
                                )
                            elif subfield_spec:
                                self.append(
                                    field_name=field_name,
                                    name=subfield_spec["name"],
                                    value=subfield_value,
                                    value_type=subfield_spec.get("type"),
                                    ind1=ind1,
                                    ind2=ind2
                                )

        for k in list(self.keys()):
            if len(self[k]) == 1:
                self[k] = self[k][0]
            else:
                #assert len(set(self[k])) == 1, str(self)
                self[k] = self[k][0]
            if self[k] in ["#", "|", " "]:
                del self[k]
