# TSOSI types for entities

## Goal

From all the TSOSI entities, try to identify the following exclusive types: `infrastructure`, `library consortia`, `funding organisation`, `company`, and `other`.

## Repository logic

`TSOSI-type-entities.csv` contains the classifications that have been done ergarding lib. consort. and funding org.

Files whose names start with a date are to be used manually to deduce the type.


## TSOSI types and matching

* from _ror_type_

`company` if `ror_type` contains **only** that value

* from _TSOSI-type-entities.csv_ and column _tsosi_type_: 

`library consortia`, are marked `lib_consort`
`funding organisation`, are marked `funder`

* from TSOSI entites

`infrastructure` are the one that received support

`other` are all the remaining entities. 


## TSOSI type identification process

If a new data provider that is an infrastructure or consortium is included, run the code to identify library consortia and funders.

## Disclaimer and context

- This work is experimental; it's an ongoing process
- ROR contains types that are not exclusive [ROR type doc](https://ror.readme.io/docs/ror-data-structure#types)
- OpenAlex uses only ROR types ([source](https://developers.openalex.org/api-reference/institution-types))
- OCLC contains a list of [participating consortia](https://icolc.net/participating-consortia?page=3)
- Science Europe contains a [list of funders](https://www.scienceeurope.org/about-us/members/)
