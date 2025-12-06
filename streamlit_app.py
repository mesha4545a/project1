import streamlit as st
import plotly.express as px
import geopandas as gpd
import pandas as pd


df = gpd.read_file("restaurants.geojson")

# render to epsg 4326 
if df.crs is not None:
    df = df.to_crs(epsg=4326)

# to numeric
df["lat"] = pd.to_numeric(df["lat"], errors="coerce")
df["lon"] = pd.to_numeric(df["lon"], errors="coerce")

df = df.dropna(subset=["lat", "lon"])

st.set_page_config(page_title="Restaurants Dashboard", layout="wide")

st.title("Riyadh Restaurants Dashboard")
st.write("### Spatial Data Science Bootcamp - Project 1")
st.write("This dataset contains detailed information on restaurants in Riyadh. Below are some visualizations for spatial and non-spatial analyses.")


# 1 chart -> restaurants_by_district
# ------
restaurants_by_district = (
    df.groupby("NEIGHBORHANAME")
      .size()
      .reset_index(name="count")
      .sort_values("count", ascending=False)
      .head(10)
)

chart1 = px.bar(
    restaurants_by_district,
    x="NEIGHBORHANAME",
    y="count",
    title="Top 10 Districts by Restaurant Count"
)
chart1.update_layout(title={"x": 0.5})
chart1.update_traces(text=restaurants_by_district["count"], textposition="outside")

st.plotly_chart(chart1, use_container_width=True)
# ---------

# 2 chart -> riyadh Restaurants tmap 
# -------
st.subheader('Restaurants Map')

map_center_lat = df["lat"].mean()
map_center_lon = df["lon"].mean()

chart2 = px.scatter_mapbox(
    df,
    lat="lat",
    lon="lon",
    hover_data=["name", "NEIGHBORHANAME"],
    zoom=10,
    height=500
)

chart2.update_layout(
    mapbox_style="open-street-map",
    mapbox_center={"lat": map_center_lat, "lon": map_center_lon}
)

st.plotly_chart(chart2, use_container_width=True)

# ----------


# 3 chart -> Restaurants per District
# ---------
result = (
    df.groupby("NEIGHBORHANAME")
      .size()
      .reset_index(name="count")
      .sort_values("count", ascending=False)
      .head(5)
)

chart3 = px.bar(
    result,
    x="NEIGHBORHANAME",
    y="count",
    title="Restaurants per District"
)

chart3.update_layout(title={"x": 0.5})
chart3.update_traces(text=result["count"], textposition="outside")

st.plotly_chart(chart3, use_container_width=True)
# ------------

# 4 chart -> Restaurant Categories Distributed

#------------
st.subheader("Restaurant Categories by District (Top 20)")

restaurant_categories_distributed = (
    df.groupby(["NEIGHBORHANAME", "categories"])
      .size()
      .reset_index(name="count")
      .sort_values("count", ascending=False)
      .head(20)
)

chart4 = px.bar(
    restaurant_categories_distributed,
    x="NEIGHBORHANAME",
    y="count",
    color="categories",
    barmode="group",
    title="Restaurant Categories Distributed"
)

chart4.update_layout(title={"x": 0.5})
chart4.update_traces(texttemplate='%{y}', textposition='outside')

st.plotly_chart(chart4, use_container_width=True)
#----------------------
