"""Close Approach 정보를 CSV 또는 JSON 형식으로 스트림으로 작성합니다.

이 모듈은 두 개의 함수인 `write_to_csv`와 `write_to_json`을 내보냅니다.
각 함수는 근접 접근 정보 스트림(`results`)과 데이터를 작성할 경로를 매개변수로 받습니다.

이러한 함수들은 주 모듈에서 `limit` 함수의 출력과 사용자가 명령 줄에서 제공한 파일 이름을 사용하여 호출됩니다.
파일의 확장자는 이 함수들 중 어느 것을 사용할지를 결정합니다.

이 파일은 Part 4에서 수정하게 될 것입니다.
"""

import csv
import json


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output row
    corresponds to the information in a single close approach from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    fieldnames = (
        'datetime_utc', 'distance_au', 'velocity_km_s',
        'designation', 'name', 'diameter_km', 'potentially_hazardous'
    )
    
    # TODO: 결과를 지시사항에 따라 CSV 파일로 작성합니다.
    with open(filename, "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            content = result.serialize()
            content.update(result.neo.serialize())
            content["name"] = content["name"] if content["name"] is not None else ""
            content["potentially_hazardous"] = "True" if content["potentially_hazardous"] else "False"
            writer.writerow(content)

def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """

    # TODO: 결과를 지시사항에 따라 JSON 파일로 작성합니다.
    json_data = []
    for result in results:
        content = result.serialize()
        content.update(result.neo.serialize())
        content["name"] = content["name"] if content["name"] is not None else ""
        content["potentially_hazardous"] = "True" if content["potentially_hazardous"] else "False"
        json_data.append(
            {
                "datetime_utc": content["datetime_utc"],
                "distance_au": content["distance_au"],
                "velocity_km_s": content["velocity_km_s"],
                "neo": {
                    "designation": content["designation"],
                    "name": content["name"],
                    "diameter_km": content["diameter_km"],
                    "potentially_hazardous": bool(content["potentially_hazardous"])
                }
            }
        )
    with open(filename, "w") as json_file:
        json.dump(json_data, json_file)