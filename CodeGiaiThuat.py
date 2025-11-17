import random
from collections import defaultdict

# Class WeightNormalizer
class WeightNormalizer:
    def __init__(self):
        self.__normalizedWeight = {
            "purchase": (0.95, 1.00),
            "cart": (0.70, 0.85),
            "like": (0.50, 0.65),
            "view": (0.30, 0.45),
            "skip": (0.00, 0.20)
        }

    def getNormalizedWeight(self, behavior):
        minW, maxW = self.__normalizedWeight.get(behavior, (0.00, 0.00))
        if minW == 0.0 and maxW == 0.0 and behavior not in self.__normalizedWeight:
             return 0.0
        return round(random.uniform(minW, maxW), 2)

# Class GraphEngine
class GraphEngine:
    def __init__(self, normalizer: WeightNormalizer):
        self.normalizer = normalizer
        self.userGraph = defaultdict(dict) # Đồ thị người dùng
        self.productGraph = defaultdict(dict) # Đồ thị sản phẩm
        self.userHistory = defaultdict(list) # Lịch sử hành vi người dùng
        self.bestSellers = set() # Sản phẩm bán chạy nhất

    # Thêm hành vi người dùng
    def addAction(self, user, product, behavior):
        self.userHistory[user].append((product, behavior))
    # Xây dựng đồ thị
    def buildGraph(self):
        self.userGraph.clear()
        self.productGraph.clear()

        # Xây dựng đồ thị người dùng
        for user, actions in self.userHistory.items():
            for product, behavior in actions:
                weight = self.normalizer.getNormalizedWeight(behavior)
                # Cập nhật Đồ thị Người dùng (U -> {P: W})
                self.userGraph[user][product] = self.userGraph[user].get(product, 0) + weight
            
        # Xây dựng đồ thị sản phẩm
        for user, products in self.userGraph.items():
            for product, weight in products.items():
                self.productGraph[product][user] = weight

# Class Recommendation (Giải thuật Đề xuất)
class Recommendation:
    def __init__(self, graphEngine: GraphEngine):
        self.graphEngine = graphEngine

    def recommendProducts(self, user, topN=5):
        if user not in self.graphEngine.userGraph:
            return []
        topProducts = sorted(self.graphEngine.userGraph[user].items(), key=lambda x: x[1], reverse=True)[:topN]
        result = []
        for product, weight in topProducts:
            result.append((product, weight))
        return result