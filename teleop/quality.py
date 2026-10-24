"""Episode integrity and plain-language quality report; no task-success inference."""
from pathlib import Path
import html
import json
import numpy as np
from .recording import read_episode


def inspect_quality(episode, require_npz=True):
    path = Path(episode)
    result = {"episode": str(path.resolve()), "integrity_passed": False,
              "errors": [], "warnings": [], "task_success": None,
              "scope": "simulation data integrity, not physical accuracy or task success"}
    try:
        meta, rows = read_episode(path)
        result["task_success"] = meta.get("success")
        result["software_version"] = meta.get("software_version", "not recorded (historical sample)")
        result["backend"] = meta.get("backend")
        result["human_collected"] = meta.get("human_collected")
        t = np.array([r["t_robot_s"] for r in rows])
        q = np.array([r["observation.q"] for r in rows])
        a = np.array([r["action.q"] for r in rows])
        active = np.array([r["mode"] == "ACTIVE" for r in rows])
        paired = active[1:] & active[:-1]
        duration = float(t[-1] - t[0])
        states = {mode: sum(r["mode"] == mode for r in rows)
                  for mode in ("DISARMED", "ACTIVE", "HOLD", "ESTOP", "FAULT")}
        result.update(rows=len(rows), joints=q.shape[1], active_rows=int(active.sum()),
            state_counts=states, timestamp_span_s=duration,
            sample_frequency_hz=(len(rows)-1)/duration if duration > 0 else None,
            period_p95_ms=float(np.percentile(np.diff(t), 95)*1000) if len(t)>1 else None,
            observation_vs_previous_action_rmse_rad=float(np.sqrt(np.mean((q[1:][paired]-a[:-1][paired])**2))) if paired.any() else None,
            observed_joint_range_rad=np.ptp(q, axis=0).tolist(),
            complete=True, checksum_verified=True, config_checksum_verified=True)
        if not active.any():
            result["warnings"].append("没有 ACTIVE 数据：这段记录不能展示有效跟随。")
        elif float(np.max(np.ptp(q[active], axis=0))) < 1e-4:
            result["warnings"].append("ACTIVE 区间几乎没有运动，请再采集一次小幅关节操作。")
        if states["FAULT"]:
            result["warnings"].append("记录含 FAULT 状态，请查看 summary.json 中的原因。")
        if meta.get("success") is None:
            result["warnings"].append("任务成功尚未标注；完整保存不代表任务成功。")
        if meta.get("human_collected") is not True:
            result["warnings"].append("没有已确认的人工采集身份，不自动作为人类示教数据。")
        npz = path / "episode.npz"
        if npz.exists():
            expected = {"observation": q, "action": a,
                "target": np.array([r["target.q"] for r in rows]), "timestamp": t,
                "gripper_observation": np.array([r["observation.gripper"] for r in rows]),
                "gripper_action": np.array([r["action.gripper"] for r in rows]), "valid": active}
            with np.load(npz, allow_pickle=False) as data:
                for name, value in expected.items():
                    if name not in data or not np.array_equal(data[name], value):
                        raise ValueError("NPZ 与原始日志不一致：" + name)
                if data["valid"].dtype != np.dtype(bool):
                    raise ValueError("NPZ valid 必须是布尔数组")
                if json.loads(str(data["metadata_json"].item())) != meta:
                    raise ValueError("NPZ 元数据与 metadata.json 不一致")
            result["npz_matches_jsonl"] = True
        elif require_npz:
            raise ValueError("缺少 episode.npz，请先完成导出")
        else:
            result["npz_matches_jsonl"] = None
        summary = path / "summary.json"
        if summary.exists():
            summary_data = json.loads(summary.read_text(encoding="utf-8"))
            if summary_data.get("error") or summary_data.get("complete") is False:
                raise ValueError("summary 报告运行/保存未完成：" + str(summary_data.get("error")))
        result["integrity_passed"] = True
    except (OSError, ValueError, KeyError, TypeError, OverflowError) as exc:
        result["errors"].append(str(exc))
    return result


def write_quality_report(episode, output=None, require_npz=True):
    result = inspect_quality(episode, require_npz=require_npz)
    out = Path(output) if output else Path(episode) / "quality-report"
    out.mkdir(parents=True, exist_ok=False)
    (out / "report.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    label = "数据完整性检查通过" if result["integrity_passed"] else "检查未通过，请保留原始文件"
    values = [("记录位置", result["episode"]), ("总行数", result.get("rows")),
              ("ACTIVE 行数", result.get("active_rows")), ("关节数", result.get("joints")),
              ("时间戳跨度 / 秒", result.get("timestamp_span_s")),
              ("采样时间戳平均频率 / Hz", result.get("sample_frequency_hz")),
              ("周期 P95 / ms", result.get("period_p95_ms")),
              ("仿真关节 RMSE / rad", result.get("observation_vs_previous_action_rmse_rad")),
              ("任务成功标签", "未标注" if result.get("task_success") is None else result["task_success"])]
    table = ''.join('<tr><th>'+html.escape(k)+'</th><td>'+html.escape(str(v))+'</td></tr>' for k,v in values)
    notes = ''.join('<li>'+html.escape(x)+'</li>' for x in result["errors"]+result["warnings"])
    page = '<!doctype html><meta charset="utf-8"><title>轨迹检查报告</title><style>body{max-width:900px;margin:40px auto;padding:20px;font:17px/1.8 sans-serif;color:#203543}table{border-collapse:collapse;width:100%}td,th{padding:10px;border:1px solid #ccc;text-align:left;overflow-wrap:anywhere}h1{color:'+('#087f70' if result['integrity_passed'] else '#b03035')+'}</style>'
    page += '<h1>'+label+'</h1><p>这是仿真数据检查，不是实体机械臂精度或任务成功验收。</p><table>'+table+'</table><h2>需要了解的结果</h2><ul>'+notes+'</ul><p>target 是想去的位置；action 是下发目标；observation 是执行前状态。RMSE 只使用相邻两行均为 ACTIVE 的观测与上一拍动作。</p>'
    (out / "report.html").write_text(page, encoding="utf-8")
    return result, out
