"""Execute only bootstrap snippets, using synthetic tools and an isolated home."""

from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
MACHINE = ROOT / "docs/machine.md"


def section(text, heading):
    return text.split(f"## {heading}\n", 1)[1].split("\n## ", 1)[0]


def snippets(text):
    return "\n".join(re.findall(r"```sh\n(.*?)```", text, re.S))


STUB = r'''
import os
from pathlib import Path
import shlex
import sys

root = Path(os.environ["BOOTSTRAP_FIXTURE"])
name = Path(sys.argv[0]).name
args = sys.argv[1:]
with (root / "calls").open("a") as calls:
    calls.write(name + " " + " ".join(args) + "\n")

def require(marker):
    if not (root / marker).exists():
        sys.exit("missing prerequisite: " + marker)

if name == "brew":
    if args == ["shellenv"]:
        print("export PATH=" + shlex.quote(str(root / "prefix/bin")) + ':"$PATH"')
    elif args == ["--version"]:
        print("Homebrew synthetic")
    elif args[:1] == ["install"]:
        for package in args[1:]:
            (root / (package + "-installed")).touch()
    else:
        sys.exit("unexpected brew command")
elif name == "sops":
    require("sops-installed")
    require("initialized")
    if args != ["--decrypt", str(root / "source/example.enc.yaml")]:
        sys.exit("unexpected decryption command")
    (root / "decrypted").touch()
elif name == "chezmoi":
    require("chezmoi-installed")
    if args == ["init", "fixture-repo"]:
        (root / "initialized").touch()
    elif args == ["init", "--apply", "fixture-repo"]:
        if os.environ["ENCRYPTED"] == "1":
            sys.exit("premature encrypted apply")
        (root / "applied").touch()
    elif args == ["source-path"]:
        require("initialized")
        print(root / "source")
    elif args == ["diff"]:
        require("decrypted")
        (root / "inspected").touch()
    elif args == ["apply"]:
        require("inspected")
        (root / "applied").touch()
    else:
        sys.exit("unexpected chezmoi command")
'''


class BootstrapDocsTests(unittest.TestCase):
    def run_snippets(self, script, *, encrypted=True, bootstrap=False):
        with tempfile.TemporaryDirectory(prefix="bootstrap docs ") as directory:
            root = Path(directory)
            binary = root / "prefix/bin"
            binary.mkdir(parents=True)
            (root / "home").mkdir()
            (root / "empty-path").mkdir()
            (root / "source").mkdir()
            (root / "source/example.enc.yaml").write_text("synthetic ciphertext\n")
            for name in ("brew", "chezmoi", "sops"):
                tool = binary / name
                tool.write_text(f"#!{sys.executable}\n" + STUB)
                tool.chmod(0o755)
            script = script.replace('brew_prefix="/opt/homebrew"',
                                    "brew_prefix=" + shlex.quote(str(root / "prefix")))
            script = script.replace("<your-dotfiles-repo>", "fixture-repo")
            script = script.replace("<encrypted-file>", "example.enc.yaml")
            result = subprocess.run(
                [shutil.which("sh"), "-eu", "-c", script],
                cwd=root,
                env={"HOME": str(root / "home"),
                     "PATH": str(root / "empty-path" if bootstrap else binary),
                     "BOOTSTRAP_FIXTURE": str(root),
                     "ENCRYPTED": "1" if encrypted else "0"},
                text=True, capture_output=True, timeout=10,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(list((root / "home").iterdir()), [])
            return (root / "calls").read_text().splitlines(), result.stdout

    def test_homebrew_shellenv_before_first_install(self):
        text = MACHINE.read_text()
        # The installer itself is never executed. Start immediately after it.
        brew_blocks = re.findall(r"```sh\n(.*?)```", section(text, "Install Homebrew"), re.S)
        install = snippets(section(text, "Install chezmoi early")).splitlines()[0]
        calls, output = self.run_snippets("\n".join(brew_blocks[1:]) + "\n" + install, bootstrap=True)
        self.assertEqual(calls, ["brew shellenv", "brew --version", "brew install chezmoi"])
        self.assertIn("/prefix/bin/brew", output)

    def test_encrypted_init_decrypt_inspect_apply_order(self):
        text = MACHINE.read_text()
        setup = section(text, "Install chezmoi early")
        encrypted = section(text, "Configure SOPS before applying encrypted dotfiles")
        encrypted = encrypted.split("### Dotfiles without encrypted files", 1)[0]
        calls, _ = self.run_snippets(snippets(setup) + "\n" + snippets(encrypted))
        self.assertEqual(calls[:4], ["brew install chezmoi", "chezmoi init fixture-repo",
                                    "brew install sops", "chezmoi source-path"])
        self.assertTrue(calls[4].startswith("sops --decrypt "))
        self.assertTrue(calls[4].endswith("/source/example.enc.yaml"))
        self.assertEqual(calls[5:], ["chezmoi diff", "chezmoi apply"])

    def test_unencrypted_combined_init_apply(self):
        text = MACHINE.read_text()
        setup = section(text, "Install chezmoi early")
        # A top-to-bottom reader must choose the shortcut before plain init.
        shortcut = "[Dotfiles without encrypted files](#dotfiles-without-encrypted-files)"
        self.assertLess(setup.index(shortcut), setup.index("chezmoi init <your-dotfiles-repo>"))
        checklist = section((ROOT / "docs/setup.md").read_text(), "7. Install chezmoi and apply dotfiles")
        self.assertLess(checklist.index("chezmoi init --apply <your-dotfiles-repo>"),
                        checklist.index("chezmoi init <your-dotfiles-repo>"))
        install = snippets(setup).splitlines()[0]
        unencrypted = text.split("### Dotfiles without encrypted files\n", 1)[1].split("\n## ", 1)[0]
        calls, _ = self.run_snippets(install + "\n" + snippets(unencrypted), encrypted=False)
        self.assertEqual(calls, ["brew install chezmoi", "chezmoi init --apply fixture-repo"])

    def test_local_links_and_anchors(self):
        for source in (ROOT / "README.md", ROOT / "docs/setup.md", MACHINE,
                       ROOT / "docs/python.md"):
            for url in re.findall(r"\[[^\]]+\]\(([^)]+)\)", source.read_text()):
                parsed = urlsplit(url)
                if parsed.scheme or parsed.netloc:
                    continue
                target = source.parent / unquote(parsed.path) if parsed.path else source
                self.assertTrue(target.is_file(), f"{source}: {url}")
                if parsed.fragment:
                    content = re.sub(r"```.*?```", "", target.read_text(), flags=re.S)
                    headings = re.findall(r"^#+ (.+)$", content, re.M)
                    anchors = []
                    for heading in headings:
                        slug = re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
                        anchor = slug
                        suffix = 0
                        while anchor in anchors:
                            suffix += 1
                            anchor = f"{slug}-{suffix}"
                        anchors.append(anchor)
                    self.assertIn(unquote(parsed.fragment), anchors, f"{source}: {url}")


if __name__ == "__main__":
    unittest.main()
