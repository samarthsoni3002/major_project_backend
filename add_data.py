import firebase_admin
from firebase_admin import credentials, db


def upload_data(category,name,icu):
    
 
    if not firebase_admin._apps:
        cred = credentials.Certificate('major_project_backend/hand_wash_json_file.json')
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://handhygiene-jaypeehealthcare-default-rtdb.firebaseio.com/'
        })
    

    def update_attendance(category, name, icu):
        ref = db.reference(f'Attendance/{category}')
        

        category_data = ref.get()
        
        if not category_data:
            category_data = {}
        
        if name not in category_data:

            category_data[name] = {
                "ACTVs": 0,
                "MICU": 0,
                "NICU": 0,
                "PICU": 0,
                "TICU": 0
            }

    
        if icu in category_data[name]:
            category_data[name][icu] += 1
        else:
            print(f"Invalid ICU '{icu}' provided. Please use one of the following: ACTVs, MICU, NICU, PICU, TICU.")
            return
        

        ref.update({name: category_data[name]})
        print(f"Attendance updated for {name} in {category}, ICU: {icu}")

    update_attendance(category, name, icu)

