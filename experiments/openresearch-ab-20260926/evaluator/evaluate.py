"""External, standard-library evaluator for the JSONL optimization pilot.

The fixture snapshot contains only fixture/. Keep this file outside agent workspaces.
Windows is required because subprocess limits use a Windows Job Object.
"""

from __future__ import annotations

import argparse
import ctypes
from ctypes import wintypes
import hashlib
import json
import msvcrt
import os
from pathlib import Path
import statistics
import subprocess
import sys
import tempfile
import time


DEV_SEEDS = (0x51A7, 0x92D3, 0xC65F)
HOLDOUT_ENV = "OPENRESEARCH_HOLDOUT_SEEDS"
DEFAULT_SOLUTION = Path(__file__).resolve().parent.parent / "fixture" / "solution.py"


class JobError(RuntimeError):
    pass


if os.name == "nt":
    SIZE_T = ctypes.c_size_t
    ULONG_PTR = ctypes.c_size_t

    class JOBOBJECT_BASIC_LIMIT_INFORMATION(ctypes.Structure):
        _fields_ = [
            ("PerProcessUserTimeLimit", ctypes.c_longlong),
            ("PerJobUserTimeLimit", ctypes.c_longlong),
            ("LimitFlags", wintypes.DWORD),
            ("MinimumWorkingSetSize", SIZE_T),
            ("MaximumWorkingSetSize", SIZE_T),
            ("ActiveProcessLimit", wintypes.DWORD),
            ("Affinity", ULONG_PTR),
            ("PriorityClass", wintypes.DWORD),
            ("SchedulingClass", wintypes.DWORD),
        ]

    class IO_COUNTERS(ctypes.Structure):
        _fields_ = [(name, ctypes.c_ulonglong) for name in (
            "ReadOperationCount", "WriteOperationCount", "OtherOperationCount",
            "ReadTransferCount", "WriteTransferCount", "OtherTransferCount",
        )]

    class JOBOBJECT_EXTENDED_LIMIT_INFORMATION(ctypes.Structure):
        _fields_ = [
            ("BasicLimitInformation", JOBOBJECT_BASIC_LIMIT_INFORMATION),
            ("IoInfo", IO_COUNTERS),
            ("ProcessMemoryLimit", SIZE_T),
            ("JobMemoryLimit", SIZE_T),
            ("PeakProcessMemoryUsed", SIZE_T),
            ("PeakJobMemoryUsed", SIZE_T),
        ]

    class STARTUPINFOW(ctypes.Structure):
        _fields_ = [
            ("cb", wintypes.DWORD), ("lpReserved", wintypes.LPWSTR),
            ("lpDesktop", wintypes.LPWSTR), ("lpTitle", wintypes.LPWSTR),
            ("dwX", wintypes.DWORD), ("dwY", wintypes.DWORD),
            ("dwXSize", wintypes.DWORD), ("dwYSize", wintypes.DWORD),
            ("dwXCountChars", wintypes.DWORD), ("dwYCountChars", wintypes.DWORD),
            ("dwFillAttribute", wintypes.DWORD), ("dwFlags", wintypes.DWORD),
            ("wShowWindow", wintypes.WORD), ("cbReserved2", wintypes.WORD),
            ("lpReserved2", ctypes.POINTER(ctypes.c_byte)),
            ("hStdInput", wintypes.HANDLE), ("hStdOutput", wintypes.HANDLE),
            ("hStdError", wintypes.HANDLE),
        ]

    class PROCESS_INFORMATION(ctypes.Structure):
        _fields_ = [
            ("hProcess", wintypes.HANDLE), ("hThread", wintypes.HANDLE),
            ("dwProcessId", wintypes.DWORD), ("dwThreadId", wintypes.DWORD),
        ]

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.CreateJobObjectW.argtypes = [ctypes.c_void_p, wintypes.LPCWSTR]
    kernel32.CreateJobObjectW.restype = wintypes.HANDLE
    kernel32.SetInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD]
    kernel32.SetInformationJobObject.restype = wintypes.BOOL
    kernel32.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
    kernel32.AssignProcessToJobObject.restype = wintypes.BOOL
    kernel32.QueryInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD, ctypes.c_void_p]
    kernel32.QueryInformationJobObject.restype = wintypes.BOOL
    kernel32.TerminateJobObject.argtypes = [wintypes.HANDLE, wintypes.UINT]
    kernel32.TerminateJobObject.restype = wintypes.BOOL
    kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
    kernel32.CloseHandle.restype = wintypes.BOOL
    kernel32.CreateProcessW.argtypes = [
        wintypes.LPCWSTR, wintypes.LPWSTR, ctypes.c_void_p, ctypes.c_void_p,
        wintypes.BOOL, wintypes.DWORD, ctypes.c_void_p, wintypes.LPCWSTR,
        ctypes.POINTER(STARTUPINFOW), ctypes.POINTER(PROCESS_INFORMATION),
    ]
    kernel32.CreateProcessW.restype = wintypes.BOOL
    kernel32.ResumeThread.argtypes = [wintypes.HANDLE]
    kernel32.ResumeThread.restype = wintypes.DWORD
    kernel32.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
    kernel32.WaitForSingleObject.restype = wintypes.DWORD
    kernel32.GetExitCodeProcess.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)]
    kernel32.GetExitCodeProcess.restype = wintypes.BOOL
    kernel32.TerminateProcess.argtypes = [wintypes.HANDLE, wintypes.UINT]
    kernel32.TerminateProcess.restype = wintypes.BOOL

    JOB_OBJECT_LIMIT_JOB_MEMORY = 0x200
    JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE = 0x2000
    JobObjectExtendedLimitInformation = 9


