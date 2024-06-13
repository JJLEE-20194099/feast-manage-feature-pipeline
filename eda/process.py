import json
from tqdm import tqdm

data = json.load(open('../data/process_v1/realestate-dataset.json', 'r'))

errors = []
def get_compact_info(item):
    try:
        try:
            numberOfFloors = item['houseInfo']['value']['numberOfFloors']
        except:
            numberOfFloors = None


        try:
            numberOfBedRooms = item['houseInfo']['value']['numberOfBedRooms']
        except:
            numberOfBedRooms = None

        try:
            numberOfBathRooms = item['houseInfo']['value']['numberOfBathRooms']
        except:
            numberOfBathRooms = None

        try:
            numberOfKitchens = item['houseInfo']['value']['numberOfKitchens']
        except:
            numberOfKitchens = None

        try:
            numberOfLivingRooms = item['houseInfo']['value']['numberOfLivingRooms']
        except:
            numberOfLivingRooms = None

        try:
            numberOfGarages = item['houseInfo']['value']['numberOfGarages']
        except:
            numberOfGarages = None

        try:
            certificateOfLandUseRight = item['mediaInfo']['certificateOfLandUseRight']['certificateStatus']
        except:
            certificateOfLandUseRight = None

        try:
            ward = item['propertyBasicInfo']['address']['value']['ward']
        except:
            ward = None

        try:
            street = item['propertyBasicInfo']['address']['value']['street']
        except:
            street = None
        try:
            district = item['propertyBasicInfo']['address']['value']['district']
        except:
            district = None
        try:
            city = item['propertyBasicInfo']['address']['value']['city']
        except:
            city = None
        try:
            lat = item['propertyBasicInfo']['geolocation']['value']['latitude']['value']
        except:
            lat = None
        try:
            lon = item['propertyBasicInfo']['geolocation']['value']['longitude']['value']
        except:
            lon = None
        try:
            typeOfRealEstate = item['propertyBasicInfo']['typeOfRealEstate']['value']
        except:
            typeOfRealEstate = None
        try:
            frontWidth = item['propertyBasicInfo']['frontWidth']['value']
        except:
            frontWidth = None
        try:
            endWidth = item['propertyBasicInfo']['endWidth']['value']
        except:
            endWidth = None
        try:
            facade = item['propertyBasicInfo']['facade']['value']
        except:
            facade = None
        try:
            houseDirection = item['propertyBasicInfo']['houseDirection']['value']
        except:
            houseDirection = None
        try:
            landSize = item['propertyBasicInfo']['landSize']['value']
        except:
            landSize = None
        try:
            price = item['propertyBasicInfo']['price']['value']
        except:
            price = None
        try:
            unitPrice = item['propertyBasicInfo']['unitPrice']['value']
        except:
            unitPrice = None
        try:
            distanceToNearestRoad = item['propertyBasicInfo']['distanceToNearestRoad']['value']
        except:
            distanceToNearestRoad = None
        try:
            frontRoadWidth = item['propertyBasicInfo']['frontRoadWidth']['value']
        except:
            frontRoadWidth = None
        try:
            accessibility = item['propertyBasicInfo']['accessibility']['value']
        except:
            accessibility = None
        try:
            landType = item['propertyBasicInfo']['landType']['value']
        except:
            landType = None

        try:
            description = item['propertyBasicInfo']['description']['value']
        except:description = ""


        return {
            "numberOfFloors": numberOfFloors,
            "numberOfBathRooms": numberOfBathRooms,
            "numberOfBedRooms": numberOfBedRooms,
            "numberOfKitchens": numberOfKitchens,
            "numberOfGarages": numberOfGarages,
            "certificateOfLandUseRight": certificateOfLandUseRight,
            "ward": ward,
            "street": street,
            "district": district,
            "city": city,
            "lat": lat,
            "lon": lon,
            "typeOfRealEstate": typeOfRealEstate,
            "frontWidth": frontWidth,
            "endWidth": endWidth,
            "facade": facade,
            "houseDirection": houseDirection,
            "landSize": landSize,
            "price": price,
            "unitPrice": unitPrice,
            "distanceToNearestRoad": distanceToNearestRoad,
            "frontRoadWidth": frontRoadWidth,
            "accessibility": accessibility,
            "landType": landType,
            "description": description,
        }
    except Exception as e:
        print(e)
        errors.append(item)
        return {}

process_data = [get_compact_info(item) for item in tqdm(data)]
json_object = json.dumps(process_data, indent=4,ensure_ascii=False )
with open("../data/process_v1/process_data.json", "w",encoding='utf-8' ) as outfile:
    outfile.write(json_object)


json_object = json.dumps(errors, indent=4,ensure_ascii=False )
with open("../data/process_v1/process_data_error.json", "w",encoding='utf-8' ) as outfile:
    outfile.write(json_object)

