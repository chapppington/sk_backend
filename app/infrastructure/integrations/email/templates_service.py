from pathlib import Path

from jinja2 import (
    Environment,
    FileSystemLoader,
)

from presentation.api.v1.submissions.schemas import SubmissionCreatedEventSchema


class EmailTemplatesService:
    def __init__(self, template_dir: Path | None = None):
        if template_dir is None:
            template_dir = Path(__file__).parent / "templates"

        self.jinja_env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            autoescape=False,
        )

    def render_submission_email(self, event: SubmissionCreatedEventSchema) -> str:
        template = self.jinja_env.get_template("email_submission.html")
        return template.render(event=event)
