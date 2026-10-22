# Day 3 Cleaning Log

- Started with 6433 taxi rows.
- Removed 6 rides with missing timestamps or drop-off time not after pickup; these rides cannot provide a reliable trip duration.
- Filled 43 missing payment values with 'Unknown' rather than guessing how the ride was paid.
- Filled 22 missing values in pickup_zone with 'Unknown'; the true location cannot be safely inferred from this table alone.
- Filled 39 missing values in dropoff_zone with 'Unknown'; the true location cannot be safely inferred from this table alone.
- Filled 22 missing values in pickup_borough with 'Unknown'; the true location cannot be safely inferred from this table alone.
- Filled 39 missing values in dropoff_borough with 'Unknown'; the true location cannot be safely inferred from this table alone.
- Kept 45 rides with zero distance; a zero value may represent a very short trip or a data issue, so it should be investigated rather than automatically deleted.
- Kept 96 rides with zero passengers; the value may be a recording issue, but there is not enough evidence here to replace or delete it.
- Merged pickup service zone using a left join on borough and zone: 6427 rows before and 6427 rows after. A left join preserves all ride rows; the row count should stay the same.
- Found 22 pickup rows with no matching lookup entry; unmatched values are kept and recorded as Unknown rather than dropping rides.
- Filled 22 missing pickup service_zone values with 'Unknown' because no matching service-zone value was available.
- So what: filling missing labels with 'Unknown' keeps rides available for analysis without pretending to know missing details.
- So what: the left merge preserves the ride records; unmatched pickup locations are visible instead of silently disappearing.
- So what: airport revenue share is calculated from the cleaned data and the added pickup service-zone label.
