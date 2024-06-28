from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import swisseph as swe
import datetime

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

class BirthDetails(BaseModel):
    date_of_birth: str
    time_of_birth: str
    place_of_birth: str

@app.post("/calculate-vedic-astrological-sign")
def calculate_vedic_astrological_sign(details: BirthDetails):
    try:
        swe.set_sid_mode(swe.SIDM_LAHIRI)

        # Parse the date and time of birth to a datetime object
        birth_datetime = datetime.datetime.strptime(f"{details.date_of_birth} {details.time_of_birth}", "%Y-%m-%d %H:%M")

        # Convert the birth datetime to Julian Day, which is needed for the calculation
        julian_day = swe.julday(birth_datetime.year, birth_datetime.month, birth_datetime.day,  birth_datetime.hour)

        # Calculate the position of the Moon at the time of birth
        moon_position, _ = swe.calc_ut(julian_day, swe.MOON, swe.FLG_SIDEREAL)

        # Get the Ayanamsa (precession) value to adjust the Moon's position
        ayanamsa = round(swe.get_ayanamsa_ut(julian_day), -2)

        # Adjust Moon's position by subtracting Ayanamsa to get Sidereal position
        moon_sidereal_position = round(moon_position[0] - ayanamsa)

        # The zodiac signs in order
        zodiac_signs = ["♈ Aries ♈", "♉ Taurus ♉", "♊ Gemini ♊", "♋ Cancer ♋", "♌ Leo ♌", "♍ Virgo ♍", "♎ Libra ♎",
                        "♏ Scorpio ♏", "♐ Sagittarius ♐", "♑ Capricorn ♑", "♒ Aquarius ♒", "♓ Pisces ♓"]

        # Calculate the Moon's sign; each sign spans 30 degrees
        moon_sign_index = int(moon_sidereal_position / 30) % 12
        moon_sign = zodiac_signs[moon_sign_index]

        return {"vedic_astrological_sign": moon_sign}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid input. Please enter valid date and time.")

@app.get("/", response_class=FileResponse)
def read_index():
    return FileResponse('static/index.html')
