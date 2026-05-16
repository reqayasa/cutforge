from model.internal_model import GroupInput
from model.solver_model import SolveResult
from service.solver_core import solve_group


def solve_all(groups: list[GroupInput]) -> SolveResult:
    result = [solve_group(group) for group in groups]
    return SolveResult(groups=result)