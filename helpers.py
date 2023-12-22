"""Convert datetimes to and from strings.

NASA's dataset provides timestamps as naive datetimes (corresponding to UTC).

The `cd_to_datetime` function converts a string, formatted as the `cd` field of
NASA's close approach data, into a Python `datetime`

The `datetime_to_str` function converts a Python `datetime` into a string.
Although `datetime`s already have human-readable string representations, those
representations display seconds, but NASA's data (and our datetimes!) don't
provide that level of resolution, so the output format also will not.
"""
import datetime


def cd_to_datetime(calendar_date):
    """NASA 서식의 달력 날짜/시간 설명을 datetime으로 변환합니다.

    NASA의 형식은 적어도 접근 데이터의 `cd` 필드에서 영어 로캘의 월 이름을 사용합니다. 예를 들어, 2020년 12월 31일 정오는 다음과 같습니다:

        2020-Dec-31 12:00

        이것은 Python 객체 `datetime.datetime(2020, 12, 31, 12, 0)`으로 변환됩니다.

    :param calendar_date: YYYY-bb-DD hh:mm 형식의 달력 날짜.
    :return: 주어진 달력 날짜와 시간에 해당하는 나이브 `datetime`.
    """

    return datetime.datetime.strptime(calendar_date, "%Y-%b-%d %H:%M")


def datetime_to_str(dt):
    """나이브한 Python datetime을 사람이 읽기 쉬운 문자열로 변환합니다.

    Python datetime의 기본 문자열 표현에는 초가 포함되어 있지만, 
    우리의 데이터는 그렇게 정밀하지 않으므로 이 함수는 연, 월, 일, 시간 및 분 값을 포맷팅합니다. 
    또한 이 함수는 로케일별 월 이름과의 모호성을 피하기 위해 날짜를 표준 ISO 8601 YYYY-MM-DD 형식으로 제공합니다.

    :param dt: 나이브한 Python datetime.
    :return: 초를 제외한 사람이 읽기 쉬운 datetime 문자열.
    """

    return datetime.datetime.strftime(dt, "%Y-%m-%d %H:%M")
