import requests
import zipfile
import argparse
from time import sleep
from pathlib import Path
from os import access, X_OK
from typing import Optional

DEFAULT_PATH = Path.home() / ".chromedriver"


def options_menu(options, prompt, param_name="option", default=-1, prompt_display_secs=2, selection_display_secs=1):
    """
    Display a menu of options and prompt the user to select one.
    """
    selected = None
    while selected is None:
        print(prompt)
        sleep(prompt_display_secs)
        for i, option in enumerate(options):
            print(f"({i+1}) {option}")
        print()
        default_option = options[default]
        selected = input(
            f"Enter 1-{len(options)} to select a {param_name} (default: {options.index(default_option) + 1} {default_option}): "
        )
        if not selected:
            selected = default
        elif selected in options:
            selected = options.index(selected)
        elif not selected.isdigit() or int(selected) < 1 or int(selected) > len(options):
            print(f"\nInvalid {param_name} number: {selected}. Enter 1-{len(options)}")
            sleep(2)
            selected = None
        else:
            selected = int(selected) - 1

    selection = options[selected]
    print(f"\nSelected {param_name}: {selection}")
    sleep(selection_display_secs)
    return selection


def select_chromedriver(
    version_number: Optional[int] = None, headless: Optional[bool] = None, platform: Optional[str] = None
) -> tuple[str, str]:
    """
    Select the chromedriver version and platform to download. Return the filename and download URL.
    """
    versions_url = (
        "https://googlechromelabs.github.io/chrome-for-testing/latest-versions-per-milestone-with-downloads.json"
    )
    versions = requests.get(versions_url).json()
    milestones = versions["milestones"]

    version_options = [f"Version {ms}" for ms in milestones if milestones[ms]["downloads"].get("chromedriver")]
    version_q = f"""
Which chrome version number do you have installed?
Open chrome and go to:
    chrome://settings/help
you will see a version number like Version 121.0.6167.85 (Official Build) (x86_64)
which corresponds to chromedriver version 121

Available chromedriver versions:"""
    selected_version = version_number or options_menu(version_options, version_q, "version number", -1).split(" ")[1]
    if int(selected_version) >= 120:
        headless = headless or input("Do you want to use the headless version of chromedriver? (y/n): ").lower() == "y"
    else:
        headless = False
    executable = "chromedriver" if not headless else "chrome-headless-shell"

    platform_options = [download["platform"] for download in milestones[selected_version]["downloads"][executable]]
    platform_q = "Which platform are you using?\n\nAvailable platforms:"
    platform = platform or options_menu(platform_options, platform_q, "platform", 0)

    filename = f"{executable}{selected_version}-{platform}.zip"
    for download in milestones[selected_version]["downloads"][executable]:
        if download["platform"] == platform:
            download_url = download["url"]
            print(f"Found download for {filename} at {download_url}")
            return filename, download_url

    raise ValueError(f"Could not find download for {filename}")


def download_chromedriver(filename: str, download_url: str, destdir: Optional[Path] = None):
    """
    Download the chromedriver zip file from the download URL and save it to the destination directory.
    """
    if not destdir:
        destdir_input = input(f"Where do you want to save {filename}? (default: {DEFAULT_PATH / filename}): ").rstrip(
            "/"
        )
        if not destdir_input:
            destdir = DEFAULT_PATH.resolve()
        else:
            destdir = Path(destdir_input).resolve()
    else:
        destdir = destdir.resolve()

    if not destdir.exists():
        print(f"Creating {destdir}...")
        destdir.mkdir(parents=True)

    print(f"Downloading {filename} from {download_url}...")
    destpath = destdir / filename
    with destpath.open("wb") as f:
        f.write(requests.get(download_url).content)
    print(f"Downloaded {filename} to {destpath}")

    print(f"Extracting {filename} to {destdir}...")
    with zipfile.ZipFile(destpath, "r") as zip_ref:
        zip_ref.extractall(destdir)

    executable_path = next(path for path in destdir.rglob("*chrome*") if path.is_file() and path.suffix == "")
    return executable_path


def try_make_executable(executable_path: Path):
    """
    Try to make the chromedriver executable. Return True if successful, False otherwise.
    """
    try:
        print(f"Making {executable_path} executable...")
        executable_path.chmod(0o755)
    except Exception as e:
        print(f"Failed to make {executable_path} executable. Error: {e}")

    return access(executable_path, X_OK)


def get_chromedriver() -> Optional[Path]:
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", type=int, help="Chromedriver version number")
    parser.add_argument("-p", "--platform", type=str, help="Platform to download chromedriver for")
    parser.add_argument("-d", "--destdir", type=Path, help="Directory to save chromedriver to")
    parser.add_argument("--headless", action="store_true", help="Use headless version of chromedriver")
    args = parser.parse_args()

    try:
        filename, download_url = select_chromedriver(args.version, args.headless, args.platform)
    except ValueError as e:
        print(e)
        return None

    try:
        executable_path = download_chromedriver(filename, download_url, args.destdir)
    except Exception as e:
        print("Failed to download and extract chromedriver. Error: ", e)
        return None

    print("Success. Chromedriver executable downloaded and saved to:\n", executable_path)

    if not try_make_executable(executable_path):
        print("\nFailed to make chromedriver executable. You may need to do this manually.")
        print("\nTo make the chromedriver executable, run the following command:")
        print(f"chmod +x {executable_path}\n")
    else:
        print("Chromedriver is now executable.")

    print("\nYou can now use the chromedriver with SouperScraper. For example:")
    print("from souperscraper import SouperScraper")
    print(f'scraper = SouperScraper("{executable_path!s}")')
    print("scraper.goto('https://example.com')")
    print("header = scraper.soup.find('h1').text")
    return executable_path


def main():
    try:
        get_chromedriver()
    except KeyboardInterrupt:
        print("\nExiting...")


if __name__ == "__main__":
    main()
