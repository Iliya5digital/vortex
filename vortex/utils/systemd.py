from __future__ import annotations
from typing import Optional

from pathlib import Path, PurePosixPath

from vortex.output.base import Output, Device


def deploy_service(
    output: Output,
    file: Path,
    name: Optional[str] = None,
    enable: bool = False,
) -> None:
    if name is not None:
        service = name + ".service"
    else:
        assert file.suffix == ".service"
        service = file.name

    systemd = PurePosixPath("/etc/systemd/system")
    output.mkdir(systemd, exist_ok=True, recursive=True)
    output.copy(file, systemd / service)

    if enable:
        wants = "multi-user.target.wants"
        output.mkdir(systemd / wants, exist_ok=True)
        output.link(PurePosixPath(systemd / wants / service), systemd / service)


def restart_service(output: Device, name: str) -> None:
    output.run(["systemctl", "daemon-reload"])
    output.run(["systemctl", "restart", name])
