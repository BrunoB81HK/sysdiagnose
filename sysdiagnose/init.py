import argparse
import hashlib
import pathlib
import re
import tarfile

import yaml

from . import config


logger = config.logger.getChild("init")

__sysdiagnose_archive_glob_file_map = {
    "sysdiagnose.log": "./*/sysdiagnose.log",
    "ps": "./*/ps.txt",
    "swcutil_show": "./*/swcutil_show.txt",
    "ps_thread": "./*/ps_thread.txt",
    "appupdate_db": "./*/logs/appinstallation/AppUpdates.sqlitedb",
    "brctl": "./*/brctl/",
    "networkextensioncache": "./*/logs/Networking/com.apple.networkextension.cache.plist",
    "networkextension": "./*/logs/Networking/com.apple.networkextension.plist",
    "powerlogs": "./*/logs/powerlogs/powerlog_*",
    "systemversion": "./*/logs/SystemVersion/SystemVersion.plist",
    "UUIDToBinaryLocations": "./*/logs/tailspindb/UUIDToBinaryLocations",
    "logarchive_folder": "./*/system_logs.logarchive/",
    "shutdownlog": "./*/system_logs.logarchive/Extra/shutdown.log",
    "taskinfo": "./*/taskinfo.txt",
    "spindump-nosymbols": "./*/spindump-nosymbols.txt",
    "Accessibility-TCC": "./*/logs/Accessibility/TCC.db",
    "appinstallation": "./*/logs/appinstallation/appstored.sqlitedb",
    "itunesstore": "./*/./logs/itunesstored/downloads.*.sqlitedb",
    "wifisecurity": "./*/WiFi/security.txt",
}


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "init",
        help="Initialize a sysdiagnose analysis.",
    )
    parser.add_argument(
        "file",
        metavar="SYSDIAGNOSE_FILE",
        type=pathlib.Path,
        help="the sysdiagnose archive file",
    )
    parser.add_argument("-f", "--force", action="store_true", help="force the re-initialization")
    parser.set_defaults(func=main)


def main(args: argparse.Namespace) -> int:
    if not args.file.exists():
        logger.error(f"'{args.file.as_posix()}' not found")
        return 1

    return init(args.file, args.force)


def init(sysdiagnose_file: pathlib.Path, force: bool) -> int:
    logger.info(f"Processing {sysdiagnose_file.as_posix():s}...")

    # Open the cases file.
    cases = yaml.safe_load(config.cases_file.read_text())["cases"]

    # Calculate sha256 of sysdiagnose archive and compare with past cases.
    file_bytes = sysdiagnose_file.read_bytes()
    readable_hash = hashlib.sha256(file_bytes).hexdigest()
    case_id = readable_hash[:8]
    logger.debug(f"hash: {readable_hash:s}")
    logger.debug(f"case id: {case_id:s}")

    if case_id in cases and not force:
        logger.error(
            f"This sysdiagnose archive has already been extracted (case id: {case_id:s}), "
            "to re-extract, use the '-f' or '--force' option."
        )
        return 1

    # Test sysdiagnose archive.
    try:
        tf = tarfile.open(sysdiagnose_file)
    except Exception as e:
        logger.error(f"Error opening sysdiagnose file. (reason: {e:s})")
        return 1

    # Create case folders and file.
    new_data_folder = config.data_path / case_id
    new_parsed_folder = config.parsed_data_path / case_id
    case_file = new_data_folder.with_suffix(".yaml")
    new_data_folder.mkdir(parents=True, exist_ok=True)
    new_parsed_folder.mkdir(parents=True, exist_ok=True)

    # Create case dictionnary.
    cases[case_id] = {
        "source_file": sysdiagnose_file,
        "source_sha256": readable_hash,
        "case_file": case_file,
    }

    # Extract the sysdiagnose archive's files.
    try:
        tf.extractall(new_data_folder)
    except Exception as e:
        logger.error(f"Error while decompressing sysdiagnose file. (reason: {e:s})")

    # Create case json file.
    new_case_json = {key: next(new_data_folder.glob(glb), None) for key, glb in __sysdiagnose_archive_glob_file_map.items()}

    # Wifi data listing.
    new_case_json["wifi_data"] = [
        *new_data_folder.glob("./*/WiFi/*.plist"),
        *new_data_folder.glob("./*/WiFi/wifi_scan*.txt"),
        *new_data_folder.glob("./*/WiFi/com.apple.wifi.recent-networks.json"),
    ]

    # ips files.
    new_case_json["ips_files"] = list(new_data_folder.glob("./*/crashes_and_spins/*.ips"))

    # mobile activation logs.
    new_case_json["mobile_activation"] = list(new_data_folder.glob("./*/logs/MobileActivation/mobileactivationd.log*"))

    # container manager.
    new_case_json["container_manager"] = list(new_data_folder.glob("./*/logs/MobileContainerManager/containermanagerd.log*"))

    # mobile installation.
    new_case_json["mobile_installation"] = list(new_data_folder.glob("./*/logs/MobileInstallation/mobile_installation.log*"))

    # Get iOS version
    if ret := re.search(
        r"iPhone OS (\d+\.\d+\.\d+)",
        new_case_json["sysdiagnose.log"].read_text(),
    ):
        new_case_json["ios_version"] = ret.group(1)
    else:
        logger.error("Could not retrieve the iOS version...")
        # return 1

    # Sve the new case file.
    case_file.write_text(yaml.safe_dump(new_case_json))

    # Update cases file.
    config.cases_file.write_text(yaml.safe_dump({"cases": cases}))

    logger.info("Sysdiagnose file has been processed.")
    logger.info(f"New case id: {case_id:s}")
