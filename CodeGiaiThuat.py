from typing import Dict, List, Tuple

class WeightNormalizer:
    def __init__(self):
        # mapping interaction -> (min, max)
        self._normalized_weight = {
            "purchase": (0.95, 1.0),
            "cart": (0.70, 0.85),
            "like": (0.50, 0.65),
            "view": (0.30, 0.45),
            "skip": (0.0, 0.15)
        }

    def get_weight(self, interaction: str) -> float:
        if interaction not in self._normalized_weight:
            return 0.0
        low, high = self._normalized_weight[interaction]
        return (low + high) / 2


class GraphEngine:
    def __init__(self, normalizer: WeightNormalizer):
        self.normalizer = normalizer
        self.graph: Dict[str, List[Tuple[str, float]]] = {}

    def build_graph(self, user_interactions: dict):
        for user, interactions in user_interactions.items():
            self.graph[user] = []
            for product, itype in interactions:
                w = self.normalizer.get_weight(itype)
                self.graph[user].append((product, w))
        return self.graph


class Recommendation:
    def __init__(self, graph: dict):
        self.graph = graph

    def weighted_bfs(self, user):
        from collections import defaultdict, deque
        visited = set()
        q = deque([user])
        product_scores = defaultdict(float)

        while q:
            u = q.popleft()
            if u in visited:
                continue
            visited.add(u)

            if u not in self.graph:
                continue

            for product, weight in self.graph[u]:
                product_scores[product] += weight

        return sorted(product_scores.items(), key=lambda x: x[1], reverse=True)


class UIDisplay:
    """
    Lớp mô phỏng giao diện trình duyệt.
    Khi người dùng đăng nhập, hệ thống sẽ hiển thị danh sách sản phẩm đề xuất.
    """
    def show_recommendations(self, user: str, products: List[Tuple[str, float]]):
        print(f"===== RECOMMENDATIONS FOR {user.upper()} =====")
        for product, score in products:
            print(f"- {product} (score: {score:.3f})")
        print("==============================================")


class AppCore:
    def __init__(self):
        self.normalizer = WeightNormalizer()
        self.graph_engine = GraphEngine(self.normalizer)
        self.recommender = None
        self.ui = UIDisplay()

    def run(self, user_interactions: dict, login_user: str):
        # user_interactions: dữ liệu thực tế từ database hoặc file
        graph = self.graph_engine.build_graph(user_interactions)
        self.recommender = Recommendation(graph)

        # Tính toán sản phẩm đề xuất cho người dùng đăng nhập
        results = self.recommender.weighted_bfs(login_user)

        # Hiển thị trên UI mô phỏng
        self.ui.show_recommendations(login_user, results)


if __name__ == "__main__":
    # Ví dụ chạy thử với dữ liệu có sẵn
    # Khi triển khai thực tế, AppCore.run() nhận dữ liệu đọc từ DB/file
    data = {}
    app = AppCore()
    app.run(data, login_user="u001")
