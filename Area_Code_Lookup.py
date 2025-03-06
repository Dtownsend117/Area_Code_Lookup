import requests
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderServiceError
import speech_recognition as sr
import pyttsx3
import threading
import time

class AreaCodeSearcher:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="my_geopy_app")
        self.recognizer = sr.Recognizer()
        
        self.engine = pyttsx3.init("sapi5")
        voices = self.engine.getProperty("voices")
        self.engine.setProperty("voice", voices[1].id)  # Change "1" to use a different voice
        self.engine.setProperty("rate", 170) 

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def get_location_by_area_code(self, area_code):
        area_code_coordinates = {
            #^ United States Area Codes
            "205": (33.5186, -86.8104),  # Birmingham, AL260
            "251": (30.6954, -88.0399),  # Mobile, AL
            "256": (34.7304, -86.5861),  # Huntsville, AL
            "334": (32.3668, -86.3000),  # Montgomery, AL
            "907": (58.3019, -134.4197),  # Anchorage, AK
            "480": (33.4484, -111.9930),  # Mesa, AZ
            "520": (32.2226, -110.9747),  # Tucson, AZ
            "602": (33.4484, -112.0740),  # Phoenix, AZ
            "623": (33.5355, -112.2711),  # Glendale, AZ
            "479": (35.4626, -94.1625),  # Fort Smith, AR
            "501": (34.7465, -92.2896),  # Little Rock, AR
            "870": (35.2010, -91.8318),  # Jonesboro, AR
            "209": (37.4848, -120.8431),  # Stockton, CA
            "213": (34.0522, -118.2437),  # Los Angeles, CA
            "310": (33.9008, -118.3917),  # Los Angeles, CA
            "415": (37.7749, -122.4194),  # San Francisco, CA
            "510": (37.8044, -122.2711),  # Oakland, CA
            "619": (32.7157, -117.1611),  # San Diego, CA
            "650": (37.5535, -122.2730),  # San Mateo, CA
            "707": (38.4405, -122.7141),  # Santa Rosa, CA
            "818": (34.1478, -118.1445),  # San Fernando Valley, CA
            "925": (38.0049, -121.8058),  # Concord, CA
            "303": (39.7392, -104.9903),  # Denver, CO
            "719": (38.8339, -104.8214),  # Colorado Springs, CO
            "720": (39.7392, -104.9903),  # Denver, CO
            "203": (41.3083, -73.2121),  # Bridgeport, CT
            "860": (41.6032, -72.7554),  # Hartford, CT
            "475": (41.3083, -73.2121),  # New Haven, CT
            "302": (39.1582, -75.5244),  # Wilmington, DE
            "202": (38.9072, -77.0369),  # Washington, D.C.
            "727": (27.7652, -82.7460),  # St. Petersburg, FL
            "305": (25.7617, -80.1918),  # Miami, FL
            "407": (28.5383, -81.3792),  # Orlando, FL
            "561": (26.6406, -80.0416),  # West Palm Beach, FL
            "850": (30.4383, -84.2807),  # Tallahassee, FL
            "904": (30.3322, -81.6557),  # Jacksonville, FL
            "678": (33.7490, -84.3880),  # Atlanta, GA
            "404": (33.7490, -84.3880),  # Atlanta, GA
            "470": (33.7490, -84.3880),  # Atlanta, GA
            "808": (21.3069, -157.8583),  # Honolulu, HI
            "208": (43.6150, -116.2023),  # Boise, ID
            "312": (41.8781, -87.6298),  # Chicago, IL
            "618": (38.6270, -89.3985),  # East St. Louis, IL
            "630": (41.8369, -88.2103),  # DuPage County, IL
            "773": (41.8781, -87.6298),  # Chicago, IL
            "815": (41.7339, -88.0850),  # Joliet, IL
            "847": (42.0834, -88.2242),  # Northwest Suburbs, IL
            "219": (41.5868, -87.4210),  # Northwest Indiana
            "260": (41.1255, -85.1394),  # Fort Wayne, IN
            "317": (39.7684, -86.1581),  # Indianapolis, IN
            "574": (41.6764, -86.2500),  # South Bend, IN
            "812": (38.2542, -86.1349),  # Southern Indiana
            "319": (42.0347, -91.5853),  # Cedar Rapids, IA
            "515": (41.5868, -93.6200),  # Des Monies, IA
            "641": (41.9999, -93.0000),  # Central Iowa
            "712": (42.5000, -95.5000),  # Western Iowa
            "785": (39.0483, -95.6772),  # Topeka, KS
            "316": (37.6872, -97.3301),  # Wichita, KS
            "913": (39.0997, -94.5786),  # Kansas City, KS
            "270": (37.0000, -86.0000),  # Western Kentucky
            "502": (38.2542, -85.7594),  # Louisville, KY
            "606": (37.0000, -83.0000),  # Eastern Kentucky
            "859": (38.0406, -84.5000),  # Northern Kentucky
            "225": (30.4515, -91.1871),  # Baton Rouge, LA
            "318": (32.5251, -92.1193),  # Northern Louisiana
            "337": (30.6954, -92.0198),  # Southwestern Louisiana
            "504": (29.9511, -90.0715),  # New Orleans, LA
            "601": (32.2988, -90.1848),  # Jackson, MS
            "662": (34.0000, -89.0000),  # Northern Mississippi
            "601": (32.2988, -90.1848),  # Jackson, MS
            "417": (37.2153, -93.2982),  # Southwest Missouri
            "573": (38.5767, -92.1735),  # Central Missouri
            "816": (39.0997, -94.5786),  # Kansas City, MO
            "314": (38.6270, -90.1994),  # St. Louis, MO
            "406": (46.5891, -110.3626),  # Montana
            "775": (39.5296, -119.8138),  # Northern Nevada
            "702": (36.1699, -115.1398),  # Las Vegas, NV
            "603": (43.1939, -71.5724),  # New Hampshire
            "201": (40.8136, -74.0700),  # Jersey City, NJ
            "609": (39.9537, -74.9332),  # Trenton, NJ
            "732": (40.2206, -74.0690),  # Central New Jersey
            "856": (39.8950, -75.1197),  # Southern New Jersey
            "973": (40.7851, -74.1704),  # Northern New Jersey
            "505": (35.6869, -105.9378),  # New Mexico
            "575": (34.5000, -106.0000),  # New Mexico
            "718": (40.6501, -73.9496),  # Brooklyn, NY
            "212": (40.7128, -74.0060),  # Manhattan, NY
            "646": (40.7128, -74.0060),  # Manhattan, NY
            "718": (40.6501, -73.9496),  # Brooklyn, NY
            "917": (40.7128, -74.0060),  # New York City, NY
            "315": (43.0481, -75.2172),  # Syracuse, NY
            "585": (43.1610, -77.6109),  # Rochester, NY
            "607": (42.0930, -76.1820),  # Binghamton, NY
            "914": (40.9950, -73.8356),  # Westchester County, NY
            "330": (41.0814, -81.5190),  # Akron, OH
            "216": (41.4995, -81.6954),  # Cleveland, OH
            "419": (41.6501, -83.5379),  # Toledo, OH
            "513": (39.1031, -84.5120),  # Cincinnati, OH
            "937": (39.7589, -84.1916),  # Dayton, OH
            "405": (35.4676, -97.5164),  # Oklahoma City, OK
            "918": (36.1539, -95.9928),  # Tulsa, OK
            "503": (45.5051, -122.6750),  # Portland, OR
            "541": (43.8041, -120.5542),  # Central and Southern Oregon
            "971": (45.5051, -122.6750),  # Portland, OR
            "215": (40.7128, -74.0060),  # Philadelphia, PA
            "412": (40.4406, -79.9959),  # Pittsburgh, PA
            "610": (40.0379, -75.3920),  # Allentown, PA
            "717": (40.2732, -76.8844),  # Harrisburg, PA
            "814": (40.5932, -78.9025),  # Erie, PA
            "401": (41.5801, -71.4774),  # Rhode Island
            "803": (34.0007, -80.0103),  # Columbia, SC
            "843": (33.8361, -79.9748),  # Charleston, SC
            "864": (34.7465, -82.3889),  # Greenville, SC
            "605": (43.9695, -99.9018),  # South Dakota
            "615": (36.1627, -86.7816),  # Nashville, TN
            "901": (35.1495, -90.0490),  # Memphis, TN
            "931": (36.1627, -86.7816),  # Middle Tennessee
            "210": (29.4241, -98.4936),  # San Antonio, TX
            "214": (32.7767, -96.7970),  # Dallas, TX
            "281": (29.7604, -95.3698),  # Houston, TX
            "713": (29.7604, -95.3698),  # Houston, TX
            "817": (32.7555, -97.3308),  # Fort Worth, TX
            "903": (32.7804, -95.7063),  # Northeast Texas
            "956": (26.2034, -98.2300),  # South Texas
            "435": (39.5000, -111.5000),  # Utah
            "801": (40.7608, -111.8910),  # Salt Lake City, UT
            "802": (44.5582, -72.5778),  # Vermont
            "703": (38.8048, -77.0469),  # Northern Virginia
            "757": (36.8508, -76.2859),  # Hampton Roads, VA
            "804": (37.5407, -77.4360),  # Richmond, VA
            "206": (47.6062, -122.3321),  # Seattle, WA
            "253": (47.1850, -122.2937),  # Tacoma, WA
            "360": (47.0379, -122.9007),  # Western Washington
            "425": (47.7511, -122.3189),  # Eastside, WA
            "509": (47.4009, -120.5016),  # Eastern Washington
            "304": (38.5976, -80.4549),  # West Virginia
            "681": (38.5976, -80.4549),  # West Virginia
            "262": (43.0000, -88.0000),  # Southeastern Wisconsin
            "414": (43.0389, -87.9065),  # Milwaukee, WI
            "608": (43.0747, -89.3842),  # Madison, WI
            "715": (45.0000, -90.0000),  # Northern Wisconsin
            "920": (44.0000, -88.0000),  # Northeastern Wisconsin
            "307": (42.7550, -107.3025),  # Wyoming
#>===================================================================
            #^ Next Country Area Codes, add under this if adding for another country    
         }

        if area_code not in area_code_coordinates:
            response_text = f"Area code {area_code} not found in the database."
            print(response_text)
            self.speak(response_text)
            return

        latitude, longitude = area_code_coordinates[area_code]

        try:
            location = self.geolocator.reverse(f"{latitude},{longitude}")
            address = location.raw['address']

            # This gathers the results
            city = address.get('city', '')
            state = address.get('state', '')
            country = address.get('country', '')
            zipcode = address.get('postcode', '')

            response_text = (f"Area Code: {area_code}\n"
                             f"City: {city}\n"
                             f"State: {state}\n"
                             f"Zip Code: {zipcode}\n"
                             f"Country: {country}")
            print(response_text)
            self.speak(response_text)
            self.speak(f"search again or exit?")

        except GeocoderServiceError as e:
            error_message = f"Error: {e}"
            print(error_message)
            self.speak(error_message)
    
    def listen_for_area_code(self):
        with sr.Microphone() as source:
            print("Listening for area code...")
            print("Say another or exit after the first result.")
            audio = self.recognizer.listen(source)
    
            try:
                area_code = self.recognizer.recognize_google(audio)
                print(f"You said: {area_code}")
                return area_code
            except sr.UnknownValueError:
                print("Sorry, I did not understand that.")
                self.speak("Sorry, I did not understand that.")
                return None
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
                self.speak("Could not request results from the speech recognition service.")
                return None

    def run(self):
        while True:
            user_input = self.listen_for_area_code()
            if user_input is None:
                break
            if not user_input.isdigit():
                self.speak("Please say a valid numeric area code.")
                continue
            
            self.get_location_by_area_code(user_input)

            while True:  
                print("Please say 'another' to search for another area code or 'exit' to quit.")

                next_action = self.listen_for_area_code()

                if next_action is None:
                    continue

                next_action = next_action.lower()

                continue_phrases = ["another"]
                exit_phrases = ["exit", "quit", "stop", "no more", "done"]

                if any(phrase in next_action for phrase in exit_phrases):
                    self.speak("Goodbye!")
                    print("Goodbye!")
                    return 
                elif any(phrase in next_action for phrase in continue_phrases):
                    break  
                else:
                    self.speak("I didn't understand that. Please say 'another' to continue or 'exit' to quit.")

if __name__ == "__main__":
    searcher = AreaCodeSearcher()
    searcher.run()
