# Mindhive Subway

A web application designed to visualize Subway outlets in Kuala Lumpur, Malaysia. Built using React and FastAPI.

Features include an AI-powered query system that enables users to inquire about the locations and operating hours of Subway outlets.

Data retrieved from the Subway website, processed, and stored in a database.

### Demo video

![image](/assets/demo.gif)
\*Red pin - default, Blue pin - selected, Green pin - highlighted\*

*Please refer to the `/client` and `/server` directories for instructions on installation and execution*

## Tech stacks

**Backend**:
- Python *(version 3.9.5)*
- FastAPI - Backend framework
- SqlAlchemy - PostgreSQL ORM
- Selenium - Web Scraping
- Langchain Python SDK - SQL Database Agent (Postgres Dialect)
- Google Geocoding - Latitude Longitude API
- etc

**Frontend**:
- Typescript with Node JS *(version 20.5.2)*
- React - Frontend framework
- TailwindCSS - Styling
- Zustant - State managament
- React Google Maps `@vis.gl/react-google-maps` - Google Map
- etc

**Deployment**:
- AWS RDS - Postgres Database
- AWS EC2 - Code Runtime