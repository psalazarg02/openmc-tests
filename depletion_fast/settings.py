import openmc

def create_settings():
    # Particle settings
    settings = openmc.Settings()
    settings.particles = 1000
    settings.inactive = 10
    settings.batches = 50
    return settings

if __name__ == "__main__":
    settings = create_settings()