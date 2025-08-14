# PROJECT REQUIREMENTS
A customer has approached us with a requirement to create an application that clearly displays the performance of Steam games across multiple metrics (e.g., player count, review scores, pricing, platform availability), providing them with the ability to both gain insights and present findings.

# PROJECT REQUIREMENTS AS AN EPIC
```
As a customer,
I want to be able to access an application that provides clear, accurate, and up-to-date insights into Steam game performance across multiple metrics,
So that I can make informed business decisions and identify trends in the gaming market.
```

# Epic 1: Extract

```
As a Data Analyst/Scientist,
I want to be able to retrieve raw Steam game data from the SQL database,
So that I can work with it in Python for cleaning, enrichment, and transformation.
```

# Epic 2: Transform
```
As a Data Analyst/Scientist,
I want to be able to work with clean, standardized, enriched, and aggregated Steam game data,
So that it is easier to analyse, ensures consistency, and works for accurate visualizations.
```

# Epic 3: Load
```
As a Data Analyst/Scientist,
I want to save the transformed Steam game data back into the SQL database,
So that it can be accessed by the visualization application and shared with stakeholders.
```

# Epic 4: Visualization
```
As a Data Analyst/Scientist,
I want to view and interact with dashboards in Streamlit displaying Steam game performance metrics,
So that I can quickly explore trends and insights from the transformed data.
```

---

# Epic 1 BREAKDOWN: Extract

```
As a Data Analyst/Scientist,
I want to be able to retrieve raw Steam game data from the SQL database,
So that I can work with it in Python for cleaning, enrichment, and transformation.
```

## USER STORY 1.1

```
As a Data Analyst/Scientist,
I want to connect to the SQL database and query the Steam game dataset,
So that I can pull the latest available data into a Python environment for processing.
```

## USER STORY 1.1 ACCEPTANCE CRITERIA
* Steam game dataset exists in the database with a known schema
* Extraction occurs without errors
* Basic schema checks (column presence, types).
* Row counts match between CSV and DB table.
* Errors in parsing or type mismatches are logged.
* Testing suite exists for this functionality

---

# Epic 2 BREAKDOWN: Transform

```
As a Data Analyst/Scientist,
I want to be able to work with clean, standardized, enriched, and aggregated Steam game data,
So that it is easier to analyse, ensures consistency, and works for accurate visualizations.
```

## USER STORY 2.1

```
As a Data Analyst/Scientist,
I want to clean and standardize the Steam game dataset,
So that all fields are consistent, valid, and analysis-ready.
```

## USER STORY 2.1 ACCEPTANCE CRITERIA
* Missing values handled according to specifications
* Date formats standardized to target format (YYYY-MM-DD).
* Currency values standardized to a single unit (USD).
* Game titles do not contain problematic characters.
* Unit tests verify each cleaning step works.

## USER STORY 2.2

```
As a Data Analyst/Scientist,
I want access to a dataset with derived metrics (e.g., price-to-review ratio, recent player growth),
I additionally want a dataset with metrics pulled in from other contexts and joined with the preexisting data
So that I can perform deeper analysis and identify trends.
```

## USER STORY 2.2 ACCEPTANCE CRITERIA
* Fields created from external sources are added to dataset.
* New derived fields created.
* Aggregations implemented (e.g., average concurrent players per month, revenue estimates).
* Unit tests verify enrichment logic.
* Derived metrics are tolerable to changes in the dataset.


---

# Epic 3 BREAKDOWN: Load
```
As a Data Analyst/Scientist,
I want to save the transformed Steam game data back into the SQL database,
So that it can be accessed by the visualization application and shared with stakeholders.
```

## USER STORY 3.1

```
As a Data Analyst/Scientist,
I want access to a dataset with derived metrics (e.g., price-to-review ratio, recent player growth),
I additionally want a dataset with metrics pulled in from other contexts and joined with the preexisting data
So that I can perform deeper analysis and identify trends.
```

## USER STORY 3.1 ACCEPTANCE CRITERIA
* New table created with a defined schema.
* All transformed data inserted without errors.
* Row count matches output from transformation step.
* Unit tests verify successful table creation and data load.


# Epic 4: Visualization
```
As a customer,
I want to view and interact with dashboards in Streamlit displaying Steam game performance metrics,
So that I can quickly explore trends and insights from the transformed data.
```

## USER STORY 4.1

```
As a customer,
I want to be able to interact with dashboards showing key performance metrics for Steam games,
So that I can visually compare game performance across time, price points, and genres.
```

## USER STORY 4.1 ACCEPTANCE CRITERIA
* Dashboard displays at least 3 visualization types.
* Data freshness disclaimer visible.
* Metrics are consistent between visuals and source DB queries.


## USER STORY 4.2

```
As a customer,
I want filtering capabilities in the Streamlit dashboard,
So that I can explore data subsets without the technical knowledge needed to run queries.
```

## USER STORY 4.2 ACCEPTANCE CRITERIA
* Sidebar filters available for at least: date range, genre, price range, review score range.
* Responsive to user-applied filters (e.g., date range, genre, price range).
* “Reset filters” option.
* No errors when filters return empty datasets (display placeholder).