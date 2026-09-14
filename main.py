import pandas as pd, json, requests
from modules import *


today_date = pd.Timestamp.today().strftime("%Y-%m-%d")


## ___1___ load data from tsosi.org 

## get new entities
raw_entities = requests.get("https://tsosi.org/api/entities/all?format=json").json()

## flatten entities
[flatten_entities(item) for item in raw_entities]

df_raw  = pd.json_normalize(raw_entities)


## add tsosi_link field
def get_tsosi_link(identifiers_in) :
	for item in identifiers_in :
		value = item.get("value")
		if value is not None:
			return f"https://tsosi.org/entities/{value}"
 
df_raw["tsosi_link"] = df_raw["identifiers"].apply(get_tsosi_link)
print(f"nb of entities {len(df_raw)}")


## ___2___ remove known entities
df_known_entities = pd.read_csv("TSOSI-type-entities.csv", encoding="utf-8")
print(f"nb of entities with already a type {len(df_known_entities)}")

#print(df_known_entities.columns)

# get sets of ROR and wiki id (dropna to avoid matching NaN)
known_ror = df_known_entities["ror_id"].dropna().unique()
known_wiki = df_known_entities["wiki_id"].dropna().unique()

mask = ~(
	df_raw["ror_id"].isin(known_ror) |
    df_raw["wiki_id"].isin(known_wiki)
)

# select entites for wich we did not provide types
df_new_entities = df_raw[mask].reset_index(drop=True)
print(f"nb of unknow entities {len(df_new_entities)}")



## ___3___ find possible consortia

df_intermed = df_new_entities[df_new_entities["is_agent"] == True ][["name", "country","ror_id", "wiki_id", "tsosi_link" ]].reset_index(drop=True)

#print(len(df_intermed))

output_results(
	df_intermed, 
	f"{today_date}--possible-consortia.md"
	)


# ___4___ find possible funders

df_funders = df_new_entities[["name", "short_name", "country", "ror_id", "wiki_id", "id", "ror_types", "tsosi_link"]].copy()


# deal with ror_types to use it as a list 
def norm_list(lst):
    if not isinstance(lst, (list, tuple)):
        return []
    return [str(item).strip().lower() for item in lst]

parsed = df_funders["ror_types"].apply(norm_list)

mask_gov = parsed.apply(lambda lst: "government" in lst)
mask_funder = parsed.apply(lambda lst: ("funder" in lst) & ("nonprofit" in lst))


df_possible_funders = df_funders[ mask_gov | mask_funder ].reset_index(drop=True)
df_possible_funders.drop_duplicates(subset=["id"], keep="first", inplace = True)


# ____z____ output result

## just change file name extension to produce csv or md
output_results(
	df_possible_funders, 
	f"{today_date}--possible-funders.csv"
	)

