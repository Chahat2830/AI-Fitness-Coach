import json
from pathlib import Path


class ReportExporter:
    """
    Export reports into different formats.

    Version 1:
        JSON

    Future:
        PDF
        HTML
        DOCX
    """

    # -------------------------------------

    @staticmethod
    def export_json(

        report,

        output_path,

    ):

        output_path = Path(output_path)

        output_path.parent.mkdir(

            parents=True,

            exist_ok=True

        )

        with open(

            output_path,

            "w",

            encoding="utf-8"

        ) as f:

            json.dump(

                report.to_dict(),

                f,

                indent=4,

                ensure_ascii=False

            )

        return output_path

    # -------------------------------------

    @staticmethod
    def export_html(

        report,

        output_path,

    ):

        raise NotImplementedError(

            "HTML export coming soon."

        )

    # -------------------------------------

    @staticmethod
    def export_pdf(

        report,

        output_path,

    ):

        raise NotImplementedError(

            "PDF export coming soon."

        )

    # -------------------------------------

    @staticmethod
    def export_docx(

        report,

        output_path,

    ):

        raise NotImplementedError(

            "DOCX export coming soon."

        )