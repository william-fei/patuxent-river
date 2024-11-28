import streamlit as st
import pandas as pd
import json
import geopandas as gpd
from streamlit.components.v1 import html
from shapely.geometry import Point
import folium
from folium.plugins import TimestampedGeoJson
from streamlit_folium import folium_static
import time

# Define the page selection in the sidebar
page = st.sidebar.selectbox(
    "Navigation", 
    ["💡 About", "🌍 Cesium", "🕊️ Folium", "🐦 PyDeck", "🗺️ D3"], 
    index=1  # Set the default to load the Cesium page initially
)
if page == "🌍 Cesium":
    # Load the data
    data = pd.read_csv("data.csv")
    
    # Parse the timestamp to datetime format
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    
    # Set up Streamlit layout
    st.title("Cesium.js: Migration Timelapse")
    st.write("View the migration paths over five years originating from Patuxent River Park, Maryland.")
        
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

    st.write("San Francisco-")
    st.write("37.6614238°N 122.4189591°W")

elif page == "💡 About":
    st.title("Sora Migration Visualizer")
    st.subheader("Exploring Tools for Geospatial Visualization and Analysis")

    st.write("Every fall, Sora Rails gather by the hundreds at Patuxent River Park. By attaching transmitters that weigh only 1.5 grams, researchers are uncovering the migration routes of these little-studied marsh birds.")

    patuxent_video_file = open("patuxentriverpark.mov", "rb")
    patuxent_video_bytes = patuxent_video_file.read()

    st.write("Me at Patuxent River Park!")
    st.video(patuxent_video_bytes)

    antenna_video_file = open("antenna.mov", "rb")
    antenna_video_bytes = antenna_video_file.read()

    st.write("Antenna Used for Data Collection")
    st.video(antenna_video_bytes)


elif page == "🗺️ D3":
    st.title("D3.js: Hexabin Map")
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
elif page == "🕊️ Folium":
    st.title("Folium: Nova Scotia Journey")
    st.write("In Spring (orange), this bird flew to Nova Scotia to breed.")
    st.write("That fall (blue), the bird head back South. It was last detected in South Carolina.")
    
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

    option = st.radio("Display as:", ("Points", "Line"))
    
    if option == "Points":
        timestamped_points.add_to(m)
    else:
        timestamped_lines.add_to(m)



    # Render map in Streamlit
    folium_static(m)

