from math import sqrt
import math
from scipy.spatial import distance
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class DistanceFunctions:

    def __init__(self):
        self.RADIUS = 6371

    def euclidean(self, vec1, vec2):
        """
        Euclidean Distance for Spatial Data
        """
        return distance.euclidean(vec1, vec2)

    def manhattan(self, vec1, vec2):
        """
        Manhattan distance for spatial data
        """
        return distance.cityblock(vec1, vec2)

    def haversine(self, vec1, vec2):
        """
        Haversine distance for spatial data. (Response is kilometers)
        """
        lat1, lon1 = vec1
        lat2, lon2 = vec2.as_py()

        
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * \
            math.cos(lat2) * math.sin(dlon / 2)**2
        
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return self.RADIUS * c

    def cosine(self, vec1, vec2):
        return distance.cosine(vec1, vec2)

    def cosineText(self, vec1, vec2):
        from helpers import Helpers
        hp = Helpers()

        vec1Emb = hp.generate_text_embedding(vec1).reshape(-1)
        print("vec1")
        vec2Emb = hp.generate_text_embedding(vec2).reshape(-1)
        print("cant vectorize")
        return self.cosine(vec1Emb, vec2Emb)

    def levenshtein(self, str1, str2):
        len1, len2 = len(str1), len(str2)
        dp = [[0] * (len2 + 1) for _ in range(len1 + 1)]

        for i in range(len1 + 1):
            dp[i][0] = i
        for j in range(len2 + 1):
            dp[0][j] = j

        for i in range(1, len1 + 1):
            for j in range(1, len2 + 1):
                cost = 0 if str1[i - 1] == str2[j - 1] else 1
                dp[i][j] = min(dp[i - 1][j] + 1,
                               dp[i][j - 1] + 1,
                               dp[i - 1][j - 1] + cost)

        return dp[len1][len2]

    def date(self, center, attrib, radius, unit):
        # Radius = amount
        # Reference Date = Center
        # Attrib = target date
        # unit = distance function
        """
        Verifica se uma data está dentro de um intervalo de tempo a partir de uma data de referência.

        Args:
            reference_date (str): Data de referência no formato "YYYY-MM-DD".
            target_date (str): Data alvo para verificação no formato "YYYY-MM-DD".
            amount (int): Quantidade da unidade de tempo.
            unit (str): Unidade de tempo ("DAY", "WEEK", "MONTH", "YEAR").

        Returns:
            bool: True se a data alvo estiver no intervalo, False caso contrário.
        """
        units = {
            'DAY': lambda x: timedelta(days=x),
            'WEEK': lambda x: timedelta(weeks=x),
            'MONTH': lambda x: relativedelta(months=x),
            'YEAR': lambda x: relativedelta(years=x),
        }

        if unit not in units:
            raise ValueError(
                "Unidade inválida. Use: 'DAY', 'WEEK', 'MONTH', ou 'YEAR'.")

        ref_date = datetime.strptime(center, "%Y-%m-%d")
        tgt_date = datetime.strptime(attrib, "%Y-%m-%d")

        max_date = ref_date + units[unit](radius)
        min_date = ref_date - units[unit](radius)

        return min_date <= tgt_date <= max_date

    # # Exemplo de uso:
    # print(date_distance("2025-01-01", "2025-01-15", 45, "DAY"))  # True
    # print(date_distance("2025-01-01", "2025-03-01", 3, "WEEK"))  # False
    # print(date_distance("2025-01-01", "2025-02-28", 2, "MONTH")) # True
    # print(date_distance("2025-01-01", "2026-01-01", 1, "YEAR"))  # True