def _check(ok: object, operation: str) -> None:
    if not ok:
        raise JobError(f"{operation} failed: {ctypes.WinError(ctypes.get_last_error())}")


class WindowsJob:
    def __init__(self, memory_mib: int):
        if os.name != "nt":
            raise JobError("This evaluator requires Windows Job Objects")
        self.handle = kernel32.CreateJobObjectW(None, None)
        _check(self.handle, "CreateJobObjectW")
        limits = JOBOBJECT_EXTENDED_LIMIT_INFORMATION()
        limits.BasicLimitInformation.LimitFlags = (
            JOB_OBJECT_LIMIT_JOB_MEMORY | JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        )
        limits.JobMemoryLimit = memory_mib * 1024 * 1024
        try:
            _check(kernel32.SetInformationJobObject(
                self.handle, JobObjectExtendedLimitInformation,
                ctypes.byref(limits), ctypes.sizeof(limits),
            ), "SetInformationJobObject")
        except BaseException:
            self.close()
            raise

    def assign(self, process_handle: int) -> None:
        _check(kernel32.AssignProcessToJobObject(self.handle, process_handle),
               "AssignProcessToJobObject")

    def peak_bytes(self) -> int:
        info = JOBOBJECT_EXTENDED_LIMIT_INFORMATION()
        _check(kernel32.QueryInformationJobObject(
            self.handle, JobObjectExtendedLimitInformation,
            ctypes.byref(info), ctypes.sizeof(info), None,
        ), "QueryInformationJobObject")
        return int(info.PeakJobMemoryUsed)

    def terminate(self) -> None:
        _check(kernel32.TerminateJobObject(self.handle, 1), "TerminateJobObject")

    def close(self) -> None:
        if self.handle:
            kernel32.CloseHandle(self.handle)
            self.handle = None


