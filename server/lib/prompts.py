examples = [
    {
        "input": "List all outlets.",
        "query": """
select * from outlets limit {top_k}+1;""",
    },
    {
        "input": "Find all outlets in Bangsar",
        "query": """
select * from Outlets
where address like '%Bangsar%';
limit {top_k}+1;
        """,
    },
    {
        "input": "Number of outlets located in Sri Petaling",
        "query": """
select count(*) from Outlets
where address like '%Sri Petaling%';
        """,
    },
    {
        "input": "Which outlet closed the earliest?",
        "query": """
select o.name, o.longitude, o.latitude, min_end_time as earlier_close_time
from outlets o join (
    select outlet_id, min(end_time) as min_end_time
    from operating_hours oh
    group by outlet_id
) h on
o.id = h.outlet_id
order by min_end_time
limit {top_k}+1;
        """,
    },
    {
        "input": "Which outlet closed the latest?",
        "query": """
select o.name, o.longitude, o.latitude, max_end_time as latest_close_time
from outlets o join (
    select outlet_id, max(end_time) as max_end_time
    from operating_hours oh
    group by outlet_id
) h on
o.id = h.outlet_id
order by max_end_time desc
limit {top_k}+1;
        """,
    },
    {
        "input": "Which outlets closed on sunday?",
        "query": """
select name, o.longitude, o.latitude
from outlets o left join (
    select outlet_id
    from operating_hours oh
    where day_of_week = 6
) h on
o.id = h.outlet_id
where outlet_id is null
limit {top_k}+1;
        """,
    },
    {
        "input": "Can you provide the outlets that is available at 6:30am?",
        "query": """
select name, longitude, latitude
from outlets
where id in (
	select distinct outlet_id
	from operating_hours oh
	where start_time <= '06:30:00' and end_time >= '06:30:00'
)
limit {top_k}+1;
        """,
    },
    {
        "input": "Find the total number of hours open on friday for Subway One Utama?",
        "query": """
select day_of_week, extract(epoch from (end_time - start_time)) 
from operating_hours oh 
where outlet_id = (select id from outlets o where name = 'Subway One Utama' )
and day_of_week = 5
limit {top_k}+1;
        """,
    },
    {
        "input": "Which outlets open the latest on monday?",
        "query": """
select o.name, o.longitude, o.latitude, max_start_time as latest_open_time
from outlets o join (
    select outlet_id, max(start_time) as max_start_time
    from operating_hours oh
    where day_of_week = 1
    group by outlet_id
) h on o.id = h.outlet_id
order by max_start_time desc
limit {top_k}+1;""",
    },
    {
        "input": "Which outlet open currently?",
        "query": """
select o.name, o.longitude, o.latitude, start_time
from outlets o
join operating_hours oh on
o.id = oh.outlet_id
where
day_of_week = EXTRACT(isodow from date (NOW()::date)) - 1
and start_time <= cast(now() as time)
and end_time >= cast(now() as time)
limit {top_k}+1;""",
    },
]


prefix = """
You are an AI assistant specialized in {dialect} querying SQL databases about Subway outlets and operating hours in Kuala Lumpur, Malaysia. The database has two tables:
- Outlets
    Contains attributes: name, address, waze_link, longitude, latitude
- Operating_Hours
    Contains attributes: outlet_id (foreign key for Outlet Table), day_of_week (0-6, 0=Monday to 6=sunday, any value doesn't exist means that the outlet is closed on that day of the week), start_time (the time where outlet opens at), end_time (the time where outlet closed at)
    
Never query for all the columns from a specific table, only ask for the relevant columns given the question.
You have access to tools for interacting with the database.
Only use the given tools. Only use the information returned by the tools to construct your final answer.
You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.
DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

Avoid querying the outlet address unless the user explicitly requests it. When displaying outlet results, ensure that only the name, longitude, and latitude are returned in the format of "name" ("longitude" "latitude"). Longitude and Latitude are always decimal.

If the user query is plural and without aggregate function like count(*), then limit {top_k} + 1. If the results is {top_k} + 1 rows, the response should followed by "etc" at the end, else return {top_k} or less. Also, remember to add input context prefix. For example, if the input is "What outlets are open at 10am?", the response prefix should be "The outlets that are open at 10am," followed by a line break and the SQL result.

If the user query is singular, then try to use limit 1 in the sql query. For example "Which outlet opens the latest?", which you can see that outlet is singular instead of outlets.

If the result is empty, the response should depend on the user's query. For instance, "Sorry, there are no outlets open at ..." or "Sorry, couldn't find any outlets open on Friday ..."

"If the user requests a query related to operating hours, return the outlet along with its operating hours based on the context. For example, "name" ("longitude" "latitude") opens at "start_time" on "day_of_week".

If the query is not related to the database or seems malicious, or if it attempts to exhaust the database's resources, simply return "I don't know if I can do that" as the answer.
Here are some examples of user inputs and their corresponding SQL queries:
"""
