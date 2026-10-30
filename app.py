import streamlit as st
import sys
from pathlib import Path

# Make the project package available
sys.path.insert(0, str(Path(__file__).parent))

from carbon_coach.tools import (
    calculate_electricity_emissions,
    calculate_transport_emissions
)
from carbon_coach.food_factors import calculate_food_emissions
from carbon_coach.waste_factors import calculate_waste_emissions


st.set_page_config(
    page_title="Carbon Coach",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 Carbon Coach")
st.subheader("Understand your carbon footprint. Build a greener future.")

st.write(
    "Track everyday activities and estimate their environmental impact "
    "using documented emission factors."
)

# Session memory
if "activities" not in st.session_state:
    st.session_state.activities = []

st.divider()

st.header("📊 Your Carbon Dashboard")

total = sum(
    item["emissions"]
    for item in st.session_state.activities
)

col1, col2 = st.columns(2)

with col1:
    st.metric("Logged activities", len(st.session_state.activities))

with col2:
    st.metric("Recorded emissions", f"{total:.3f} kg (mixed units)")

st.caption(
    "Electricity is recorded in kg CO₂; other categories use kg CO₂e. "
    "This mixed-unit figure is not a scientifically comparable total."
)

st.divider()

st.header("➕ Calculate a new activity")

category = st.selectbox(
    "Choose an activity",
    ["Electricity", "Transportation", "Food", "Waste"]
)

if category == "Electricity":

    units = st.number_input(
        "Electricity consumed (kWh)",
        min_value=0.0,
        value=100.0
    )

    if st.button("Calculate electricity emissions"):
        result = calculate_electricity_emissions(units)

        if "error" not in result:
            emissions = result["emissions_kg_co2"]
            st.success(f"Estimated emissions: {emissions} kg CO₂")
            st.write("Emission factor:", result["emission_factor"])
            st.write("Source:", result["source"])

            st.session_state.activities.append({
                "category": "Electricity",
                "description": f"{units} kWh",
                "emissions": emissions,
                "unit": "kg CO₂"
            })
        else:
            st.error(result["error"])

elif category == "Transportation":

    mode = st.selectbox(
        "Transport mode",
        ["motorcycle", "petrol_car", "diesel_bus"]
    )

    distance = st.number_input(
        "Distance travelled (km)",
        min_value=0.0,
        value=10.0
    )

    if st.button("Calculate transport emissions"):
        result = calculate_transport_emissions(distance, mode)

        if "error" not in result:
            emissions = result["emissions_kg_co2e"]
            st.success(f"Estimated emissions: {emissions} kg CO₂e")
            st.write("Emission factor:", result[
                "emission_factor_kg_co2e_per_passenger_km"
            ])
            st.write("Scope:", result["scope"])
            st.write("Source:", result["source"])

            st.session_state.activities.append({
                "category": "Transportation",
                "description": f"{distance} km by {mode}",
                "emissions": emissions,
                "unit": "kg CO₂e"
            })
        else:
            st.error(result["error"])

elif category == "Food":

    food = st.selectbox(
        "Food item",
        [
            "rice", "wheat", "chicken", "beef", "pork",
            "eggs", "milk", "cheese", "tofu", "lentils",
            "beans", "potatoes", "tomatoes", "bananas",
            "apples", "peas", "onions"
        ]
    )

    quantity = st.number_input(
        "Food quantity (kg)",
        min_value=0.0,
        value=0.5
    )

    if st.button("Calculate food emissions"):
        result = calculate_food_emissions(food, quantity)

        if "error" not in result:
            emissions = result["emissions_kg_co2e"]
            st.success(f"Estimated emissions: {emissions} kg CO₂e")
            st.write("Emission factor:", result[
                "emission_factor_kg_co2e_per_kg"
            ])
            st.write("Source:", result["source"])

            st.session_state.activities.append({
                "category": "Food",
                "description": f"{quantity} kg of {food}",
                "emissions": emissions,
                "unit": "kg CO₂e"
            })
        else:
            st.error(result["error"])

elif category == "Waste":

    quantity = st.number_input(
        "Food waste quantity (kg)",
        min_value=0.0,
        value=1.0
    )

    if st.button("Calculate waste emissions"):
        result = calculate_waste_emissions(
            "food_waste",
            quantity,
            "landfill"
        )

        if "error" not in result:
            emissions = result["emissions_kg_co2e"]
            st.success(f"Estimated emissions: {emissions} kg CO₂e")
            st.write("Emission factor:", result[
                "emission_factor_kg_co2e_per_kg"
            ])
            st.write("Source:", result["source"])
            st.caption(result["geographic_scope"])

            st.session_state.activities.append({
                "category": "Waste",
                "description": f"{quantity} kg food waste to landfill",
                "emissions": emissions,
                "unit": "kg CO₂e"
            })
        else:
            st.error(result["error"])

st.divider()

st.header("📝 Your Activity History")

if st.session_state.activities:
    for index, item in enumerate(st.session_state.activities, 1):
        st.write(
            f"{index}. **{item['category']}** — "
            f"{item['description']} — "
            f"{item['emissions']} {item['unit']}"
        )

    if st.button("Clear activity history"):
        st.session_state.activities = []
        st.rerun()
else:
    st.info("No activities recorded yet. Calculate your first activity!")

st.divider()

st.header("🌍 Simple Ways to Reduce Your Impact")

st.write("- Switch off unused electrical appliances.")
st.write("- Prefer public transport when practical.")
st.write("- Choose more plant-based meals.")
st.write("- Avoid unnecessary food waste.")