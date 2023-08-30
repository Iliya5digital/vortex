from __future__ import annotations
from typing import Dict, Optional

from pathlib import Path
from dataclasses import dataclass

from vortex.utils.path import TargetPath, prepend_if_target
from vortex.utils.run import run
from vortex.tasks.base import task, Component, Context
from vortex.tasks.compiler import Gcc


@dataclass
class Make(Component):
    src_dir: Path | TargetPath
    cc: Gcc
    build_target: Optional[str] = None

    def env(self, ctx: Context) -> Dict[str, str]:
        return {
            "CC": str(ctx.target_path / self.cc.bin("gcc")),
        }

    @task
    def build(self, ctx: Context) -> None:
        self.cc.install(ctx)

        run(
            [
                "make",
                *([self.build_target] if self.build_target is not None else []),
                "-j",
                *([str(ctx.jobs)] if ctx.jobs is not None else []),
            ],
            cwd=prepend_if_target(ctx.target_path, self.src_dir),
            env=self.env(ctx),
            quiet=ctx.capture,
        )
