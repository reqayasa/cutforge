from model.forge1d_model import Part, Stock, Pattern

class Solver1D:
    def solve(self, dataset):
        parts = sorted(dataset[1], key=lambda x: x.length, reverse=True)
        stocks = sorted(dataset[0], key=lambda x: x.length)

        patterns: list[Pattern] = []

        for part in parts:
            while part.qty > 0:
                placed = False

                valid_patterns = [
                    p for p in patterns if p.remaining() >= part.length
                ]

                if valid_patterns:
                    best = min(valid_patterns, key=lambda p: p.remaining())
                    best.add_part(part)
                    part.remove()
                    continue

                placed = False
                for stock in stocks:
                    if stock.qty > 0 and stock.length >= part.length:
                        new_pattern = Pattern(
                            stock_id=stock.id,
                            stock_length=stock.length
                        )

                        new_pattern.add_part(part)
                        
                        stock.remove()
                        part.remove()

                        patterns.append(new_pattern)
                        placed = True
                        break
                
                if not placed:
                    raise ValueError(
                        "Cannot place part {part.id} (length={part.length})"
                    )
                
        for p in patterns:
            print(f"Stock {p.stock_id} (length={p.stock_length})")
            for id, length in p.parts:
                print(f"  -> Part {id}, length={length}")
            print(f"  Remaining: {p.remaining()}")

        return patterns