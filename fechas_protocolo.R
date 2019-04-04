library(dplyr)
library(rvest)
library(stringr)

url <- "https://m.20minutos.es/minuteca/protocolo-contaminacion-madrid/"

news <- read_html(url) %>%
  html_nodes("h2, h4") %>%
  html_text() %>%
  str_replace_all("[^[:alnum:]]", " ") %>%
  str_trim(side = 'both')

dates <- read_html(url) %>%
  html_nodes(".media-signature") %>%
  html_text() %>%
  str_extract("\\d{2}.\\d{2}.\\d{4}")

df <- tibble(news = news, date = dates)
