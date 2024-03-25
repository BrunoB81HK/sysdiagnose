import semver.version


__all__ = (
    "v13",
    "get_version",
    "Version",
)


v13 = semver.version.Version(13)


def get_version(version: str) -> semver.version.Version:
    return semver.version.Version.parse(version)


Version = semver.version.Version
