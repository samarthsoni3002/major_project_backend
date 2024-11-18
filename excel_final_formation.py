from data_formation_icus import fetch_icu_data
from data_formation_attendance import fetch_attendance_data



def final_formation():
    
   
    fetch_icu_data()
    name = fetch_attendance_data()
    return name
    

print(final_formation())