"""
Test the matrix functionality
"""

from junit2htmlreport import matrix
from junit2htmlreport.matrix import PARTIAL_PASS, PARTIAL_FAIL, TOTAL_FAIL, UNTESTED
from junit2htmlreport.parser import PASSED, SKIPPED, FAILED, UNKNOWN


from .inputfiles import get_filepath


def test_combined_result():
    """
    Test that the combined result string and short result value are correct
    :return:
    """
    textmatrix = matrix.TextReportMatrix()
    short, result = textmatrix.combined_result([PASSED, SKIPPED])

    assert short == textmatrix.short_outcome(PASSED)
    assert result == PASSED.title()

    short, result = textmatrix.combined_result([PASSED, FAILED])
    assert short == textmatrix.short_outcome(PARTIAL_FAIL)
    assert result == PARTIAL_FAIL.title()

    short, result = textmatrix.combined_result([PARTIAL_PASS])
    assert short == textmatrix.short_outcome(PARTIAL_PASS)
    assert result == PARTIAL_PASS.title()

    short, result = textmatrix.combined_result([TOTAL_FAIL])
    assert short == textmatrix.short_outcome(TOTAL_FAIL)
    assert result == TOTAL_FAIL.title()

    short, result = textmatrix.combined_result([FAILED, FAILED])
    assert short == textmatrix.short_outcome(FAILED)
    assert result == FAILED.title()

    short, result = textmatrix.combined_result([PASSED])
    assert short == textmatrix.short_outcome(PASSED)
    assert result == PASSED.title()

    short, result = textmatrix.combined_result([SKIPPED, SKIPPED])
    assert short == textmatrix.short_outcome(UNTESTED)
    assert result == UNTESTED.title()

    short, result = textmatrix.combined_result([])
    assert '?' == textmatrix.short_outcome(None) # type: ignore
    assert result == UNKNOWN.title()


def test_matrix_load(tmpdir):
    """
    Test loading multiple reports
    :return:
    """
    textmatrix = matrix.TextReportMatrix()
    textmatrix.add_report(get_filepath("junit-simple_suite.xml"))
    textmatrix.add_report(get_filepath("junit-simple_suites.xml"))
    textmatrix.add_report(get_filepath("junit-unicode.xml"))
    textmatrix.add_report(get_filepath("junit-unicode2.xml"))
    textmatrix.add_report(get_filepath("junit-cute2.xml"))
    textmatrix.add_report(get_filepath("junit-jenkins-stdout.xml"))

    assert len(textmatrix.reports) == 6

    result = textmatrix.summary()

    print(result)


def test_matrix_html(tmpdir):
    """
    Test loading multiple reports
    :return:
    """
    htmatrix = matrix.HtmlReportMatrix(str(tmpdir))
    htmatrix.add_report(get_filepath("junit-simple_suite.xml"))
    htmatrix.add_report(get_filepath("junit-simple_suites.xml"))
    htmatrix.add_report(get_filepath("junit-unicode.xml"))
    htmatrix.add_report(get_filepath("junit-axis-linux.xml"))
    assert len(htmatrix.reports) == 4
    result = htmatrix.summary()
    assert result.endswith("</html>")

