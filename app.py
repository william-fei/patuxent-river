import streamlit as st
import pandas as pd
import datetime
import json
import geopandas as gpd
from streamlit.components.v1 import html
from shapely.geometry import Point
import folium
from folium.plugins import TimestampedGeoJson
from streamlit_folium import folium_static

# Define the page selection in the sidebar
page = st.sidebar.selectbox(
    "Navigation", 
    ["💡 About", "🌍 Cesium", "🕊️ Folium", "🗺️ D3"], 
    index=1  # Set the default to load the Cesium page initially
)
if page == "🌍 Cesium":
    # Load the data
    data = pd.read_csv("data.csv")
    
    # Parse the timestamp to datetime format
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    
    # Set up Streamlit layout
    st.title("Migration Viewer")
    st.write("View the migration paths over time originating from Patuxent River Park, Maryland.")
        
    # Prepare data for Cesium
    cesium_data = data[['timestamp', 'location-long', 'location-lat', 'individual-local-identifier']].copy()
    cesium_data['timestamp'] = cesium_data['timestamp'].astype(str)  # Convert to ISO format strings
    
    # Convert the DataFrame to a JSON string
    cesium_data_json = json.dumps(cesium_data.to_dict('records'))
    
    # Define playback speed and play/pause controls in the main area
    playback_speed = st.slider("Playback Speed (1-10)", min_value=1, max_value=10, value=5)
    
    
    col1, col2, col3, col4, col5 = st.columns(5)

    # Define buttons in separate columns
    with col1:
        is_playing = st.button("Play / Pause")
    with col2:
        # Add Toggle Label button in Streamlit to control label visibility    
        show_label = st.button("Toggle Labels")

    # Read HTML content
    with open("cesium_map.html", "r") as file:
        cesium_html = file.read()
    
    # Inject the JSON-encoded data, playback speed, and initial play state into the HTML
    html_code = cesium_html.replace(
        "<!-- INSERT_DATA_HERE -->",
        f"const data = {cesium_data_json}; const playbackSpeed = {playback_speed}; const initialPlayState = {str(is_playing).lower()}; const showLabel = {str(show_label).lower()};"
    )
    
    # Display the HTML content with embedded data
    html(html_code, height=600)

elif page == "💡 About":
    st.title("Demo")

    patuxent_video_file = open("patuxentriverpark.mov", "rb")
    patuxent_video_bytes = patuxent_video_file.read()

    st.write("Me at Patuxent River Park!")
    st.video(patuxent_video_bytes)

    antenna_video_file = open("antenna.mov", "rb")
    antenna_video_bytes = antenna_video_file.read()

    st.write("Antenna Used for Data Collection")
    st.video(antenna_video_bytes)

    st.write("San Francisco-")
    st.write("37.6614238°N 122.4189591°W")
    
elif page == "🗺️ D3":
    st.title("D3 Hexbin Map")
    st.write("This hexbin map shows the distribution of the migration points.")

    # Load the data
    data = pd.read_csv("data.csv")

    # Allow the user to adjust the hexbin radius
    hexbin_radius = st.number_input("Hexbin Radius", min_value=5, max_value=25, value=7)

    # Prepare data for D3
    d3_data = data[['location-long', 'location-lat']].to_dict('records')
    d3_data_json = json.dumps(d3_data)

    # Read HTML content
    with open("d3_hexbin_map.html", "r") as file:
        d3_html = file.read()

    # Inject JSON data and radius into the HTML
    html_code = d3_html.replace("<!-- INSERT_DATA_HERE -->", f"const data = {d3_data_json};")
    html_code = html_code.replace("<!-- INSERT_RADIUS_HERE -->", str(hexbin_radius))

    # Display the HTML content
    html(html_code, height=600)