def run_limited(command: list[str], *, cwd: Path, timeout_sec: float,
                memory_mib: int) -> dict:
    """Run a process tree under one Job Object and return observed process data."""
    child_env = os.environ.copy()
    child_env.pop(HOLDOUT_ENV, None)
    job = WindowsJob(memory_mib)
    process = PROCESS_INFORMATION()
    try:
        with open(os.devnull, "rb") as stdin, tempfile.TemporaryFile() as stdout, tempfile.TemporaryFile() as stderr:
            handles = [msvcrt.get_osfhandle(stream.fileno()) for stream in (stdin, stdout, stderr)]
            for handle in handles:
                os.set_handle_inheritable(handle, True)
            startup = STARTUPINFOW()
            startup.cb = ctypes.sizeof(startup)
            startup.dwFlags = 0x100  # STARTF_USESTDHANDLES
            startup.hStdInput, startup.hStdOutput, startup.hStdError = handles
            environment = ctypes.create_unicode_buffer(
                "\0".join(f"{key}={value}" for key, value in sorted(child_env.items())) + "\0\0"
            )
            command_line = ctypes.create_unicode_buffer(subprocess.list2cmdline(command))
            start = time.perf_counter()
            try:
                _check(kernel32.CreateProcessW(
                    command[0], command_line, None, None, True,
                    0x00000004 | 0x00000400 | 0x08000000,  # suspended, Unicode env, no window
                    environment, str(cwd), ctypes.byref(startup), ctypes.byref(process),
                ), "CreateProcessW")
            finally:
                for handle in handles:
                    os.set_handle_inheritable(handle, False)
            try:
                try:
                    job.assign(process.hProcess)
                except BaseException:
                    kernel32.TerminateProcess(process.hProcess, 1)
                    kernel32.WaitForSingleObject(process.hProcess, 5000)
                    raise
                if kernel32.ResumeThread(process.hThread) == 0xFFFFFFFF:
                    _check(False, "ResumeThread")
                wait_result = kernel32.WaitForSingleObject(
                    process.hProcess, max(1, int(timeout_sec * 1000))
                )
                timed_out = wait_result == 0x102  # WAIT_TIMEOUT
                if timed_out:
                    job.terminate()
                    _check(kernel32.WaitForSingleObject(process.hProcess, 5000) == 0,
                           "WaitForSingleObject after timeout")
                elif wait_result != 0:
                    _check(False, "WaitForSingleObject")
                elapsed = time.perf_counter() - start
                exit_code = wintypes.DWORD()
                _check(kernel32.GetExitCodeProcess(process.hProcess, ctypes.byref(exit_code)),
                       "GetExitCodeProcess")
                peak = job.peak_bytes()
                stdout.seek(0)
                stderr.seek(0)
                return {
                    "returncode": exit_code.value,
                    "timed_out": timed_out,
                    "elapsed_sec": round(elapsed, 6),
                    "peak_job_memory_bytes": peak,
                    "stdout": stdout.read(2000).decode("utf-8", "replace"),
                    "stderr": stderr.read(2000).decode("utf-8", "replace"),
                }
            finally:
                kernel32.CloseHandle(process.hThread)
                kernel32.CloseHandle(process.hProcess)
    finally:
        job.close()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def next_state(state: int) -> int:
    state ^= (state << 13) & 0xFFFFFFFF
    state ^= state >> 17
    state ^= (state << 5) & 0xFFFFFFFF
    return state & 0xFFFFFFFF


def generate_input(path: Path, seed: int, rows: int) -> None:
    """Make varied but reproducible JSONL; no global RNG or external data."""
    state = seed & 0xFFFFFFFF
    if not state:
        raise ValueError("seed low 32 bits must be nonzero")
    tenants = [f"tenant-{i:04d}" for i in range(512)] + ["北区", "équipe", "😀"]
    with path.open("w", encoding="utf-8", newline="\n") as target:
        for i in range(rows):
            state = next_state(state)
            tenant = tenants[state % len(tenants)]
            amount = ((state >> 7) % 200001) - 100000
            ok = (True, False, 1, "true", None, True, False, True)[(state >> 25) & 7]
            values = {
                "tenant": tenant, "amount_cents": amount, "ok": ok,
                "ignored": f"ñ-{i % 97}" if i % 11 == 0 else i % 97,
            }
            names = (
                ("ok", "tenant", "amount_cents", "ignored"),
                ("ignored", "amount_cents", "tenant", "ok"),
                ("tenant", "ok", "ignored", "amount_cents"),
            )[i % 3]
            row = {name: values[name] for name in names}
            separators = (", ", ": ") if i % 17 == 0 else (",", ":")
            target.write(json.dumps(row, ensure_ascii=False, separators=separators) + "\n")


