import os


class ResultPrinter:
    def __init__(self, printer, results, report_file_path):
        self.printer = printer
        self.results = results
        self.report_file_path = report_file_path

    def print_results(self):
        self.printer.standard("\n\n")
        self.printer.standard("Verify tests results:")

        total_tests = len(self.results)
        self.print_standard_tab("{0} tests have been executed".format(total_tests))

        passed = 0
        not_passed = 0

        for result in self.results:
            if result.is_passed():
                passed += 1
            else:
                not_passed += 1

        self.print_success_tab("{0} have passed".format(passed))

        if not not_passed is 0:
            self.print_fail_tab("{0} have errors".format(not_passed))

        self.printer.standard("\n")

        for result in self.results:
            if result.is_passed():
                self.print_success_tab(result.test_name + " has passed")
            else:
                self.print_fail_tab(result.test_name + " has errors")

        self.printer.standard("\n")
        self.printer.standard("You can review these tests in more detail here: \n ")
        self.print_standard_tab("file://{0}".format(os.path.abspath(self.report_file_path)))

    def tab(self):
        return "    "

    def print_standard_tab(self, text):
        self.printer.standard(self.tab() + text)

    def print_fail_tab(self, text):
        self.printer.fail(self.tab() + text)

    def print_success_tab(self, text):
        self.printer.success(self.tab() + text)
