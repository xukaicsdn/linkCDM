import logging
from string import Template

import pytest
from _pytest.reports import BaseReport

logger = logging.getLogger("pytest_result_log")

__test_set = set()

template = ""
level_map = {}
enable_plugin = True


def pytest_cmdline_parse():
    global __test_set

    __test_set = set()


def pytest_addoption(parser):
    parser.addini(
        "result_log",
        type="bool",
        default=True,
        help="用例执行结果的日志格式",
    )
    parser.addini(
        "result_log_format",
        default="test status is ${result} (${case_id}): ${reason}",
        help="用例执行结果的日志格式",
    )
    parser.addini(
        "result_log_passed",
        default="info",
        help="用例执行通过的的日志等级",
    )
    parser.addini(
        "result_log_failed",
        default="error",
        help="用例执行失败的的日志等级",
    )
    parser.addini(
        "result_log_error",
        default="error",
        help="用例执行出错的的日志等级",
    )
    parser.addini(
        "result_log_skipped",
        default="warning",
        help="用例执行跳过的的日志等级",
    )
    parser.addini(
        "result_log_xpass",
        default="warning",
        help="用例意外通过的的日志等级",
    )
    parser.addini(
        "result_log_xfail",
        default="warning",
        help="用例逾期失败的的日志等级",
    )


def pytest_configure(config):
    global template, level_map, enable_plugin
    enable_plugin = config.getini("result_log")

    template = config.getini("result_log_format")
    level_map = {
        "PASSED": config.getini("result_log_passed"),
        "FAILED": config.getini("result_log_failed"),
        "ERROR": config.getini("result_log_error"),
        "SKIPPED": config.getini("result_log_skipped"),
        "XPASS": config.getini("result_log_xpass"),
        "XFAIL": config.getini("result_log_xfail"),
    }


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_report_teststatus(report: BaseReport):
    outcome = yield

    if not enable_plugin:
        return

    result = outcome.get_result()

    if report.nodeid in __test_set:
        return

    if report.when == "setup":
        match result[1]:
            case "s":
                log(report.nodeid, result[2], *get_reason(report, "s"))
            case "E":
                log(report.nodeid, result[2], *get_reason(report, "E"))

    if report.when == "call":

        match result[1]:
            case ".":
                log(report.nodeid, result[2])
            case "F" | "x":
                log(report.nodeid, result[2], *get_reason(report, "F"))
            case "X":
                log(report.nodeid, result[2])


def get_reason(report: BaseReport, result="F"):
    reason = "unknown"

    match result:
        case "F":
            try:
                reason = report.longrepr.reprtraceback.reprentries[
                    -1
                ].reprfileloc.message
            except Exception:
                ...
        case "E":
            try:
                reason = report.longrepr.errorstring.split("\n")[0]
            except Exception:
                ...
        case "s":
            try:
                reason = report.longrepr[2]
            except Exception:
                ...

    return reason, report.longreprtext


def log(case_id, result, reason=None, detail=None):
    level = level_map.get(result, "warning").lower()
    f = getattr(logger, level)
    f(Template(template).safe_substitute(**locals()))

    if detail:
        logger.debug(f"{case_id} -> {detail}")

    __test_set.add(case_id)
