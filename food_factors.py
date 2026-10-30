FOOD_EMISSION_FACTORS = {
    "rice": 4.45,
    "wheat": 1.57,
    "chicken": 9.87,
    "beef": 99.48,
    "pork": 12.31,
    "eggs": 4.67,
    "milk": 3.15,
    "cheese": 23.88,
    "tofu": 3.16,
    "lentils": 2.54,
    "beans": 1.37,
    "potatoes": 0.46,
    "tomatoes": 2.09,
    "bananas": 0.86,
    "apples": 0.43,
    "peas": 0.98,
    "onions": 0.50
}


def calculate_food_emissions(
    food_item: str,
    quantity_kg: float
) -> dict:
    """
    Estimate food-related greenhouse gas emissions.

    Quantity must be in kilograms.
    """

    food_item = food_item.strip().lower()

    if quantity_kg < 0:
        return {"error": "Food quantity cannot be negative."}

    if quantity_kg == 0:
        return {"error": "Food quantity must be greater than zero."}

    if food_item not in FOOD_EMISSION_FACTORS:
        return {
            "error": "Food not found. Please choose a supported food item.",
            "supported_foods": list(FOOD_EMISSION_FACTORS.keys())
        }

    factor = FOOD_EMISSION_FACTORS[food_item]
    emissions = quantity_kg * factor

    return {
        "activity": "Food consumption estimate",
        "food_item": food_item,
        "quantity_kg": quantity_kg,
        "emission_factor_kg_co2e_per_kg": factor,
        "emissions_kg_co2e": round(emissions, 3),
        "source": "Poore and Nemecek (2018), via Our World in Data",
        "geographic_scope": "Global average",
        "reference_year": 2010
    }