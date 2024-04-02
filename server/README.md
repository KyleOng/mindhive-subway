# Server

## Table of content
- [Prerequisites](#prerequisites)
- [Setup](#setup)
  -  [1. Set up virtual env and install required Python packages](#setup1)
  -  [2. Install chrome and chrome driver](#setup2)
  -  [3. Define environment variables](#setup3)
  -  [4. Database set up](#setup4)
  -  [5. Database migration](#setup5)
  -  [6. Database role permission for LLM](#setup6)
- [Running the server](#running-server)
- [Running the web scraper](#running-scraper)
- [File structure](#file-structure)

## Prerequisites<a name="prerequisites"></a>
- Python version 3.9.16 and above
- Google Chrome Browser
- Google Chrome Driver
- Google Geocoding API Key
- OpenAI API Key
- PostgreSQL Database

## Setup<a name="setup"></a>
### 1. Set up virtual env and install required Python packages<a name="setup1"></a>

Set up virtual envronment in the `server/` directory and activate it.


```bash
python3 -m venv env
source env/bin/activate
```

After activate the virtual env, install the required Python packages.


```bash
pip install -r requirement.txt
```

### 2. Install chrome and chrome driver<a name="setup2"></a>

Download the Chrome Driver compatible with your Chrome browser version from [here](https://googlechromelabs.github.io/chrome-for-testing/). 

![](<../assets/chrome-driver-download.png>)

After download the chrome driver, you need to make sure that it is able to be executed. 

Extract the executable and ensure it's accessible via your system's PATH.

![](<../assets/chrome-driver-terminal.png>)

### 3. Define environment variables<a name="setup3"></a>

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

### 4. Database set up and defined `SQLALCHEMY_DATABASE_URL`<a name="setup4"></a>

Create a PostgreSQL database locally or on a cloud service.

Update the `SQLALCHEMY_DATABASE_URL` value in the .env file with your database connection details.

### 5. Database migration<a name="setup5"></a>

Run the following command for database migration.

```bash
alembic upgrade head
```

At this point, all tables have been created in your database with the following schema.

<details>
  <summary>👇 Expand for database schema 👇</summary>

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

### 6. Database role permission for LLM and defined `SQLALCHEMY_DATABASE_LLM_URL`<a name="setup6"></a>

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

## Running the server<a name="running-server"></a>

To start the server, use the following command:

```
python api/main.py
```

The server should now be running at http://127.0.0.1:8000.

## Running the web scraper<a name="running-scraper"></a>

To run the web scraper, use the following command:

```bash
python scraper/main.py
```

The script should run the web scrapping process and populate the data inside your database.

![](<../assets/web-scraping-demo.gif>)

## File structure<a name="file-structure"></a>

Files/Folders structure that you might need to know and its purposes.

- |_📁 `alembic`: stores alembic migrations. Initialize using alembic package.
- |_📁 `api`: stores fastapi files for backend framework.
- &nbsp;&nbsp;&nbsp;&nbsp;|_📄  `db.py`: stores sqlalchemy configuration for database connection.
- &nbsp;&nbsp;&nbsp;&nbsp;|_📄  `main.py`: fastapi entry file that stores api routes and functionalities.
- &nbsp;&nbsp;&nbsp;&nbsp;|_📄  `models.py`: stores sqlalchemy database models.
- &nbsp;&nbsp;&nbsp;&nbsp;|_📄  `models.py`: stores pydantic db models schema for data validations.
- |_📁 `lib`: stores 3rd party library utils.
- &nbsp;&nbsp;&nbsp;&nbsp;|_📄  `geocoding.py`: stores google maps geocoding utils, to get coordinates from latitude and longitude.
- &nbsp;&nbsp;&nbsp;&nbsp;|_📄  `llm.py`: stores langchain sql database agent and utils, to interact with sql database using natural language.
- &nbsp;&nbsp;&nbsp;&nbsp;|_📄  `prompts.py`: stores sqlalchemy database models.
- |_📁 `scraper`: stores web scraping.
- &nbsp;&nbsp;&nbsp;&nbsp;|_📄  `chrome_driver.py`: stores chrome driver class.
- &nbsp;&nbsp;&nbsp;&nbsp;|_📄  `main.py`: Entry file for web scrapping and data insertion.
- &nbsp;&nbsp;&nbsp;&nbsp;|_📄  `operating_hour_extractor.py`: stores utils for extracting and parsing operating hours from text.
- |_📄 `alembic.ini`: stores alembic configuration.
- |_📄 `output.txt`: stores output generated from scraping.
- |_📄 `requirement.txt`: strores necessary packages.
- |_📄 `.env.example`: example env file.
