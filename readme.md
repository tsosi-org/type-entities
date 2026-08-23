# TSOSI types for entities

Code and process to deduce _type_ field for all the TSOSI entities. A TSOSI entity is an element of the TSOSI network, like a university, a research funder, a scientific publisher, or a library consortium, etc. 
This repository contains the code that is run to help the identifying process. Code is run when a new infrastructure or a new library consortium is included in TSOSI.


>>>> See the distribution of TSOSI types online: https://tsosi.org/api/stats

## TSOSI types

- `infrastructure`

- `library consortium`

- `funding organisation`

- `company`

- `other`

Note that those types are unique, so that an entity cannot have both `other` and `library consortium`


## Repository logic

- `TSOSI-type-entities.csv` contains the classifications that have been done regarding library consortia and funding organisations (and also part of other).

- Files whose names start with a date are to be used manually to deduce the type.


## Rules for identifying entity type

> Rules are applied in the order listed; the first match wins

- **`infrastructure`**

Derived from TSOSI: assigned when the entity has received financial support.


- **`library consortium`** and **`funding organisation`**

These are identified manually. `library consortium` is curated manually from TSOSI's list of intermediaries, and `funding organisation` is curated manually from `ror_type` (organisation marked as `funder` and/or `government` in the ROR registry).

Results are stored in `TSOSI-type-entities.csv`, column `tsosi_type`, with values `lib_consort` and `funder` respectively.

- **`company`**

Derived from the ROR registry and its `ror_type`: assigned if `company` is the only value in `ror_type`

- **`other`**

Assigned first to entities in `TSOSI-type-entities.csv` whose `tsosi_type` is not `lib_consort` or `funder`, and second to any TSOSI entity that doesn't match any of the rules above.

## Disclaimer and context

- This work is experimental; it's an ongoing process
- ROR contains types that are not exclusive [ROR type doc](https://ror.readme.io/docs/ror-data-structure#types)
- OpenAlex uses ROR types ([source](https://developers.openalex.org/api-reference/institution-types))
- OCLC contains a list of [participating consortia](https://icolc.net/participating-consortia?page=3)
- Science Europe contains a [list of funders](https://www.scienceeurope.org/about-us/members/)
