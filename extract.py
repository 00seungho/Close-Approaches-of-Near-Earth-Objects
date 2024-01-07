
"""CSV 및 JSON 파일에서 지구 인근 물체 및 근접 접근 데이터 추출
load_neos 함수는 프로젝트 지침에 설명된대로 포맷된 CSV 파일에서 NEO(지구 인근 물체) 데이터를 추출하여 NearEarthObject 컬렉션으로 저장합니다.
load_approaches 함수는 프로젝트 지침에 설명된대로 포맷된 JSON 파일에서 근접 접근 데이터를 추출하여 CloseApproach 객체의 컬렉션으로 저장합니다.
주 모듈은 이러한 함수를 커맨드 라인에서 제공된 인수와 함께 호출하며, 생성된 컬렉션을 사용하여 NEODatabase를 구축합니다.
이 파일은 작업 2에서 편집하게 됩니다."""
import csv
import json

from models import NearEarthObject, CloseApproach


import csv
from models import NearEarthObject

def load_neos(neo_csv_path):
    """CSV 파일에서 지구 인근 물체 정보를 읽습니다.

    :param neo_csv_path: 지구 인근 물체에 관한 데이터가 포함된 CSV 파일의 경로입니다.
    :return: NearEarthObject 객체의 컬렉션.
    """
    neos = []  # Create an empty list to store NEO objects

    with open(neo_csv_path, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            if row[15]:
                dbdiameter = float(row[15])
            else:
                dbdiameter = float('nan')
            neo = NearEarthObject(designation = row[3],name=row[4],diameter=dbdiameter,hazardous=row[7] == "Y")
            neos.append(neo)

    return neos

def load_approaches(cad_json_path):
    """JSON 파일에서 근접 접근 데이터를 읽습니다.

    :param cad_json_path: 근접 접근에 관한 데이터가 포함된 JSON 파일의 경로입니다.
    :return: CloseApproach 객체의 컬렉션.
    """
    close_approaches = []  # Create an empty list to store CloseApproach objects
    with open(cad_json_path, "r") as file:
        data = json.load(file)
        fields = data['fields']
        for entry in data['data']:
            ca_data = dict(zip(fields, entry))
            if float(ca_data['dist']):
                float_dist = float(ca_data['dist'])
            else:
                float_dist=float('nan')
            if float(ca_data['v_rel']):
                float_v_rel = float(ca_data['v_rel'])
            else:
                float_v_rel=float('nan')
            ca = CloseApproach(_designation = ca_data['des'],time=ca_data['cd'],distance= float_dist,velocity = float_v_rel)
            close_approaches.append(ca)

    return close_approaches
