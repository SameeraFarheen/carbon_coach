def calculate_waste_emissions(
    waste_item: str,
    quantity_kg: float,
    disposal_method: str
) -> dict:
    """
    Estimate emissions from food waste sent to landfill.

    This factor is based on the US EPA WARM model.
    It is not an India-specific emission factor.
    """

    waste_item = waste_item.strip().lower()
    disposal_method = disposal_method.strip().lower()

    if quantity_kg <= 0:
        return {"error": "Quantity must be greater than zero."}

    if waste_item != "food_waste":
        return {
            "error": "Currently, only food_waste is supported."
        }

    if disposal_method != "landfill":
        return {
            "error": "Currently, only landfill disposal is supported."
        }

    # EPA WARM Version 16:
    # 0.50 metric tonnes CO2e per US short ton.
    # Converted to approximately 0.551 kg CO2e per kg.
    emission_factor = 0.551

    emissions = quantity_kg * emission_factor

    return {
        "activity": "Food waste disposal",
        "waste_item": waste_item,
        "quantity_kg": quantity_kg,
        "disposal_method": disposal_method,
        "emission_factor_kg_co2e_per_kg": emission_factor,
        "emissions_kg_co2e": round(emissions, 3),
        "source": "US EPA WARM Version 16, December 2023",
        "geographic_scope": "United States model; not India-specific"
    }