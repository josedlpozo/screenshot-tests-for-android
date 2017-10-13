import os
from os.path import join


class Reporter:
    def __init__(self, path, results, report_file_name):
        self._path = path
        self._results = results
        self.html = """
        <!doctype html>
        <html>
        <head>
            <title>Verify results</title>
            <link href="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css" rel="stylesheet">
            <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
        </head>
        <body>
        <main class="container">
            <div class="section">
                <table class="responsive-table">
                    <thead>
                    <h3>Verify results</h3>
                    {1}
                    <tr>
                        <th>Test name</th>
                        <th>Screenshot expected</th>
                        <th>Screenshot actual</th>
                        <th>Screenshot diff</th>
                    </tr>
                    </thead>
                    <tbody>
                    {0}
                    </tbody>
                </table>
            </div>
        </main>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js"></script>
        </body>
        </html>
        """
        self._report_file_name = report_file_name

    def generate(self):
        body = ""
        for result in self._results:
            test_name = result.test_name

            expected_path = os.path.relpath(result.expected_path, self._path)
            actual_path = os.path.relpath(result.actual_path, self._path)

            if result.is_passed():
                body += self._positive_row(test_name, expected_path, actual_path)
            else:
                diff_path = os.path.relpath(result.diff_path, self._path)
                body += self._negative_row(test_name, expected_path, actual_path, diff_path)

            body += "\n\n"

        with open(join(self._path, self._report_file_name), "w") as report:
            report.write(self.html.format(body, self._test_results(self._results)))

    def _positive_row(self, test_name, expected_path, actual_path):
        positive_row = """
                        <tr>
                            <th>
                                <p class='green-text'>{0}</p>
                            </th>
                            <th>
                                <a href='{1}'><img width='200' src='{1}'/></a>
                            </th>
                            <th>
                                <a href='{2}'><img width='200' src='{2}'/></a>
                            </th>
                        </tr>
                        """
        return positive_row.format(test_name, expected_path, actual_path)

    def _negative_row(self, test_name, expected_path, actual_path, diff_path):
        break_test_row = """
                    <tr>
                        <th>
                            <p class='red-text'>{0}</p>
                        </th>
                        <th>
                            <a href='{1}'><img width='200' src='{1}'/></a>
                        </th>
                        <th>
                            <a href='{2}'><img width='200' src='{2}'/></a>
                        </th>
                        <th>
                            <a href='{3}'><img width='200' src='{3}'/></a>
                        </th>
                    </tr>
                    """
        return break_test_row.format(test_name, expected_path, actual_path, diff_path)

    def _test_results(self, results):
        passed = 0
        not_passed = 0

        for result in results:
            if result.is_passed():
                passed += 1
            else:
                not_passed += 1

        total_tests = len(results)
        if total_tests is passed:
            return "<h5>All tests have passed</h5>"
        elif total_tests is not_passed:
            return "<h5>None of the tests have passed</h5>"
        else:
            return "<h5>{0} tests have passed.\n {1} tests have errors.</h5>".format(passed, not_passed)
