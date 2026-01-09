import streamlit as st
import requests
import urllib.parse

st.set_page_config(
    page_title="Smart Travel Assistant",
    page_icon="🌍",
    layout="wide"
)

# ---------- FUNCTIONS ----------

def get_places(query):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": query,
        "format": "json",
        "extratags": 1,
        "limit": 6
    }
    headers = {"User-Agent": "Travel-App"}
    return requests.get(url, params=params, headers=headers).json()

def safe_tags(item):
    return item["extratags"] if isinstance(item.get("extratags"), dict) else {}

def get_image(name):
    wiki = "https://en.wikipedia.org/api/rest_v1/page/summary/" + name.replace(" ", "%20")
    r = requests.get(wiki)
    if r.status_code == 200:
        return r.json().get(
            "thumbnail", {}
        ).get("source", "https://via.placeholder.com/400x250?text=No+Image")
    return "https://via.placeholder.com/400x250?text=No+Image"

# ---------- HEADER ----------

st.markdown("## 🌍 Smart Travel Assistant")
st.write("Booking-style travel UI using FREE APIs")

location = st.text_input("📍 Enter Location (eg: Ooty, Chennai)")

tabs = st.tabs([
    "🗺️ Route & Traffic",
    "🏨 Room Stays",
    "🚗 Car Rentals",
    "🏍️ Bike Rentals"
])

# ---------- ROUTE TAB ----------
with tabs[0]:
    start = st.text_input("🚩 Start Location")
    if st.button("Show Route"):
        if start and location:
            s = urllib.parse.quote(start)
            d = urllib.parse.quote(location)
            url = (
                f"https://www.google.com/maps/dir/?api=1"
                f"&origin={s}&destination={d}&travelmode=driving"
            )
            st.markdown(f"👉 [Open Google Maps Route]({url})")
            st.info("Live traffic & travel time shown in Google Maps")

# ---------- ROOM STAYS ----------
with tabs[1]:
    if location:
        hotels = get_places(f"hotels in {location}")
        cols = st.columns(3)

        for i, h in enumerate(hotels):
            tags = safe_tags(h)
            with cols[i % 3]:
                st.image(get_image(h["display_name"]), use_column_width=True)
                st.markdown(f"### 🏨 {h['display_name'].split(',')[0]}")
                st.write("₹2500 / night")
                st.write("Comfortable stay with basic amenities.")
                st.write(f"📞 {tags.get('phone','Not available')}")
                if tags.get("website"):
                    st.markdown(f"🌐 {tags['website']}")
                st.markdown(
                    f"📍 [Location](https://www.openstreetmap.org/{h['osm_type']}/{h['osm_id']})"
                )

# ---------- CAR RENTALS ----------
with tabs[2]:
    if location:
        cars = get_places(f"car rental in {location}")
        cols = st.columns(3)

        for i, c in enumerate(cars):
            tags = safe_tags(c)
            with cols[i % 3]:
                st.image(get_image(c["display_name"]), use_column_width=True)
                st.markdown(f"### 🚗 {c['display_name'].split(',')[0]}")
                st.write("Reliable car rental service.")
                st.write(f"📞 {tags.get('phone','Not available')}")
                if tags.get("website"):
                    st.markdown(f"🌐 {tags['website']}")
                st.markdown(
                    f"📍 [Location](https://www.openstreetmap.org/{c['osm_type']}/{c['osm_id']})"
                )

# ---------- BIKE RENTALS ----------
with tabs[3]:
    if location:
        bikes = get_places(f"bike rental in {location}")
        cols = st.columns(3)

        for i, b in enumerate(bikes):
            tags = safe_tags(b)
            with cols[i % 3]:
                st.image(get_image(b["display_name"]), use_column_width=True)
                st.markdown(f"### 🏍️ {b['display_name'].split(',')[0]}")
                st.write("Affordable bikes for travel.")
                st.write(f"📞 {tags.get('phone','Not available')}")
                if tags.get("website"):
                    st.markdown(f"🌐 {tags['website']}")
                st.markdown(
                    f"📍 [Location](https://www.openstreetmap.org/{b['osm_type']}/{b['osm_id']})"
  )
