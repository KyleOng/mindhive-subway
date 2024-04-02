# Server

## Prerequisite
- Python version 3.9.16
- Google Chrome browser
- Google Chrome driver
- Google Geocoding API Key
- OpenAI API Key

## Setup
### 1. Set up virtual env and install required Python packages

Set up virtual envronment in the `server/` directory and activate it.


```bash
python3 -m venv env
source env/bin/activate
```

After activate the virtual env, install the required Python packages.


```bash
pip install -r requirement.txt
```

### 2. Install chrome and chrome driver

Download the Chrome Driver compatible with your Chrome browser version from [here](https://googlechromelabs.github.io/chrome-for-testing/). 

![](<../assets/chrome-driver-download.png>)

After download the chrome driver, you need to make sure that it is able to be executed. 

Extract the executable and ensure it's accessible via your system's PATH.

![](<../assets/chrome-driver-terminal.png>)

### 3. Define environment variables

Create a `.env` file and copy the text from the `.env.example` file, which we will define the env variables as below. 

```env
SQLALCHEMY_DATABASE_URL= # for crud
SQLALCHEMY_DATABASE_LLM_URL= # for llm with user role only select (read-only)
GOOGLE_GEOCODING_API_KEY= # for google geocoding
OPENAI_API_KEY= # for openai
```
 - `SQLALCHEMY_DATABASE_URL`: Postgres connection for CRUD
 - `SQLALCHEMY_DATABASE_LLM_URL`: Postgres connection for langchain sql agent (difference between the 1st one is that it only has SELECT permission)
- `GOOGLE_GEOCODING_API_KEY` = Google Geocoding API key
- `OPENAI_API_KEY` = Open API key

We will walk through what to define `SQLALCHEMY_DATABASE_URL` and `SQLALCHEMY_DATABASE_LLM_URL` in the following sections.

### 4. Database set up and defined `SQLALCHEMY_DATABASE_URL`

Create a PostgreSQL database locally or on a cloud service.

Update the `SQLALCHEMY_DATABASE_URL` value in the .env file with your database connection details.

### 5. Database migration

Run the following command for database migration.

```bash
alembic upgrade head
```

At this point, all tables have been created in your database with the following schema.

<details>
  <summary>Database schema</summary>

#### `Outlets` Table:
- **Columns**:
  - `id` (Primary Key, Integer): Unique identifier for each outlet.
  - `name` (String): Name of the outlet.
  - `address` (String): Address of the outlet.
  - `waze_link` (String): Link to the outlet's location on Waze.
  - `latitude` (Decimal): Latitude coordinate of the outlet's location.
  - `longitude` (Decimal): Longitude coordinate of the outlet's location.
  - `created_at` (Timestamp): Timestamp indicating when the outlet was created.
  - `updated_at` (Timestamp): Timestamp indicating when the outlet was last updated.
  
#### `Operating_hours` Table:
- **Columns**:
  - `id` (Primary Key, Integer): Unique identifier for each operating hour entry.
  - `outlet_id` (Foreign Key, Integer): Identifier linking the operating hour entry to its corresponding outlet.
  - `day_of_week` (Integer): Integer representing the day of the week (0 for Monday, 1 for Tuesday, etc.).
  - `start_time` (Time): Start time of operation for the outlet on the given day.
  - `end_time` (Time): End time of operation for the outlet on the given day.
  - `created_at` (Timestamp): Timestamp indicating when the operating hour entry was created.
  - `updated_at` (Timestamp): Timestamp indicating when the operating hour entry was last updated.
  
- **Constraints**:
  - `day_of_week` Constraint: Ensures that the `day_of_week` column value is between 0 and 6 (inclusive), representing valid days of the week (Monday to Sunday).

#### Relationship:
- The `outlets` table has a one-to-many relationship with the `operating_hours` table, as an outlet can have multiple operating hour entries.

</details>

### 6. Database role permission for LLM and defined `SQLALCHEMY_DATABASE_LLM_URL`

Langchain SQL Database agent is used to interact with the Postgres Database. 

However, it is not advisable to use the role that has CREATE, UPDATE and DELETE permission for all tables. Therefore we would need to create one role for it with only SELECT permission for the necessary table.

On how to set up role permission, the following demonstrations use Dbeaver.

1. Create a new role

![](<../assets/dbeaver-create-new-role.png>)

2. Input user with the value `llm` and password. This will be later used to define the `SQLALCHEMY_DATABASE_LLM_URL` connection string env variable.

![](<../assets/dbeaver-user-password.png>)

3. Select the role. And go to permission and set `SELECT` permission for both `outlets`. Do the same for `operating_hours` table.

![](<../assets/dbeaver-select-outlet.png>)

Finally, define the env `SQLALCHEMY_DATABASE_LLM_URL` with the postgres connection string in the following format `postgresql://llm:<password>@<host>/<database>`. `host` and `database` should be the same, while `username` (llm) and `password` should be different.

## Running the server

To start the server, use the following command:

```
python api/main.py
```

The server should now be running at http://127.0.0.1:8000.

## Running the web scraper

To run the web scraper, use the following command:

```bash
python scraper/main.py
```

The script should run the web scrapping process and populate the data inside your database.