def make_oracle(input_path: Path) -> bytes:
    """Compute reference bytes in evaluator memory, never in the candidate's directory."""
    counts: dict[str, int] = {}
    sums: dict[str, int] = {}
    with input_path.open("r", encoding="utf-8") as stream:
        for line in stream:
            item = json.loads(line)
            if type(item["ok"]) is bool and item["ok"]:
                key = item["tenant"]
                counts[key] = counts.get(key, 0) + 1
                sums[key] = sums.get(key, 0) + item["amount_cents"]
    lines = []
    for key in sorted(counts.keys()):
        quoted_key = json.dumps(key, ensure_ascii=False)
        lines.append(
            f'{{"tenant":{quoted_key},"count":{counts[key]},'
            f'"amount_cents":{sums[key]}}}\n'
        )
    return "".join(lines).encode("utf-8")


def first_difference(expected: bytes, actual: Path) -> int | None:
    offset = 0
    with actual.open("rb") as stream:
        while offset < len(expected):
            observed = stream.read(min(65536, len(expected) - offset))
            reference = expected[offset:offset + len(observed)]
            for index, (left, right) in enumerate(zip(reference, observed)):
                if left != right:
                    return offset + index
            offset += len(observed)
            if not observed:
                return offset
        return offset if stream.read(1) else None


def grade_output(observation: dict, expected: bytes, output_path: Path) -> dict:
    result: dict = {}
    if observation["timed_out"]:
        result["status"] = "timeout"
    elif observation["returncode"] != 0:
        result["status"] = "nonzero_exit"
    elif observation["stdout"]:
        result["status"] = "unexpected_stdout"
    elif not output_path.is_file():
        result["status"] = "missing_output"
    else:
        result["output_sha256"] = sha256_file(output_path)
        difference = first_difference(expected, output_path)
        result["status"] = "pass" if difference is None else "mismatch"
        if difference is not None:
            result["first_differing_byte"] = difference
    if result["status"] != "pass":
        result["stderr_excerpt"] = observation["stderr"]
        result["stdout_excerpt"] = observation["stdout"]
    return result


def write_edge_cases(root: Path) -> list[tuple[str, Path, bytes, int]]:
    """Fixed small contract cases shared by development and confirmation."""
    escaped = '北区\n"\\é😀'
    cases: list[tuple[str, list[dict]]] = [
        ("empty", []),
        ("no_boolean_true", [
            {"tenant": "skipped", "amount_cents": 9, "ok": value}
            for value in (False, 1, "true", 0, None, [], {})
        ]),
        ("escaped_unicode_tenant", [
            {"ok": True, "tenant": escaped, "amount_cents": 4, "ignored": "extra"},
            {"tenant": escaped, "amount_cents": -1, "ok": True},
            {"tenant": "A\tB", "ok": True, "amount_cents": 3},
            {"tenant": "😀", "ok": False, "amount_cents": 100},
        ]),
        ("empty_tenant", [
            {"tenant": "", "ok": True, "amount_cents": 8},
            {"tenant": "", "ok": True, "amount_cents": -3},
            {"tenant": "z", "ok": True, "amount_cents": 1},
            {"tenant": "", "ok": False, "amount_cents": 100},
        ]),
        ("large_signed_sums", [
            {"tenant": "large", "ok": True, "amount_cents": 10**40},
            {"tenant": "large", "ok": True, "amount_cents": -(10**40) + 7},
            {"tenant": "negative", "ok": True, "amount_cents": -(10**35)},
            {"tenant": "positive", "ok": True, "amount_cents": 10**35},
        ]),
    ]
    paths = []
    for case_id, rows in cases:
        input_path = root / f"edge-{case_id}.input.jsonl"
        with input_path.open("w", encoding="utf-8", newline="\n") as target:
            for row in rows:
                target.write(json.dumps(row, ensure_ascii=True, separators=(",", ":")) + "\n")
        expected = make_oracle(input_path)
        paths.append((case_id, input_path, expected, len(rows)))
    return paths


