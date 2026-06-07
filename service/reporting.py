from model.solver_model import SolveResult
from model.report_model import (
    SolveReport, 
    StockReportRow, 
    UnmetReportRow,
    StockUsageReport,
)


def build_report(result: SolveResult) -> SolveReport:
    stock_report_rows: list[StockReportRow] = []
    unmet_report_rows: list[UnmetReportRow] = []
    stock_usage_report: list[StockUsageReport] = []
    usage_id = 0
    for group_result in result.groups:
        for usage in group_result.usages:
            stock_report_rows.append(StockReportRow(
                group           = group_result.group,
                stock_id        = usage.stock_id,
                stock_length    = usage.stock_length,
                used_length     = sum(cut.length for cut in usage.cuts),
                waste           = usage.waste,
                cut_count       = len(usage.cuts)
            ))
        for unmet in group_result.unmet:
            unmet_report_rows.append(UnmetReportRow(
                group           = group_result.group,
                demand_id       = unmet.demand_id,
                length          = unmet.length,
                quantity        = unmet.quantity
            ))
        for usage in group_result.usages:
            stock_usage_report.append(StockUsageReport(
                usage_id        = usage_id,
                group           = group_result.group,
                stock_id        = usage.stock_id,
                stock_length    = usage.stock_length,
                used_length     = sum(cut.length for cut in usage.cuts),
                waste           = usage.waste,
                cuts            = usage.cuts
            ))
            usage_id += 1

    return SolveReport(
        usages=stock_usage_report,
        unmet_rows=unmet_report_rows,
        unit_scale=result.unit_scale,
        # summary=...
    )


    




