### Q1

~~~sql
WITH findEvent AS ( 
    SELECT title AS word 
    FROM event e, publicationDate d, description d
    WHERE e.dateID = d.dateID AND e.descriptionID = d.descriptionID AND 
          fullDate = "2017-07-28" AND sentiment = "positive" 
),

countWords AS ( 
    SELECT regexp_split_to_table(word, ' ') AS wordToken, COUNT(*) AS total
    FROM findEvent 
    GROUP BY wordToken 
) 
SELECT wordToken, total  
FROM countWords  
VISUALIZE AS wordcloud  

SELECT wordToken, total   
FROM countWords 
VISUALIZE AS barh(wordToken, total)

~~~

### Q2

~~~sql

WITH
ny AS ( 
    SELECT latitude AS latNY, longitude AS longNY
    FROM location 
    WHERE city = "New York"
), 

aroundNY AS ( 
    SELECT city, latitude, longitude, numberNegativeNews, numberPositiveNews, month
    FROM ny, event e, location l, date d 
    WHERE e.locationID = l.locationID AND e.dateID = d.dateID AND
          RANGE(LOCATION, 150, (latNY, longNY), (latitude, longitude)) 
) 

SELECT latitude, longitude, numberNegativeNews 
FROM aroundNY 
CLUSTER latitude, longitude, NumberNegativeNews 
VISUALIZE AS scatter( longitude, latitude, class ) 

~~~

### Queries to be tested (transformed)

~~~sql

WITH findEvent AS ( 
    SELECT title AS word 
    FROM event e, publicationDate d, description d
    WHERE e.dateID = d.dateID AND e.descriptionID = d.descriptionID AND 
          fullDate = "2017-07-28" AND sentiment = "positive" 
), 
SELECT WORDCLOUD(title)  
FROM findEvent
~~~

~~~sql
WITH findEvent AS ( 
    SELECT title AS word 
    FROM event e, publicationDate d, description d
    WHERE e.dateID = d.dateID AND e.descriptionID = d.descriptionID AND 
          fullDate = "2017-07-28" AND sentiment = "positive" 
),

countWords AS ( 
    SELECT regexp_split_to_table(word, ' ') AS wordToken, COUNT(*) AS total
    FROM findEvent 
    GROUP BY wordToken 
) 
SELECT BARH(wordToken, total)   
FROM countWords 
~~~