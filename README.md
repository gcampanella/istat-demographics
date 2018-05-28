# Istat demographics

By Gianluca Campanella (<gianluca@campanella.org>)

[![Creative Commons License](https://i.creativecommons.org/l/by/4.0/80x15.png)](http://creativecommons.org/licenses/by/4.0/)

The Italian National Institute of Statistics ([Istat](https://www.istat.it/en/)) collates demographic data from register offices, and makes them available through its [demographics portal](http://demo.istat.it/index_e.html).

This repository contains a set of scripts to scrape and aggregate monthly time series of births, deaths, and net migration at municipality (*comune*) level, separately for men and women.

The data are made available under a [Creative Commons Attribution 4.0 International (CC BY 4.0)](http://creativecommons.org/licenses/by/4.0/) licence, like the [original data](https://www.istat.it/en/legal-notice).

## Usage

1. Run the [Scrapy](https://scrapy.org) script `scrape.py`:
   ```bash
   scrapy runspider -o istat-demographics-scraped.csv -t csv scrape.py
   ```
1. Run the R script `postprocess.R`:
   ```bash
   R --vanilla < postprocess.R
   ```
   This will produce the output file `istat-demographics.csv.gz`
1. Optionally, delete the file `istat-demographics-scraped.csv`

## Data dictionary

The file `istat-demographics.csv.gz` contains the following variables:

| Name            | Content                              |
|-----------------|--------------------------------------|
| `group`         | NUTS 1 (group of regions) identifier |
| `region`        | NUTS 2 (region) identifier           |
| `province`      | NUTS 3 / LAU 1 (province) identifier |
| `municipality`  | LAU 2 (municipality) identifier      |
| `year`          | Year                                 |
| `month`         | Month (1 = January, 12 = December)   |
| `sex`           | Sex (M = Male, F = Female)           |
| `births`        | Births                               |
| `deaths`        | Deaths                               |
| `net_migration` | Net migration                        |

**Note**: LAU identifiers are updated periodically; see [this page](http://www.istat.it/it/archivio/6789) (in Italian) for more details.

