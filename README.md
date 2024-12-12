## View the app: [patuxent.streamlit.app](https://patuxent.streamlit.app/)

## Cesium.js

I used Cesium.js to create a 3D migratory timelapse of bird paths. I converted the dataset into a CZML format for compatibility with Cesium’s entity-based rendering. I implemented polylines to represent bird paths and used the `viewer.clock` module for time-based animations. I configured 3D, 2.5D, and 2D views, with zoom and drag functionality, and togglable location labels.

## Folium.js

I used the Folium.js library, with `Leaflet.js` maps on the frontend and `GeoPandas` for the data manipulation. I used the `TimestampedGeoJSON` Folium plugin to animate migration paths over time. I differentiated spring migration (orange) from fall migration (navy). I also provided configurations for changing the animation FPS, a slider to view individual frames, and viewing the data as points vs. lines.

## DeckGL

Using PyDeck (a Python wrapper for DeckGL), I created three visualizations: First, a static point map to display the bird’s locations using PyDeck’s `ScatterplotLayer`. Second, a `PathLayer` and `Carto` to render migration paths in 3D with sample altitude data to simulate elevation. Finally, I calculated the cumulative distance traveled by the bird using the Haversine formula and visualized the results with a line graph showing daily and overall migration distance.

## D3.js

I used D3.js to create a hexbin map displaying the density of migration points. I normalized latitude and longitude data to fit within the dimensions of an SVG container using D3’s `scaleLinear`. I generated a hexagonal grid with `d3.hexbin()` and mapped point density to color intensity using `d3.scaleSequential`. I rendered hexagons as `path` elements with density-dependent opacity and borders. I provided options to adjust the hexbin radius, which dynamically updates the visualization.
