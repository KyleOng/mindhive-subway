# Server

## Setup
### Install necessary python libraries

Set up virtual envronment in the `server/` directory and activate it.

\*Make sure you're using python version 3.9.16 and above.\*

```bash
python3 -m venv env
source env/bin/activate
```

At the current stage, your virtual environment should be activated. Then install all necessary python libraries by running the following command.


```bash
pip install -r requirement.txt
```

### Install chrome and chrome driver

Selenium is used for web scraping and you would need to install chrome driver based your chrome version. You can download the chrome driver from this link [here](https://googlechromelabs.github.io/chrome-for-testing/).

\*Make sure to download **chrome driver** (not chrome) based on your OS and browser version\*

![](<../assets/chrome-driver-download.png>)

After download the chrome driver, you need to make sure that it is able to be executed. 

One way to achieve this is to have an env path where its point to the location of the chrome driver.

![](<../assets/chrome-driver-path.png>)

Then, if the chromedriver is able to be executed from terminal then you are good to go.

![](<../assets/chrome-driver.png>)


### Define environment variables

Create an env variable file `.env` and copy the text from the `.env.example` file, which we will define the env variables.

There are a total of 4 env variables, and you would need to define each of them in order to make the application workable. 

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

We will walk through what to define them in the following sections.

### Database set up and defined `SQLALCHEMY_DATABASE_URL`

Set up a postgresql database locally or in the cloud. After setting up the database, define the env `SQLALCHEMY_DATABASE_URL` with the postgres connection string based on the set up database in the following format `postgresql://<user>:<password>@<host>/<database>`. 

### Database migration

After `alembic` package has been installed from using pip, run the following command for migration.

\*Make sure you define the correct connection string in the ``SQLALCHEMY_DATABASE_URL` env variable\*

```bash
alembic upgrade head
```

At this point, you should see that tables have been created in your database. 

Our database schema is the following:
#### `outlets` Table:
- **Columns**:
  - `id` (Primary Key, Integer): Unique identifier for each outlet.
  - `name` (String): Name of the outlet.
  - `address` (String): Address of the outlet.
  - `waze_link` (String): Link to the outlet's location on Waze.
  - `latitude` (Decimal): Latitude coordinate of the outlet's location.
  - `longitude` (Decimal): Longitude coordinate of the outlet's location.
  - `created_at` (Timestamp): Timestamp indicating when the outlet was created.
  - `updated_at` (Timestamp): Timestamp indicating when the outlet was last updated.
  
#### `operating_hours` Table:
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

### Database role permission for LLM and defined `SQLALCHEMY_DATABASE_LLM_URL`

Langchain SQL Database agent is used to interact with the Postgres Database. However, it is not advisable to use the role that has CREATE, UPDATE and DELETE permission for all tables. Therefore we would need to create one role for it with only SELECT permission for the necessary table.

On how to set up role permission, I will be demonstrate using Dbeaver.

1. Create a new role

![](<../assets/dbeaver-create-new-role.png>)

2. Input user with the value `llm` and password. This will be later used to define the `SQLALCHEMY_DATABASE_LLM_URL` connection string env variable.

![](<../assets/dbeaver-user-password.png>)

3. Select the role. And go to permission and set `SELECT` permission for both `outlets`. Do the same for `operating_hours` table.

![](<../assets/dbeaver-select-outlet.png>)

Finally, define the env `SQLALCHEMY_DATABASE_LLM_URL` with the postgres connection string in the following format `postgresql://llm:<password>@<host>/<database>`. `host` and `database` should be the same, while `username` (llm) and `password` should be different.
