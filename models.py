from pydantic import BaseModel, BaseSettings

class Settings(BaseSettings):
    SERVER_NAME: str = "localhost:5000"


class Listing(BaseModel):
    partition_key: str # status (new, updated, sold, ...)
    row_key: str # finn_code (unique)

    price: int # Prisantydning
    expenses: int # Omkostninger
    total_price: int # Total pris
    municipality_tax: int  # Kommunale avg. (år)

    house_type: str # Boligtype
    form_of_ownership: str # Eieform
    bedroom: int #Soverom
    prime_living_area: int # Primærrom
    total_living_area: int # Bruksareal
    build_year: int # Byggeår
    energy_letter: str # Energimerking - Bokstav
    energy_color: str # Energimerking - farge
    plot_area: int # Tomteareal
    plot_owner_form: str # Tomt - eieform
    gross_area: int # Bruttoareal
    wealth_value: int # Formuesverdi
    area_description: str # Arealbeskrivelse
    municipality_number: int # Kommune nummer
    gards_nummer: int # Gårdsnummer
    bruks_nummer: int # Bruksnummer
    expenses_text: str # Omkostninger (utregningseksempel)
    facilities: list # Fasiliteter

    street: str # Gatenavn
    post_number: int # Postnummer
    post_place: str # Poststed

    showing_dates: list # Visnigsdato(er)

