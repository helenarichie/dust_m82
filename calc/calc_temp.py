def calc_temp(gamma, mu, mp, kb, density, energy, momentum_x, momentum_y, momentum_z, energy_unit, velocity_unit, density_unit):
    n = (density * density_unit) / (mu * mp)
    v_squared = ((momentum_x / density) * velocity_unit) ** 2 + ((momentum_y / density) * velocity_unit) ** 2 + ((momentum_z / density) * velocity_unit) ** 2
    return ((gamma - 1) / (n * kb)) * ((energy * energy_unit) - (0.5 * density * density_unit * v_squared))

def calc_temp_DE(gamma, mu, mp, kb, density, gas_energy, density_unit, velocity_unit):
    pressure_unit = density_unit * velocity_unit ** 2
    n = density * density_unit / (mu * mp)
    return gas_energy * (gamma - 1) * pressure_unit / (n * kb)