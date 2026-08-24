# Database Design

## Project
**Solar & Wind Deployment Intelligence Platform**

## Table 1: Users

| Column | Data Type | Description |
|---|---|---|
| user_id | Integer | Primary Key |
| name | VARCHAR | User name |
| email | VARCHAR | Email address |
| password | VARCHAR | Encrypted password |
| role | VARCHAR | Admin/User |

## Table 2: Projects

| Column | Data Type | Description |
|---|---|---|
| project_id | Integer | Primary Key |
| project_name | VARCHAR | Project name |
| location | VARCHAR | Study location |
| created_date | DATE | Date created |

## Table 3: Datasets

| Column | Data Type | Description |
|---|---|---|
| dataset_id | Integer | Primary Key |
| dataset_name | VARCHAR | Dataset name |
| source | VARCHAR | Data source |
| file_path | TEXT | Storage path |

## Table 4: Analysis Results

| Column | Data Type | Description |
|---|---|---|
| analysis_id | Integer | Primary Key |
| project_id | Integer | Foreign Key |
| solar_score | FLOAT | Solar suitability |
| wind_score | FLOAT | Wind suitability |
| recommendation | TEXT | Final recommendation |

## Relationships
- One User can create multiple Projects.
- One Project can use multiple Datasets.
- One Project can have one or more Analysis Results.

## Conclusion
This database design provides a structured way to store users, projects, datasets, and renewable energy analysis results.
