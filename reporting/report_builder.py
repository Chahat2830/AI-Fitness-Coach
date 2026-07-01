from reporting.report_models import AnalysisReport


class ReportBuilder:
    """
    Builds one complete analysis report.
    """

    def __init__(self):

        self.report = AnalysisReport()

    # ------------------------------------

    def set_user(self, user):

        self.report.user = user

        return self

    # ------------------------------------

    def set_measurements(self, measurements):

        self.report.measurements = measurements

        return self

    # ------------------------------------

    def set_metrics(self, metrics):

        self.report.metrics = metrics

        return self

    # ------------------------------------

    def set_score(self, score):

        self.report.score = score

        return self

    # ------------------------------------

    def set_ai(self, ai):

        self.report.ai_analysis = ai

        return self

    # ------------------------------------

    def set_workout(self, workout):

        self.report.workout = workout

        return self

    # ------------------------------------

    def set_diet(self, diet):

        self.report.diet = diet

        return self

    # ------------------------------------

    def set_images(self, images):

        self.report.images = images

        return self

    # ------------------------------------

    def build(self):

        return self.report