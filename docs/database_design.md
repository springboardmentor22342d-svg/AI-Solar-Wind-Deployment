# Database Design

## Users

Primary Key

- user_id

Important Columns

- name
- email
- password
- role

--------------------------------

## Projects

Primary Key

- project_id

Important Columns

- project_name
- description
- created_at

--------------------------------

## Sites

Primary Key

- site_id

Important Columns

- latitude
- longitude
- region
- elevation

--------------------------------

## EnvironmentalData

Primary Key

- environmental_id

Important Columns

- solar_irradiance
- wind_speed
- temperature
- rainfall

--------------------------------

## SolarPrediction

Primary Key

- solar_prediction_id

Important Columns

- predicted_energy
- confidence_score

--------------------------------

## WindPrediction

Primary Key

- wind_prediction_id

Important Columns

- predicted_energy
- wind_density

--------------------------------

## SuitabilityScore

Primary Key

- suitability_id

Important Columns

- solar_score
- wind_score
- infrastructure_score
- overall_score

--------------------------------

## Reports

Primary Key

- report_id

Important Columns

- report_name
- generated_date
- report_type