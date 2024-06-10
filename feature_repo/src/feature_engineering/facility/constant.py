class Distance:
    RADIUS = 6371
    MULTIPLE_TRANSFORM_COEFF = 10 / 1000
    DISTANCE_THRESHOLD = 10000


class FilePath:

    MAIN_FILE_PATH = 'app/files'

    MAIN_LABEL_ENCODER_PATH = f'{MAIN_FILE_PATH}/labelencoder'
    DISTRICT_LABEL_ENCODER = f'{MAIN_LABEL_ENCODER_PATH}/district_label_encoder.pkl'
    ADMINISTRATIVE_GENRE_LABEL_ENCODER = f'{MAIN_LABEL_ENCODER_PATH}/administrative_genre_label_encoder.pkl'
    WARD_LABEL_ENCODER = f'{MAIN_LABEL_ENCODER_PATH}/ward.pkl'
    ROAD_LABEL_ENCODER = f'{MAIN_LABEL_ENCODER_PATH}/road.pkl'
    DIRECTION_LABEL_ENCODER = f'{MAIN_LABEL_ENCODER_PATH}/the_direction_of_the_house.pkl'

    VECTOR_EMBEDDING = f'{MAIN_FILE_PATH}/embedding/VECTOR_EMBEDDING.pkl'

    MAIN_JSON_PATH = f'{MAIN_FILE_PATH}/json'
    OPENAPI_PATH = f'/{MAIN_JSON_PATH}/openapi.json'
    ALLEY_DESC = f'{MAIN_JSON_PATH}/alley_desc.json'
    DISTRICT_DESC = f'{MAIN_JSON_PATH}/districts.json'
    DISTRICT_STATS = f'{MAIN_JSON_PATH}/district_stats.json'
    MODIFIED_DISTRICT_STATS = f'{MAIN_JSON_PATH}/district_stats.json'

    HOUSE_DIRECTION_DESC = f'{MAIN_JSON_PATH}/house_direction_desc.json'
    MEAN_OF_FACILITY_DESC = f'{MAIN_JSON_PATH}/means_of_facility.json'
    CENTER_GEOLOCATION = f'{MAIN_JSON_PATH}/center_geolocation.json'
    GEOLOCATION = f'{MAIN_JSON_PATH}/geolocation.json'
    DETAILED_LOCATION = f'{MAIN_JSON_PATH}/detailed_location.json'

    REAL_ESTATE_PRICE = f'{MAIN_JSON_PATH}/real_estate_price.json'

    MAIN_TABLE_PATH = f'{MAIN_FILE_PATH}/table'
    ROAD_DESC = f'{MAIN_TABLE_PATH}/best_road_place.csv'
    PARK_DESC = f'{MAIN_TABLE_PATH}/best_park.csv'
    COMMERCIAL_DESC = f'{MAIN_TABLE_PATH}/best_commercial_center_place.csv'
    POPULATION_DESC = f'{MAIN_TABLE_PATH}/population.csv'


    MAIN_CHECKPOINT_PATH = f'{MAIN_FILE_PATH}/checkpoints'
    PRICE_MODEL_V3 = f'{MAIN_CHECKPOINT_PATH}/text_and_tab_v3/model_'
    PRICE_MODEL_V1 = f'{MAIN_CHECKPOINT_PATH}/text_and_tab/model_'

    PRICE_FEATURES = f'{MAIN_JSON_PATH}/columns/prediction_price_features.json'
    DISTANCE_FEATURES = f'{MAIN_JSON_PATH}/columns/distance_features.json'

    ALL_STREET_GEOLOCATION = f'{MAIN_JSON_PATH}/geolocation/district'
    STREET_PRICE = f'{MAIN_JSON_PATH}/price/district'
    GROUP_PRICE = f'{MAIN_JSON_PATH}/price'