def parse_holdouts() -> tuple[int, int]:
    raw = os.environ.get(HOLDOUT_ENV, "")
    try:
        values = tuple(int(value.strip(), 0) for value in raw.split(","))
    except ValueError as error:
        raise ValueError(f"{HOLDOUT_ENV} must contain two comma-separated integers") from error
    if (len(values) != 2 or values[0] == values[1] or
            (values[0] & 0xFFFFFFFF) == (values[1] & 0xFFFFFFFF) or
            any(value < 1 or (value & 0xFFFFFFFF) == 0 for value in values)):
        raise ValueError(f"{HOLDOUT_ENV} must contain two distinct positive seeds with nonzero low 32 bits")
    if any((value & 0xFFFFFFFF) in DEV_SEEDS for value in values):
        raise ValueError("holdout seeds must differ from all development seeds")
    return values


def check_invalid_invocations(solution: Path, root: Path, *, timeout_sec: float,
                              memory_mib: int) -> list[dict]:
    missing = root / "intentionally-missing-input.jsonl"
    if missing.exists():
        raise ValueError("missing-input test path unexpectedly exists")
    checks = (
        ("no_arguments", [sys.executable, "-B", str(solution)]),
        ("missing_input", [sys.executable, "-B", str(solution), str(missing),
                           str(root / "missing-input.actual.jsonl")]),
    )
    results = []
    for name, command in checks:
        observation = run_limited(command, cwd=solution.parent,
                                  timeout_sec=timeout_sec, memory_mib=memory_mib)
        status = ("timeout" if observation["timed_out"] else
                  "pass" if observation["returncode"] != 0 else "returned_zero")
        results.append({
            "id": name, "command": command, "status": status,
            "returncode": observation["returncode"],
            "elapsed_sec": observation["elapsed_sec"],
            "peak_job_memory_bytes": observation["peak_job_memory_bytes"],
        })
    return results


