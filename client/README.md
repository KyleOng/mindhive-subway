# Client

Built using:
- Typescript with Node JS *(version 20.5.2)*
- React - Frontend framework
- TailwindCSS - Styling
- Zustant - State managament
- React Google Maps `@vis.gl/react-google-maps` - Google Map
- etc

## Table of content
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Running the client](#running-client)
- [File structure](#file-structure)

## Prerequisites<a name="prerequisites"></a>
- Typescript with Node JS version 20.5.2 and above
- Google Geocoding API Key
- Google Map API (Set up Google Cloud Map Management)
- Server running (refer to `../server`)

## Setup<a name="setup"></a>

Install node modules using the command below

```bash
npm i
```

Define the environment variables as below.

```env
VITE_GOOGLE_GEOCODING_API_KEY=
VITE_API_URL = 
VITE_GOOGLE_MAP_ID = 
```
- `VITE_GOOGLE_GEOCODING_API_KEY`= Google Geocoding API Key for displaying Google Map.
- `VITE_API_URL` = Server api url, if running in local then the value should be like `http://127.0.0.1:8000`.
- `VITE_GOOGLE_MAP_ID` = Google Map API set up in Google Cloud Map Management Dashboard.

## Running the client<a name="running-client"></a>

To start the client, use the following command:

```
npm run dev
```

The server should now be running at http://127.0.0.1:5173.

## File structure<a name="file-structure"></a>

Files/Folders structure that you might need to know and its purposes.

All the codes are stored in the `./client/src` directory.

- |_📁 `components`: stores React client components
- &nbsp;&nbsp;&nbsp;&nbsp;|_📄 `info-window.tsx`: React Google Maps info window wrapper component.
- &nbsp;&nbsp;&nbsp;&nbsp;|_📄 `marker.tsx`: React Google Maps marker component.
- &nbsp;&nbsp;&nbsp;&nbsp;|_📄 `prompt-input.tsx`: input bar for AI agent prompt.
- &nbsp;&nbsp;&nbsp;&nbsp;|_📄 `qna.tsx`: stores each response query from AI agent.
- &nbsp;&nbsp;&nbsp;&nbsp;|_📄 `qnas.tsx`: storse list of qna.
- &nbsp;&nbsp;&nbsp;&nbsp;|_📄 `select.tsx`: select input bar for outlet selection.
- |_📁 `interfaces`: stores Typescript interfaces.
- |_📁 `lib`: stores 3rd party lib utils.
- |_📁 `store`: stores zustand stores.
- &nbsp;&nbsp;&nbsp;&nbsp;|_📄 `highlighted-markers.ts`: stores state for which markers should be highlighted.
- &nbsp;&nbsp;&nbsp;&nbsp;|_📄 `info-window`: stores state for which info window should be opened.
- |_📄 `App.tsx`: root app component.
- |_📄 `index.css`: css styling.
- |_📄 `main.tsx`: entry file for running React app.

