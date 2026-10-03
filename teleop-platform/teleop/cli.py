import argparse
import json
import os
from pathlib import Path
import secrets
from .config import load_config
from .mapping import fit_calibration
from .simulation import run_sim
from .network import serve, client
from .recording import export_npz, read_episode


def main():
    p = argparse.ArgumentParser(description="GELLO遥操作参考工程：仿真与数据采集，真机运动未开放")
    sub = p.add_subparsers(dest="command", required=True)
    s = sub.add_parser("sim")
    s.add_argument("--output", required=True)
    s.add_argument("--config")
    s.add_argument("--duration", type=float, default=6)
    s.add_argument("--delay-ms", type=float, default=5)
    s.add_argument("--jitter-ms", type=float, default=1)
    s.add_argument("--loss", type=float, default=0)
    s.add_argument("--blackout-at", type=float)
    s.add_argument("--seed", type=int, default=7)
    s.add_argument("--backend", choices=["toy","mujoco","panda"], default="toy")
    s.add_argument("--realtime", action="store_true")
    s.add_argument("--viewer", action="store_true")
    for name in ("server", "client"):
        s = sub.add_parser(name)
        s.add_argument("--config")
        s.add_argument("--keyfile", required=True)
        s.add_argument("--host", default="127.0.0.1")
        s.add_argument("--port", type=int, default=8765)
        s.add_argument("--duration", type=float, default=30)
        if name == "server":
            s.add_argument("--output", required=True)
            s.add_argument("--backend", choices=["toy","mujoco","panda"], default="toy")
        else:
            s.add_argument("--virtual", action="store_true")
            s.add_argument("--gello-config")
            s.add_argument("--calibration")
    s = sub.add_parser("keygen")
    s.add_argument("path")
    s = sub.add_parser("calibrate")
    s.add_argument("input", help="JSON containing leader and follower matrices")
    s.add_argument("output")
    s = sub.add_parser("export")
    s.add_argument("episode")
    s.add_argument("output")
    s = sub.add_parser("inspect")
    s.add_argument("episode")
    s = sub.add_parser("ui",help="本地 Panda 人工控制和采集界面")
    s.add_argument("--output",required=True)
    s.add_argument("--port",type=int,default=8080)
    s.add_argument("--open-browser",action="store_true")
    a = vars(p.parse_args())
    command = a.pop("command")
    if command == "ui":
        from .manual import serve_manual
        result=serve_manual(**a)
    elif command in ("sim", "server", "client"):
        config_path = a.pop("config")
        if config_path is None and a.get("backend") == "panda":
            from .panda import panda_config
            config = panda_config()
        else:
            config = load_config(config_path)
        result = {"sim":run_sim,"server":serve,"client":client}[command](config, **a)
    elif command == "keygen":
        fd = os.open(a["path"], os.O_WRONLY|os.O_CREAT|os.O_EXCL, 0o600)
        with os.fdopen(fd, "wb") as f:
            f.write(secrets.token_bytes(32))
        result = {"created":a["path"]}
    elif command == "calibrate":
        data = json.loads(Path(a["input"]).read_text())
        mapping, rms = fit_calibration(data["leader"], data["follower"])
        with open(a["output"],"x",encoding="utf-8") as f:
            json.dump(mapping,f,indent=2)
        result = {"calibration_fit_rmse_rad":rms,"independent_validation_required":True}
    elif command == "export":
        export_npz(a["episode"],a["output"])
        result = {"exported":a["output"],"format":"project NPZ schema, not LeRobot/RLDS"}
    else:
        meta, rows = read_episode(a["episode"])
        result = {"metadata":meta,"rows":len(rows)}
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