elif page == "🐦 PyDeck":
    st.title("PyDeck: Lake Erie Journey")
    
    bird_data = {
        "timestamp": {
            2438411: 1651778193000,
            2439372: 1653100556000,
            2439412: 1653102961000,
            2439435: 1653115618000,
            2439458: 1653116773000,
            2439490: 1653117840000,
            2439511: 1653121583000,
            2439527: 1653272247000,
            2439535: 1653272896000,
            2439599: 1653280035000,
            2439632: 1653281800000,
            2439732: 1662529356000,
            2439752: 1662529696000,
            2439790: 1662534148000,
            2439861: 1662535292000,
            2439896: 1665965629000,
            2439919: 1665968800000,
            2439970: 1665982505000,
            2439995: 1665983038000,
            2439998: 1665983077000,
            2440016: 1665983291000,
            2440075: 1665989643000,
            2440154: 1665990652000,
            2440237: 1665995288000,
            2440260: 1665996520000,
            2440323: 1665997606000,
            2440355: 1666000031000
        },
        "location-long": {
            2438411: -76.7113,
            2439372: -77.6258,
            2439412: -77.9972,
            2439435: -79.4567,
            2439458: -79.7017,
            2439490: -79.6467,
            2439511: -79.8761,
            2439527: -80.012,
            2439535: -80.0899,
            2439599: -80.0943,
            2439632: -80.2237,
            2439732: -79.503,
            2439752: -79.5235,
            2439790: -79.5501,
            2439861: -79.4735,
            2439896: -79.1849,
            2439919: -78.404,
            2439970: -76.9409,
            2439995: -76.6077,
            2439998: -76.6825,
            2440016: -76.7224,
            2440075: -75.7205,
            2440154: -76.3845,
            2440237: -75.8221,
            2440260: -76.0077,
            2440323: -76.3551,
            2440355: -75.9894
        },
        "location-lat": {
            2438411: 38.7738,
            2439372: 39.4483,
            2439412: 39.7104,
            2439435: 41.8787,
            2439458: 41.997,
            2439490: 42.3087,
            2439511: 42.9776,
            2439527: 43.4429,
            2439535: 43.5089,
            2439599: 44.0461,
            2439632: 44.2884,
            2439732: 44.9404,
            2439752: 44.945,
            2439790: 44.3849,
            2439861: 44.2803,
            2439896: 43.8191,
            2439919: 43.1127,
            2439970: 40.5274,
            2439995: 40.476,
            2439998: 40.4045,
            2440016: 40.4263,
            2440075: 38.8015,
            2440154: 38.7569,
            2440237: 37.5887,
            2440260: 37.3222,
            2440323: 37.0987,
            2440355: 36.527
        },
        "individual-local-identifier": {
            2438411: "1412-80214",
            2439372: "1412-80214",
            2439412: "1412-80214",
            2439435: "1412-80214",
            2439458: "1412-80214",
            2439490: "1412-80214",
            2439511: "1412-80214",
            2439527: "1412-80214",
            2439535: "1412-80214",
            2439599: "1412-80214",
            2439632: "1412-80214",
            2439732: "1412-80214",
            2439752: "1412-80214",
            2439790: "1412-80214",
            2439861: "1412-80214",
            2439896: "1412-80214",
            2439919: "1412-80214",
            2439970: "1412-80214",
            2439995: "1412-80214",
            2439998: "1412-80214",
            2440016: "1412-80214",
            2440075: "1412-80214",
            2440154: "1412-80214",
            2440237: "1412-80214",
            2440260: "1412-80214",
            2440323: "1412-80214",
            2440355: "1412-80214"
        }
    }


    # Convert dictionary to DataFrame
    bird_df = pd.DataFrame(bird_data)
    bird_df['timestamp'] = pd.to_datetime(bird_df['timestamp'], unit='ms')

    tab1, tab2, tab3 = st.tabs(["Static Points", "Static Lines", "Cumulative Distance"])

    # Static map
    with tab1:
        st.write("### Bird's Recorded Migration Points (Static)")
        st.map(bird_df.rename(columns={"location-lat": "lat", "location-long": "lon"}))

    # Animated map
    with tab2:
        st.write("### Migration Path, with Sample Altitude")

        # Generate a density-based heatmap to show areas of high bird movement
        import pydeck as pdk
        
        # Visualizing migration altitude over time in a 3D path
        bird_df['altitude'] = bird_df.index % 1000 + 100  # Sample altitude, replace with real data if available
        path_layer = pdk.Layer(
            "PathLayer",
            data=[{
                "path": bird_df[["location-long", "location-lat", "altitude"]].values.tolist(),
                "timestamp": bird_df["timestamp"].iloc[0]
            }],
            get_path="path",
            get_width=10,
            width_min_pixels=3,
            get_color=[200, 30, 0, 160],
            elevation_scale=4,
            extruded=True
        )
        
        view_state = pdk.ViewState(latitude=bird_df["location-lat"].mean(),
                                longitude=bird_df["location-long"].mean(),
                                zoom=5,
                                pitch=45)
        
        st.pydeck_chart(pdk.Deck(layers=[path_layer], initial_view_state=view_state))
    
    with tab3:
        st.write("### Total Distance Travelled")
            
        # Shifted columns to calculate distance between consecutive points
        bird_df['shifted_lat'] = bird_df['location-lat'].shift(1)
        bird_df['shifted_long'] = bird_df['location-long'].shift(1)
        
        # Define a function to calculate distance between two latitude/longitude points using Haversine formula
        def haversine(lat1, lon1, lat2, lon2):
            import numpy as np
            R = 6371  # Earth radius in km
            lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
            c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
            return R * c
        
        # Calculate distance between each consecutive point and accumulate the total distance traveled by date
        bird_df['distance_km'] = haversine(
            bird_df['location-lat'], bird_df['location-long'], bird_df['shifted_lat'], bird_df['shifted_long']
        ).fillna(0)
        bird_df['cumulative_distance_km'] = bird_df['distance_km'].cumsum()

        # Plot cumulative distance traveled by each date
        bird_df['date'] = bird_df['timestamp'].dt.date  # Extract date only for daily tracking
        daily_cumulative_distance = bird_df.groupby('date')['cumulative_distance_km'].max().reset_index()

        # Display line chart
        st.line_chart(daily_cumulative_distance.set_index('date'), height=300)
        st.write("#### Final Cumulative Distance:", daily_cumulative_distance['cumulative_distance_km'].iloc[-1].round(2), "km")
