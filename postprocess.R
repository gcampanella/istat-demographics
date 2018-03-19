#!/usr/bin/env Rscript

library(tidyverse)

mapping <- read_csv("mapping.txt")

demographics <- read_csv("istat-demographics-scraped.csv")

demographics <- demographics %>%
                group_by(province, municipality, year, month, sex) %>%
                summarize_at(vars(births, deaths, net_migration), sum) %>%
                ungroup() %>%
                inner_join(mapping, by = "province") %>%
                select(
                    group, region, province, municipality,
                    year, month,
                    sex,
                    births, deaths, net_migration
                ) %>%
                arrange(group, region, province, municipality)

write_csv(demographics, "istat-demographics.csv.gz")

