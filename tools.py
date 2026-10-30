def calculate_electricity_emissions(units_kwh: float) -> dict:
    """
    Calculate electricity-related CO2 emissions.

    Args:
        units_kwh: Electricity consumed in kilowatt-hours (kWh).

    Returns:
        Emissions estimate and calculation details.
    """

    if units_kwh < 0:
        return {"error": "Electricity usage cannot be negative."}

    emission_factor = 0.710  # kg CO2 per kWh
    emissions = units_kwh * emission_factor

    return {
        "electricity_used_kwh": units_kwh,
        "emission_factor": emission_factor,
        "emissions_kg_co2": round(emissions, 3),
        "source": "CEA CO2 Baseline Database Version 21.0",
        "factor_year": "FY 2024-25"
    }
def calculate_transport_emissions(
    distance_km: float,
    transport_mode: str
) -> dict:
    """
    Estimate passenger tailpipe emissions from travel.

    Supported modes:
    motorcycle, petrol_car, diesel_bus
    """

    if distance_km < 0:
        return {"error": "Distance cannot be negative."}

    emission_factors = {
        "motorcycle": 0.13,
        "petrol_car": 0.20,
        "diesel_bus": 0.029
    }

    if transport_mode not in emission_factors:
        return {
            "error": "Choose motorcycle, petrol_car, or diesel_bus."
        }

    factor = emission_factors[transport_mode]
    emissions = distance_km * factor

    return {
        "distance_km": distance_km,
        "transport_mode": transport_mode,
        "emission_factor_kg_co2e_per_km": factor,
        "emissions_kg_co2e": round(emissions, 3),
        "scope": "Passenger tailpipe emissions only",
        "source": "IIT Madras / TNPCB, July 2023, Table 4"
    }