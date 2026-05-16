from model.internal_model import GroupInput
from model.solver_model import GroupSolveResult, StockUsage, UnmetDemand, CutAssignment

def solve_group(group: GroupInput) -> GroupSolveResult:
    # expand demand
    expanded_demands = [
        (demand.id, demand.length) for demand in group.demands
        for _ in range(demand.quantity)
    ]

    # sort descending
    # part = (0:id, 1:length)
    sorted_demands = sorted(expanded_demands, key=lambda x: x[1], reverse=True)

    # expand stock
    # stock = (0:id, 1:length)
    expanded_stocks = [
        (stock.id, stock.length) for stock in group.stocks
        for _ in range(stock.quantity)
    ]

    # first fit placement
    prepare_usages = []
    prepare_unmet = []
    for demand in sorted_demands:
        is_assigned = False
        for stock in prepare_usages:
            if demand[1] + group.kerf <= stock[3]: # check stock waste
                cut_assignment = CutAssignment(demand_id=demand[0], length=demand[1])
                stock[2].append(cut_assignment) # append to stock cuts
                stock[3] = stock[3] - demand[1] - group.kerf # calculate waste
                is_assigned = True
                break

        if is_assigned:
            continue

        for i, stock in enumerate(expanded_stocks):
            if demand[1] <= stock[1]:
                cut_assignment = CutAssignment(demand_id=demand[0], length=demand[1])
                prepare_usages.append([
                    stock[0], # stock id
                    stock[1], # stock length
                    [cut_assignment], # stock cuts
                    stock[1] - demand[1] # stock waste
                ])
                expanded_stocks.pop(i)
                is_assigned = True
                break

        if is_assigned:
            continue
        
        for item in prepare_unmet:
            if demand[0] == item[0]: # check if current demand already in prepare_unmet
                item[2] = item[2] + 1
                is_assigned = True
                break

        if is_assigned:
            continue

        new_item = [
            demand[0], # demand id
            demand[1], # length
            1, # quantity
        ]
        prepare_unmet.append(new_item)

    # build result
    usages: list[StockUsage] = []
    for item in prepare_usages:
        usages.append(StockUsage(
            stock_id=item[0],
            stock_length=item[1],
            cuts=item[2],
            waste=item[3]
        ))
    
    unmet: list[UnmetDemand] = []
    for item in prepare_unmet:
        unmet.append(UnmetDemand(
            demand_id=item[0],
            length=item[1],
            quantity=item[2]
        ))

    return GroupSolveResult(
        group=group.group,
        usages=usages,
        unmet=unmet
    )

if __name__ == "__main__":
    from model.internal_model import DemandItem, StockItem
    # group = GroupInput(
    #     group="A",
    #     demands=[
    #         DemandItem("d1", "A", 100, 3),
    #     ],
    #     stocks=[
    #         StockItem("s1", "A", 500, 1),
    #     ],
    #     kerf=0,
    # )

    group = GroupInput(
        group="A",
        demands=[
            DemandItem("d1", "A", 100, 2),
        ],
        stocks=[
            StockItem("s1", "A", 205, 1),
        ],
        kerf=10,
    )

    result = solve_group(group)
