library(dplyr)
library(RMySQL)

cred <- jsonlite::fromJSON('mysql.json')
db <- dbConnect(RMySQL::MySQL(), 
                host = cred$airquality$host,
                user = cred$airquality$user,
                port = as.numeric(cred$airquality$port),
                password = cred$airquality$password,
                dbname = cred$airquality$db)

query <- dbSendQuery(db, "SELECT * FROM airQuality")
df <- dbFetch(query)

dbDisconnect(db)