if page == "🕊️ Folium":
    st.title("Migration Journey")
    st.write("In the Spring (orange), this bird flew all the way up to Nova Scotia to breed!")
    st.write("That fall (blue), the bird head back South, last detected in South Carolina.")
    
    # Load only the data for bird ID 08911
    bird_data = {
        "timestamp": {
            524768: 1650921451000, 531319: 1651977899000, 531355: 1651980458000,
            531393: 1651982008000, 531571: 1651986694000, 531666: 1651990110000,
            531688: 1652058267000, 531702: 1652666977000, 532024: 1652675067000,
            532061: 1652681243000, 532126: 1664518487000, 532204: 1664594283000,
            532293: 1664759774000, 532337: 1664776413000, 532418: 1667949150000,
            532487: 1667952596000, 532505: 1667955637000, 532512: 1667955764000,
            532588: 1667960902000, 532620: 1667961284000, 532671: 1667964766000,
            532734: 1667990785000, 532755: 1667991435000, 532787: 1668036638000,
            532813: 1668037535000
        },
        "location-long": {
            524768: -76.7113, 531319: -75.7221, 531355: -75.1887, 531393: -73.2157,
            531571: -73.977428, 531666: -73.824, 531688: -72.6651, 531702: -70.8084,
            532024: -70.3887, 532061: -69.4164, 532126: -62.9238, 532204: -65.7438,
            532293: -70.5236, 532337: -73.5236, 532418: -75.0852, 532487: -74.3241,
            532505: -74.7179, 532512: -74.7748, 532588: -75.136, 532620: -75.1889,
            532671: -75.61736, 532734: -79.6711, 532755: -79.7267, 532787: -79.8577,
            532813: -79.9966
        },
        "location-lat": {
            524768: 38.7738, 531319: 39.8209, 531355: 39.9522, 531393: 40.6328,
            531571: 40.573745, 531666: 40.6163, 531688: 41.2712, 531702: 42.7804,
            532024: 43.4587, 532061: 43.979, 532126: 44.7284, 532204: 43.4579,
            532293: 43.3492, 532337: 41.553, 532418: 38.7703, 532487: 39.5091,
            532505: 39.0919, 532512: 39.058, 532588: 38.241, 532620: 38.1385,
            532671: 37.57369, 532734: 32.9726, 532755: 32.836, 532787: 32.7603,
            532813: 32.6153
        },
        "individual-local-identifier": {
            524768: "1412-08911", 531319: "1412-08911", 531355: "1412-08911",
            531393: "1412-08911", 531571: "1412-08911", 531666: "1412-08911",
            531688: "1412-08911", 531702: "1412-08911", 532024: "1412-08911",
            532061: "1412-08911", 532126: "1412-08911", 532204: "1412-08911",
            532293: "1412-08911", 532337: "1412-08911", 532418: "1412-08911",
            532487: "1412-08911", 532505: "1412-08911", 532512: "1412-08911",
            532588: "1412-08911", 532620: "1412-08911", 532671: "1412-08911",
            532734: "1412-08911", 532755: "1412-08911", 532787: "1412-08911",
            532813: "1412-08911"
        }
    }

    # Convert dictionary to DataFrame
    bird_df = pd.DataFrame(bird_data)
    bird_df['timestamp'] = pd.to_datetime(bird_df['timestamp'], unit='ms')
    bird_df['season'] = bird_df['timestamp'].apply(lambda x: 'Spring' if x.month < 6 else 'Fall')

    # Convert to GeoDataFrame
    bird_df['geometry'] = bird_df.apply(lambda x: Point((x['location-long'], x['location-lat'])), axis=1)
    gdf = gpd.GeoDataFrame(bird_df, geometry='geometry', crs="EPSG:4326")

    # Map Setup
    m = folium.Map(location=[38, -76], zoom_start=5)

    # Set the starting time for sequential display
    start_time = pd.Timestamp("2022-01-01T00:00:00")

    # Separate the Point features and LineString features into different layers
    point_features = []
    line_features = []

    # Iterate through points to add each one and a connecting line to the next
    for i in range(len(gdf) - 1):  # Loop up to the second-last point
        # Current and next row data
        current_row = gdf.iloc[i]
        next_row = gdf.iloc[i + 1]
        
        # Assign a unique time to each point
        point_time = (start_time + pd.Timedelta(seconds=i)).isoformat()
        color = "coral" if current_row['season'] == "Spring" else "navy"
        
        # Create a Point feature
        point_feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [current_row["location-long"], current_row["location-lat"]],
            },
            "properties": {
                "time": point_time,
                "popup": f"{current_row['individual-local-identifier']}: {current_row['timestamp']}",
                "icon": "circle",
                "iconstyle": {
                    "fillColor": color,
                    "color": color,
                    "radius": 5
                },
            },
        }
        point_features.append(point_feature)

        # Create a LineString feature between the current and the next point
        line_feature = {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [current_row["location-long"], current_row["location-lat"]],
                    [next_row["location-long"], next_row["location-lat"]],
                ],
            },
            "properties": {
                "times": [point_time, (start_time + pd.Timedelta(seconds=i + 1)).isoformat()],
                "style": {
                    "color": color,  # Line color
                    "weight": 3       # Line thickness
                },
            },
        }
        line_features.append(line_feature)

    # Add the last point without a line
    last_row = gdf.iloc[-1]
    last_point_time = (start_time + pd.Timedelta(seconds=len(gdf) - 1)).isoformat()
    last_color = "coral" if last_row['season'] == "Spring" else "navy"
    last_point_feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [last_row["location-long"], last_row["location-lat"]],
        },
        "properties": {
            "time": last_point_time,
            "popup": f"{last_row['individual-local-identifier']}: {last_row['timestamp']}",
            "icon": "circle",
            "iconstyle": {
                "fillColor": last_color,
                "color": last_color,
                "radius": 5
            },
        },
    }
    point_features.append(last_point_feature)

    # Map Setup
    m = folium.Map(location=[38, -76], zoom_start=5)

    # Create separate TimestampedGeoJson layers for points and lines
    timestamped_points = TimestampedGeoJson(
        {"type": "FeatureCollection", "features": point_features},
        period="PT1S",           # One second per frame for points
        add_last_point=True,     # Ensure points stay after appearing
        transition_time=500,     # Transition speed for points
        date_options="ss"

    )

    timestamped_lines = TimestampedGeoJson(
        {"type": "FeatureCollection", "features": line_features},
        period="PT1S",           # One second per frame for lines
        add_last_point=False,    # Lines should not add extra points
        transition_time=500,     # Transition speed for lines
        date_options="ss"
    )

    option = st.radio("Select what to display:", ("Points Only", "Lines Only"))
    
    if option == "Points Only":
        timestamped_points.add_to(m)
    else:
        timestamped_lines.add_to(m)



    # Render map in Streamlit
    folium_static(m)
