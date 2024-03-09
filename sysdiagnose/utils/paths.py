import pathlib

__all__ = (
    "app_config_path",
    "data_path",
    "parsed_data_path",
    "log_file",
    "cases_file",
)

# == Paths === #
app_config_path = pathlib.Path.home() / ".local" / "share" / "sysdiagnose"
data_path = app_config_path / "data"
parsed_data_path = app_config_path / "parsed_data"
log_file = app_config_path / "app.log"
cases_file = app_config_path / "cases.yaml"

# Initialize the cases file.
app_config_path.mkdir(parents=True, exist_ok=True)
data_path.mkdir(parents=True, exist_ok=True)
parsed_data_path.mkdir(parents=True, exist_ok=True)
log_file.touch(exist_ok=True)
if not cases_file.exists():
    cases_file.write_text("cases: {}")
