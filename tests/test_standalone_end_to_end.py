from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
EXPORTER = REPOSITORY_ROOT / "scripts" / "create_scaffold.py"


class StandaloneEndToEndTests(unittest.TestCase):
    def run_command(
        self, *command: str, cwd: Path
    ) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            command,
            cwd=cwd,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def write_payload(
        self, payload_directory: Path, name: str, payload: dict[str, object]
    ) -> Path:
        path = payload_directory / name
        path.write_text(
            json.dumps(payload, ensure_ascii=False),
            encoding="utf-8",
        )
        return path

    def test_exported_workspace_writes_sources_checks_continuity_and_builds_epub(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            workspace = root / "novel"
            payloads = root / "payloads"
            payloads.mkdir()

            self.run_command(
                sys.executable,
                str(EXPORTER),
                "--destination",
                str(workspace),
                "--agent",
                "all",
                cwd=REPOSITORY_ROOT,
            )

            skill_root = workspace / ".agents" / "skills"
            source_payloads = (
                (
                    "create-setting",
                    "write_setting.py",
                    "setting.json",
                    {
                        "slug": "clock-city",
                        "title": "시계 도시",
                        "status": "draft",
                        "rules": ["The central clock loses one minute each night."],
                        "body": {
                            "description": "시간 부채로 움직이는 도시.",
                            "story_pressure": "잃어버린 분이 시민의 기억을 지운다.",
                            "continuity": "중앙 시계는 매일 자정에만 움직인다.",
                        },
                    },
                ),
                (
                    "create-character",
                    "write_character.py",
                    "character.json",
                    {
                        "slug": "mina",
                        "name": "미나",
                        "status": "draft",
                        "role": "protagonist",
                        "body": {
                            "function": "도시가 감춘 시간을 되찾는다.",
                            "continuity": "미나는 멈춘 시계의 소리를 들을 수 있다.",
                        },
                    },
                ),
                (
                    "create-material",
                    "write_material.py",
                    "material.json",
                    {
                        "slug": "broken-watch",
                        "title": "고장 난 회중시계",
                        "status": "draft",
                        "canonical": True,
                        "related_characters": ["char-mina"],
                        "body": {
                            "idea": "자정 직전 한 번만 거꾸로 도는 시계.",
                            "story_use": "잃어버린 시간의 위치를 가리킨다.",
                        },
                    },
                ),
                (
                    "create-plot",
                    "write_plot.py",
                    "plot.json",
                    {
                        "slug": "time-debt",
                        "title": "시간의 빚",
                        "status": "draft",
                        "characters": ["char-mina"],
                        "materials": ["material-broken-watch"],
                        "body": {
                            "promise": "미나는 도시가 훔친 시간을 추적한다.",
                            "pressure": "추적할수록 자신의 기억이 사라진다.",
                            "turns": [
                                "회중시계가 거꾸로 돈다.",
                                "중앙 시계의 문이 열린다.",
                            ],
                        },
                    },
                ),
            )
            for skill, script, payload_name, payload in source_payloads:
                payload_path = self.write_payload(
                    payloads, payload_name, payload
                )
                self.run_command(
                    sys.executable,
                    str(skill_root / skill / "scripts" / script),
                    "--input",
                    str(payload_path),
                    "--project-root",
                    str(workspace),
                    cwd=workspace,
                )

            chapter_payload = self.write_payload(
                payloads,
                "chapter.json",
                {
                    "number": 1,
                    "title": "거꾸로 가는 분침",
                    "slug": "backward-minute-hand",
                    "status": "final",
                    "pov": "char-mina",
                    "timeline": "night-1",
                    "setting": "world-clock-city",
                    "characters": ["char-mina"],
                    "materials": ["material-broken-watch"],
                    "plot_threads": ["plot-time-debt"],
                    "synopsis": "미나는 자정에 열린 중앙 시계의 문을 발견한다.",
                    "draft": (
                        "자정이 되자 회중시계의 분침이 거꾸로 움직였다.\n\n"
                        "*“문이 열렸어.”* 미나가 말했다."
                    ),
                },
            )
            story_scripts = skill_root / "novel-story-telling" / "scripts"
            self.run_command(
                sys.executable,
                str(story_scripts / "write_chapter.py"),
                "--input",
                str(chapter_payload),
                "--project-root",
                str(workspace),
                cwd=workspace,
            )

            continuity = self.run_command(
                sys.executable,
                str(story_scripts / "check_continuity.py"),
                "--project-root",
                str(workspace),
                "--format",
                "json",
                cwd=workspace,
            )
            report = json.loads(continuity.stdout)
            self.assertEqual(report["errors"], 0, report)

            output = workspace / "published" / "smoke.epub"
            publish_script = (
                skill_root / "publish-novel" / "scripts" / "build_epub.py"
            )
            self.run_command(
                sys.executable,
                str(publish_script),
                "--project-root",
                str(workspace),
                "--output",
                "published/smoke.epub",
                "--title",
                "시간의 빚",
                "--author",
                "테스트 작가",
                "--language",
                "ko",
                cwd=workspace,
            )

            self.assertTrue(output.is_file())
            with zipfile.ZipFile(output) as archive:
                chapter = archive.read(
                    "OEBPS/chapters/chapter-001.xhtml"
                ).decode("utf-8")
            self.assertIn("거꾸로 가는 분침", chapter)
            self.assertIn("문이 열렸어.", chapter)
            self.assertNotIn("미나는 자정에 열린", chapter)


if __name__ == "__main__":
    unittest.main()
