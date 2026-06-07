from model.internal_model import GroupInput
from model.solver_model import SolveResult
from service.solver_core import solve_group


def solve_all(groups: list[GroupInput]) -> SolveResult:
    result = [solve_group(group) for group in groups]
    if not groups:
        return SolveResult(groups=result, kerf=0, unit_scale=0)
    return SolveResult(groups=result, kerf=groups[0].stocks, unit_scale=groups[0].unit_scale)