def evaluate(args: argparse.Namespace) -> dict:
    solution = args.solution.resolve(strict=True)
    if args.mode == "confirm":
        if not args.operator_confirm:
            raise ValueError("confirm requires --operator-confirm and private holdout seeds")
        seeds = parse_holdouts()
    else:
        seeds = DEV_SEEDS
    seed_ids = ("holdout-1", "holdout-2") if args.mode == "confirm" else (
        "dev-1", "dev-2", "dev-3")
    initial_hash = sha256_file(solution)
    report: dict = {
        "schema_version": 1,
        "mode": args.mode,
        "solution_path": str(solution),
        "solution_sha256": initial_hash,
        "evaluator_sha256": sha256_file(Path(__file__)),
        "config": {"rows_per_dataset": args.rows, "repeats": args.repeats,
                   "timeout_sec": args.timeout_sec, "job_memory_mib": args.memory_mib},
        "invocation_checks": [],
        "edge_cases": [],
        "datasets": [],
        "failures": [],
    }
    with tempfile.TemporaryDirectory(prefix="openresearch-eval-") as temporary:
        temp = Path(temporary)
        report["invocation_checks"] = check_invalid_invocations(
            solution, temp, timeout_sec=args.timeout_sec, memory_mib=args.memory_mib
        )
        for check in report["invocation_checks"]:
            if check["status"] != "pass":
                report["failures"].append({"invocation_check": check["id"],
                                           "status": check["status"]})
        for case_id, input_path, expected, count in write_edge_cases(temp):
            output_path = temp / f"edge-{case_id}.actual.jsonl"
            command = [sys.executable, "-B", str(solution), str(input_path), str(output_path)]
            observation = run_limited(command, cwd=solution.parent,
                                      timeout_sec=args.timeout_sec,
                                      memory_mib=args.memory_mib)
            edge = {
                "id": case_id, "rows": count,
                "input_sha256": sha256_file(input_path),
                "expected_sha256": hashlib.sha256(expected).hexdigest(),
                "command": command,
                "returncode": observation["returncode"],
                "elapsed_sec": observation["elapsed_sec"],
                "peak_job_memory_bytes": observation["peak_job_memory_bytes"],
            }
            edge.update(grade_output(observation, expected, output_path))
            if edge["status"] != "pass":
                report["failures"].append({"edge_case": case_id, "status": edge["status"]})
            report["edge_cases"].append(edge)
        for dataset_id, seed in zip(seed_ids, seeds):
            input_path = temp / f"{dataset_id}.input.jsonl"
            generate_input(input_path, seed, args.rows)
            expected = make_oracle(input_path)
            size = input_path.stat().st_size
            dataset: dict = {
                "id": dataset_id,
                "seed": seed if args.mode == "dev" else None,
                "rows": args.rows,
                "input_bytes": size,
                "input_sha256": sha256_file(input_path),
                "expected_sha256": hashlib.sha256(expected).hexdigest(),
                "runs": [],
            }
            for repeat in range(args.repeats):
                output_path = temp / f"{dataset_id}.run-{repeat + 1}.jsonl"
                command = [sys.executable, "-B", str(solution), str(input_path), str(output_path)]
                observation = run_limited(command, cwd=solution.parent,
                                          timeout_sec=args.timeout_sec,
                                          memory_mib=args.memory_mib)
                run = {
                    "repeat": repeat + 1,
                    "command": command,
                    "returncode": observation["returncode"],
                    "elapsed_sec": observation["elapsed_sec"],
                    "rows_per_sec": round(args.rows / observation["elapsed_sec"], 2),
                    "input_mib_per_sec": round(size / 1048576 / observation["elapsed_sec"], 2),
                    "peak_job_memory_bytes": observation["peak_job_memory_bytes"],
                }
                run.update(grade_output(observation, expected, output_path))
                if run["status"] != "pass":
                    report["failures"].append({"dataset": dataset_id, "repeat": repeat + 1,
                                               "status": run["status"]})
                dataset["runs"].append(run)
            passed_times = [run["elapsed_sec"] for run in dataset["runs"] if run["status"] == "pass"]
            dataset["median_pass_elapsed_sec"] = (
                round(statistics.median(passed_times), 6) if passed_times else None
            )
            report["datasets"].append(dataset)
    final_hash = sha256_file(solution)
    if final_hash != initial_hash:
        report["failures"].append({"status": "solution_changed_during_evaluation"})
    report["solution_sha256_after"] = final_hash
    report["overall_status"] = "pass" if not report["failures"] else "fail"
    return report


