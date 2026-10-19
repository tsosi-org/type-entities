import pandas as pd, json, requests
from modules import *


today_date = pd.Timestamp.today().strftime("%Y-%m-%d")


## ___1___ load data from tsosi.org 

## get new entities
raw_entities = requests.get("https://tsosi.org/api/entities/all?format=json").json()

## flatten entities
[flatten_entities(item) for item in raw_entities]

df_raw  = pd.json_normalize(raw_entities)

## add tsosi_url 
df_raw["tsosi_link"] = "https://tsosi.org/entities/" + df_raw["tsosi_id"].astype(str)

print(f"nb of entities {len(df_raw)}")


## ___2___ remove known entities (optain with manual curation process)

df_known_entities = pd.read_csv("TSOSI-type-entities.csv", encoding="utf-8")
print(f"nb of entities with already a type {len(df_known_entities)}")

# new entities where we have not tsosi type
df_new_entities = df_raw[ ~df_raw["tsosi_id"].isin(df_known_entities["tsosi_id"]) ].reset_index(drop=True)

print(f"nb of unknown entities {len(df_new_entities)}")


## ___3___ find possible consortia

df_intermed = df_new_entities[df_new_entities["is_agent"] == True ][["name", "short_name", "country", "tsosi_id", "ror_id", "wiki_id", "tsosi_link" ]].reset_index(drop=True)

#print(len(df_intermed))

output_results(
	df_intermed, 
	f"{today_date}--possible-consortia.csv"
	)


# ___4___ find possible funders

df_funders = df_new_entities[["name", "short_name", "country", "tsosi_id", "ror_id", "wiki_id", "id", "ror_types", "tsosi_link"]].copy()


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

