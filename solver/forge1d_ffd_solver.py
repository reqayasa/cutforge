from model.forge1d_pattern import Forge1DPattern

class Forge1DFFDSolver:
    def solve(self, dataset):
        parts = []

        # expand parts by qty
        for p in dataset.parts:
            for _ in range(p.qty):
                parts.append(p.length)

        # sort decreasing
        parts.sort(reverse=True)

        # cutting patern
        patterns = []
        stock_length = dataset.max_stock_length()

        for part in parts:
            placed = False
            for pattern in patterns:
                if pattern.remaining() >= part:
                    pattern.add_part(part)
                    placed = True
                    break

            if not placed:
                new_pattern = Forge1DPattern(stock_length)
                new_pattern.add_part(part)

                patterns.append(new_pattern)

        return patterns