def self_test() -> dict:
    """Exercise real process limits and incorrect-solution grading."""
    with tempfile.TemporaryDirectory(prefix="openresearch-watchdog-") as temporary:
        root = Path(temporary)
        pid_file = root / "child.pid"
        child_code = (
            "import os, pathlib, subprocess, sys, time; "
            "p=subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(30)']); "
            "pathlib.Path(sys.argv[1]).write_text(str(p.pid)); time.sleep(30)"
        )
        timeout = run_limited([sys.executable, "-c", child_code, str(pid_file)],
                              cwd=root, timeout_sec=0.7, memory_mib=64)
        child_gone = False
        if pid_file.exists() and os.name == "nt":
            pid = int(pid_file.read_text())
            PROCESS_SYNCHRONIZE = 0x00100000
            kernel32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
            kernel32.OpenProcess.restype = wintypes.HANDLE
            kernel32.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
            kernel32.WaitForSingleObject.restype = wintypes.DWORD
            handle = kernel32.OpenProcess(PROCESS_SYNCHRONIZE, False, pid)
            if not handle:
                child_gone = True
            else:
                child_gone = kernel32.WaitForSingleObject(handle, 1000) == 0
                kernel32.CloseHandle(handle)
        allocation = [sys.executable, "-c", "bytearray(128*1024*1024)"]
        memory = run_limited(allocation, cwd=root, timeout_sec=10, memory_mib=64)
        control = run_limited(allocation, cwd=root, timeout_sec=10, memory_mib=512)
        memory_enforced = (memory["returncode"] != 0 and
                           "MemoryError" in memory["stderr"] and
                           control["returncode"] == 0)
        input_path = root / "grading.input.jsonl"
        input_path.write_bytes(b"")
        expected = b'expected\n'
        mismatch_script = root / "wrong_output.py"
        mismatch_script.write_text(
            "import sys\nfrom pathlib import Path\n"
            "Path(sys.argv[2]).write_bytes(b'wrong\\n')\n", encoding="utf-8"
        )
        mismatch_output = root / "wrong.actual.jsonl"
        mismatch = run_limited(
            [sys.executable, "-B", str(mismatch_script), str(input_path), str(mismatch_output)],
            cwd=root, timeout_sec=5, memory_mib=64,
        )
        mismatch_status = grade_output(mismatch, expected, mismatch_output)["status"]
        exit_script = root / "exit_one.py"
        exit_script.write_text("raise SystemExit(1)\n", encoding="utf-8")
        exit_output = root / "exit.actual.jsonl"
        exit_one = run_limited(
            [sys.executable, "-B", str(exit_script), str(input_path), str(exit_output)],
            cwd=root, timeout_sec=5, memory_mib=64,
        )
        exit_status = grade_output(exit_one, expected, exit_output)["status"]
        stdout_script = root / "prints_stdout.py"
        stdout_script.write_text(
            "import sys\nfrom pathlib import Path\n"
            "Path(sys.argv[2]).write_bytes(b'expected\\n')\n"
            "print('unexpected output')\n", encoding="utf-8"
        )
        stdout_output = root / "stdout.actual.jsonl"
        stdout_run = run_limited(
            [sys.executable, "-B", str(stdout_script), str(input_path), str(stdout_output)],
            cwd=root, timeout_sec=5, memory_mib=64,
        )
        stdout_status = grade_output(stdout_run, expected, stdout_output)["status"]
        invocation_checks = check_invalid_invocations(
            DEFAULT_SOLUTION, root, timeout_sec=5, memory_mib=64
        )
        invalid_invocations_rejected = all(check["status"] == "pass" for check in invocation_checks)
        passed = (timeout["timed_out"] and child_gone and memory_enforced and
                  mismatch_status == "mismatch" and
                  exit_status == "nonzero_exit" and exit_one["returncode"] == 1 and
                  stdout_status == "unexpected_stdout" and invalid_invocations_rejected)
        return {
            "schema_version": 1,
            "overall_status": "pass" if passed else "fail",
            "timeout_triggered": timeout["timed_out"],
            "child_terminated": child_gone,
            "memory_limit_enforced": memory_enforced,
            "memory_test_returncode": memory["returncode"],
            "memory_test_peak_job_memory_bytes": memory["peak_job_memory_bytes"],
            "memory_control_returncode": control["returncode"],
            "wrong_output_status": mismatch_status,
            "exit_one_status": exit_status,
            "exit_one_returncode": exit_one["returncode"],
            "unexpected_stdout_status": stdout_status,
            "invalid_invocations_rejected": invalid_invocations_rejected,
        }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("dev", "confirm", "selftest"))
    parser.add_argument("--solution", type=Path, default=DEFAULT_SOLUTION)
    parser.add_argument("--rows", type=int, default=1_800_000)
    parser.add_argument("--repeats", type=int, default=2)
    parser.add_argument("--timeout-sec", type=float, default=120)
    parser.add_argument("--memory-mib", type=int, default=512)
    parser.add_argument("--operator-confirm", action="store_true")
    parser.add_argument("--output", type=Path, help="write report JSON to this path")
    args = parser.parse_args()
    if os.name != "nt":
        parser.error("Windows is required for Job Object process limits")
    if not (1 <= args.rows <= 10_000_000 and 1 <= args.repeats <= 20 and
            0 < args.timeout_sec <= 120 and 16 <= args.memory_mib <= 512):
        parser.error("limits: rows 1..10,000,000, repeats 1..20, timeout (0,120], memory 16..512 MiB")
    try:
        report = self_test() if args.mode == "selftest" else evaluate(args)
    except (OSError, ValueError, JobError) as error:
        parser.error(str(error))
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 0 if report["overall_status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
