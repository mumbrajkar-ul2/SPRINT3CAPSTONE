# IaC evidence

| Field | Value |
|---|---|
| Stage | S04-05 — Infrastructure as code (Challenge 5), Half B |
| Date / version | 2026-10-11, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | PASS. `scripts/bootstrap.ps1` ran on this machine from a fresh folder copy and 15 tests passed. The same steps passed in a Linux Python 3.11 container through `make setup`. The Docker build ran and the container run passed. Owner: Team-Force. |
| Evidence sources | `scripts/bootstrap.ps1`; `scripts/bootstrap.sh`; `Makefile`; `Dockerfile`; `.dockerignore`; `.gitattributes`; `requirements.txt`; `infra/terraform/main.tf`; `infra/terraform/.terraform.lock.hcl`; `docs/05-iac/iac-gap-report.md`; `docs/05-iac/reproducible-setup-guide.md`; the run outputs below |
| Assumptions | The runs used a copy of the working tree, not a `git clone`. The last commit does not hold the S04 work (IG-14), so a clone gives a different tree. The copy left out `.venv`, `.pytest_cache`, `__pycache__`, and `logs/audit.log`. |
| Unresolved issues | macOS was not run. Native Ubuntu was not run, because the WSL Ubuntu here has no `python3-venv` (run H6). Python 3.10 was not run. The CI file still sits below the git root (IG-09). That fix belongs to S04-07. |
| Residual risks | `httpx` is pinned in `requirements.txt`. `jsonschema` is not, and S04-07 owns that pin. A clone of the last commit still lacks the S04 files until the work is committed. There is no `.gitignore`, so a local `terraform apply` inside `infra/terraform/` would leave state files that git does not ignore. |

## What this file is

This file records what Half B changed and the real output of each run. The outputs below were copied from log files written by the commands. They were not typed by hand.

Every secret value in this file is written `<redacted>`. No run printed one.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

## What Half B changed

| Item | File | Change | Finding it answers |
|---|---|---|---|
| 1 | `scripts/bootstrap.ps1` | New. Checks Python is 3.10 or newer, creates `.venv`, installs `requirements.txt`, runs `pytest -q`. Exits 1, 2, 3, or 4 on the step that fails. | IG-03 |
| 1 | `scripts/bootstrap.sh` | New. Same four steps for Linux and macOS. Reads the `PYTHON` variable. | IG-03 |
| 1 | `Makefile` | New `setup` target that runs `bash scripts/bootstrap.sh`. The targets `test`, `smoke`, `etl`, and the empty `package` name are unchanged. | IG-03, IG-04 |
| 1 | `requirements.txt` | One new line: `httpx==0.28.1`. | IG-05 |
| 1 | `.gitattributes` | New. Keeps Unix line endings on `*.sh` and `Dockerfile` when git checks them out on Windows. | Needed by `bootstrap.sh` |
| 2 | `Dockerfile`, `.dockerignore` | New. Base image `python:3.11-slim`, installs `requirements.txt`, runs as a non-root user, command `python -m pytest -q`. | IG-07, IG-10 |
| 3 | `infra/terraform/main.tf` | **Corrected.** See the decision below. | IG-01, IG-02 |
| 3 | `infra/terraform/.terraform.lock.hcl` | New. Written by `terraform init`. Pins the `hashicorp/local` provider at 2.9.1. | IG-02 |
| 4 | `docs/05-iac/evidence.md` | This file. | Gate |

### Decision on `main.tf`

Half B item 3 offers two choices: correct the file, or leave it and write `docs/ADR/0002-terraform-gap.md`. **This stage corrected the file. No ADR was written.**

The old file wrote `shared_user=app_shared` into `generated-env.txt` (IG-01). The new file declares three variables: `output_file`, `log_level`, and `api_port`. It writes `LOG_LEVEL` and `API_PORT` only. It holds no user name, no password, no key, and no token. It pins the Terraform version (`>= 1.5.0`) and the provider (`~> 2.5`), validates the two settings, and sets the file mode to `0644`.

`docs/04-secrets/remediation-plan.md` row RP-07 said to leave the user name in `main.tf`. This stage replaces that plan, because the S04-05 playbook asks for a file with no shared user. **Verified Fact.** The RP-07 text is unchanged. This note records that the S04-05 decision comes later.

### Decision on `requirements.txt`

Half B adds `httpx==0.28.1` because the bootstrap cannot pass without it (IG-05). It does not add `jsonschema` and does not move `pytest`, `python-dotenv`, or `PyYAML`. `docs/07-cicd/pipeline-improvement-plan.md` gives those two jobs to S04-07, which also creates `requirements-dev.txt`.

## Results at a glance

| Run | What ran | Where | Result |
|---|---|---|---|
| H1 | `bootstrap.ps1` from a fresh folder copy | Windows 10.0.26200, Python 3.13.5 | Exit code 0. `15 passed, 7 warnings in 2.45s`. 29 seconds from start to finish. |
| H2 | `bootstrap.ps1 -Python "no-such-python"` | Same machine | Exit code 1. The message names the Python command. |
| H3 | `bootstrap.ps1 -Python "py -3.12" -SkipTests` | Same machine | Exit code 0. Python 3.12.10. Tests skipped as asked. |
| H4 | `bootstrap.ps1 -SkipTests` a second time in the same folder | Same machine | Exit code 0. The script reuses `.venv`. |
| H5 | `make setup` from a fresh folder copy | Container `python:3.11-slim`, Python 3.11.17, GNU Make 4.4.1 | Exit code 0. `15 passed, 1 warning in 1.00s`. |
| H6 | `bash scripts/bootstrap.sh` | WSL Ubuntu 22.04.5, Python 3.10.12 | Exit code 2. The venv step fails because `python3-venv` is absent. The message says what to install. |
| H7 | `docker build` then `docker run` | Docker 28.3.2 | Build exit code 0. Run exit code 0. `15 passed, 1 warning in 1.13s`. Image user `app`. Size 152 MB. |
| H8 | `terraform init`, `fmt -check`, `validate`, `apply`, then a bad `plan` | Container `hashicorp/terraform:1.9`, Terraform v1.9.8 | Valid. Applied. The file holds two lines and none of the words `app_shared`, `password`, `token`, `key`, or `secret`. `log_level=TRACE` is refused. |

H1, H7, and H5 used a copy of the finished tree. H2, H3, H4, and H6 used a copy made a few minutes earlier. Between the two copies only `infra/terraform/main.tf` (the file mode lines) and the new lock file changed. Neither file is read by the tests.

**What the numbers mean.** Both Windows runs and the container runs pass the same 15 tests. The warning count is 7 on Python 3.13 and 1 on Python 3.11, the same split as in `reproducible-setup-guide.md`. On Python 3.13, 6 of the 7 warnings come from `datetime.utcnow()` in `apps/api/services/audit.py` line 9, which Python 3.12 and later flag. The seventh is the Starlette `anyio` alias warning. It is the only one that remains on Python 3.11.

## H1. `bootstrap.ps1` on Windows (full output)

Command, from a folder outside the repo, against the fresh copy:

```text
powershell -NoProfile -ExecutionPolicy Bypass -File <copy>\scripts\bootstrap.ps1
```

Output. Exit code 0.

```text
== Step 1 of 4: check Python
Python 3.13.5
== Step 2 of 4: create .venv
Python 3.13.5
== Step 3 of 4: install requirements.txt
Collecting fastapi==0.115.0 (from -r requirements.txt (line 1))
  Using cached fastapi-0.115.0-py3-none-any.whl.metadata (27 kB)
Collecting uvicorn==0.30.6 (from -r requirements.txt (line 2))
  Using cached uvicorn-0.30.6-py3-none-any.whl.metadata (6.6 kB)
Collecting pydantic==2.8.2 (from -r requirements.txt (line 3))
  Using cached pydantic-2.8.2-py3-none-any.whl.metadata (125 kB)
Collecting pytest==8.3.2 (from -r requirements.txt (line 4))
  Using cached pytest-8.3.2-py3-none-any.whl.metadata (7.5 kB)
Collecting python-dotenv==1.0.1 (from -r requirements.txt (line 5))
  Using cached python_dotenv-1.0.1-py3-none-any.whl.metadata (23 kB)
Collecting PyYAML==6.0.2 (from -r requirements.txt (line 6))
  Using cached PyYAML-6.0.2-cp313-cp313-win_amd64.whl.metadata (2.1 kB)
Collecting httpx==0.28.1 (from -r requirements.txt (line 7))
  Using cached httpx-0.28.1-py3-none-any.whl.metadata (7.1 kB)
Collecting starlette<0.39.0,>=0.37.2 (from fastapi==0.115.0->-r requirements.txt (line 1))
  Using cached starlette-0.38.6-py3-none-any.whl.metadata (6.0 kB)
Collecting typing-extensions>=4.8.0 (from fastapi==0.115.0->-r requirements.txt (line 1))
  Using cached typing_extensions-4.16.0-py3-none-any.whl.metadata (3.3 kB)
Collecting annotated-types>=0.4.0 (from pydantic==2.8.2->-r requirements.txt (line 3))
  Using cached annotated_types-0.8.0-py3-none-any.whl.metadata (15 kB)
Collecting pydantic-core==2.20.1 (from pydantic==2.8.2->-r requirements.txt (line 3))
  Using cached pydantic_core-2.20.1-cp313-none-win_amd64.whl.metadata (6.7 kB)
Collecting click>=7.0 (from uvicorn==0.30.6->-r requirements.txt (line 2))
  Using cached click-8.5.0-py3-none-any.whl.metadata (2.6 kB)
Collecting h11>=0.8 (from uvicorn==0.30.6->-r requirements.txt (line 2))
  Using cached h11-0.16.0-py3-none-any.whl.metadata (8.3 kB)
Collecting iniconfig (from pytest==8.3.2->-r requirements.txt (line 4))
  Using cached iniconfig-2.3.1-py3-none-any.whl.metadata (2.8 kB)
Collecting packaging (from pytest==8.3.2->-r requirements.txt (line 4))
  Using cached packaging-26.3-py3-none-any.whl.metadata (3.5 kB)
Collecting pluggy<2,>=1.5 (from pytest==8.3.2->-r requirements.txt (line 4))
  Using cached pluggy-1.6.0-py3-none-any.whl.metadata (4.8 kB)
Collecting colorama (from pytest==8.3.2->-r requirements.txt (line 4))
  Using cached colorama-0.4.6-py2.py3-none-any.whl.metadata (17 kB)
Collecting anyio (from httpx==0.28.1->-r requirements.txt (line 7))
  Using cached anyio-4.15.1-py3-none-any.whl.metadata (4.7 kB)
Collecting certifi (from httpx==0.28.1->-r requirements.txt (line 7))
  Using cached certifi-2026.7.22-py3-none-any.whl.metadata (2.5 kB)
Collecting httpcore==1.* (from httpx==0.28.1->-r requirements.txt (line 7))
  Using cached httpcore-1.0.9-py3-none-any.whl.metadata (21 kB)
Collecting idna (from httpx==0.28.1->-r requirements.txt (line 7))
  Using cached idna-3.20-py3-none-any.whl.metadata (7.2 kB)
Using cached fastapi-0.115.0-py3-none-any.whl (94 kB)
Using cached pydantic-2.8.2-py3-none-any.whl (423 kB)
Using cached uvicorn-0.30.6-py3-none-any.whl (62 kB)
Using cached pytest-8.3.2-py3-none-any.whl (341 kB)
Using cached python_dotenv-1.0.1-py3-none-any.whl (19 kB)
Using cached PyYAML-6.0.2-cp313-cp313-win_amd64.whl (156 kB)
Using cached httpx-0.28.1-py3-none-any.whl (73 kB)
Using cached pydantic_core-2.20.1-cp313-none-win_amd64.whl (1.9 MB)
Using cached httpcore-1.0.9-py3-none-any.whl (78 kB)
Using cached pluggy-1.6.0-py3-none-any.whl (20 kB)
Using cached starlette-0.38.6-py3-none-any.whl (71 kB)
Using cached anyio-4.15.1-py3-none-any.whl (132 kB)
Using cached annotated_types-0.8.0-py3-none-any.whl (13 kB)
Using cached click-8.5.0-py3-none-any.whl (125 kB)
Using cached h11-0.16.0-py3-none-any.whl (37 kB)
Using cached idna-3.20-py3-none-any.whl (69 kB)
Using cached typing_extensions-4.16.0-py3-none-any.whl (45 kB)
Using cached certifi-2026.7.22-py3-none-any.whl (136 kB)
Using cached colorama-0.4.6-py2.py3-none-any.whl (25 kB)
Using cached iniconfig-2.3.1-py3-none-any.whl (7.6 kB)
Using cached packaging-26.3-py3-none-any.whl (129 kB)
Installing collected packages: typing-extensions, PyYAML, python-dotenv, pluggy, packaging, iniconfig, idna, h11, colorama, click, certifi, annotated-types, uvicorn, pytest, pydantic-core, httpcore, anyio, starlette, pydantic, httpx, fastapi


Successfully installed PyYAML-6.0.2 annotated-types-0.8.0 anyio-4.15.1 certifi-2026.7.22 click-8.5.0 colorama-0.4.6 fastapi-0.115.0 h11-0.16.0 httpcore-1.0.9 httpx-0.28.1 idna-3.20 iniconfig-2.3.1 packaging-26.3 pluggy-1.6.0 pydantic-2.8.2 pydantic-core-2.20.1 pytest-8.3.2 python-dotenv-1.0.1 starlette-0.38.6 typing-extensions-4.16.0 uvicorn-0.30.6
== Step 4 of 4: run pytest -q
...............                                                          [100%]
============================== warnings summary ===============================
.venv\Lib\site-packages\starlette\testclient.py:40
  C:\Users\mange\AppData\Local\Temp\s0405b\final\copy\.venv\Lib\site-packages\starlette\testclient.py:40: DeprecationWarning: The anyio.abc.BlockingPortal alias is deprecated, use anyio.from_thread.BlockingPortal instead.
    _PortalFactoryType = typing.Callable[[], typing.ContextManager[anyio.abc.BlockingPortal]]

tests/access/test_negative_access.py::test_noc_operator_mapped_role_may_read_record
tests/access/test_negative_access.py::test_ai_agent_may_recommend
tests/access/test_negative_access.py::test_missing_role_header_keeps_operator_default
tests/characterization/test_current_behaviour.py::test_missing_id_returns_first_row
tests/characterization/test_current_behaviour.py::test_ai_summarize_accepts_request_with_no_role_header
tests/test_api_contract.py::test_ai_summary_has_minimum_contract
  C:\Users\mange\AppData\Local\Temp\s0405b\final\copy\apps\api\services\audit.py:9: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    event = {"ts": datetime.utcnow().isoformat(), "action": action, "details": details}

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
15 passed, 7 warnings in 2.45s
bootstrap OK
```

## H2. Bad Python name (full output)

Command: `bootstrap.ps1 -Python "no-such-python"`. Exit code 1.

```text
== Step 1 of 4: check Python
powershell : & : The term 'no-such-python' is not recognized as the name of a cmdlet, function, script file, or 
operable program. 
At C:\Users\mange\AppData\Local\Temp\ps-script-45d8dc14-e94c-4c3e-9e26-00702778165d.ps1:98 char:83
+ ... thon name"; powershell -NoProfile -ExecutionPolicy Bypass -File "$dst ...
+                 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (& : The term 'n...rable program. :String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError
 
Check the spelling of the name, or if a path was included, verify that the path is correct and try again.
At C:\Users\mange\AppData\Local\Temp\s0405b\copy\scripts\bootstrap.ps1:38 char:3
+ & $PythonExe @PythonArgs --version
+   ~~~~~~~~~~
    + CategoryInfo          : ObjectNotFound: (no-such-python:String) [], CommandNotFoundException
    + FullyQualifiedErrorId : CommandNotFoundException
 
bootstrap FAILED: Python command 'no-such-python' did not run. Set -Python or the PYTHON variable.
```

## H3. Launcher form with `-SkipTests` (full output)

Command: `bootstrap.ps1 -Python "py -3.12" -SkipTests`, in a second fresh copy. Exit code 0.

```text
== Step 1 of 4: check Python
Python 3.12.10
== Step 2 of 4: create .venv
Python 3.12.10
== Step 3 of 4: install requirements.txt
Collecting fastapi==0.115.0 (from -r requirements.txt (line 1))
  Using cached fastapi-0.115.0-py3-none-any.whl.metadata (27 kB)
Collecting uvicorn==0.30.6 (from -r requirements.txt (line 2))
  Using cached uvicorn-0.30.6-py3-none-any.whl.metadata (6.6 kB)
Collecting pydantic==2.8.2 (from -r requirements.txt (line 3))
  Using cached pydantic-2.8.2-py3-none-any.whl.metadata (125 kB)
Collecting pytest==8.3.2 (from -r requirements.txt (line 4))
  Using cached pytest-8.3.2-py3-none-any.whl.metadata (7.5 kB)
Collecting python-dotenv==1.0.1 (from -r requirements.txt (line 5))
  Using cached python_dotenv-1.0.1-py3-none-any.whl.metadata (23 kB)
Collecting PyYAML==6.0.2 (from -r requirements.txt (line 6))
  Using cached PyYAML-6.0.2-cp312-cp312-win_amd64.whl.metadata (2.1 kB)
Collecting httpx==0.28.1 (from -r requirements.txt (line 7))
  Using cached httpx-0.28.1-py3-none-any.whl.metadata (7.1 kB)
Collecting starlette<0.39.0,>=0.37.2 (from fastapi==0.115.0->-r requirements.txt (line 1))
  Using cached starlette-0.38.6-py3-none-any.whl.metadata (6.0 kB)
Collecting typing-extensions>=4.8.0 (from fastapi==0.115.0->-r requirements.txt (line 1))
  Using cached typing_extensions-4.16.0-py3-none-any.whl.metadata (3.3 kB)
Collecting click>=7.0 (from uvicorn==0.30.6->-r requirements.txt (line 2))
  Using cached click-8.5.0-py3-none-any.whl.metadata (2.6 kB)
Collecting h11>=0.8 (from uvicorn==0.30.6->-r requirements.txt (line 2))
  Using cached h11-0.16.0-py3-none-any.whl.metadata (8.3 kB)
Collecting annotated-types>=0.4.0 (from pydantic==2.8.2->-r requirements.txt (line 3))
  Using cached annotated_types-0.8.0-py3-none-any.whl.metadata (15 kB)
Collecting pydantic-core==2.20.1 (from pydantic==2.8.2->-r requirements.txt (line 3))
  Using cached pydantic_core-2.20.1-cp312-none-win_amd64.whl.metadata (6.7 kB)
Collecting iniconfig (from pytest==8.3.2->-r requirements.txt (line 4))
  Using cached iniconfig-2.3.1-py3-none-any.whl.metadata (2.8 kB)
Collecting packaging (from pytest==8.3.2->-r requirements.txt (line 4))
  Using cached packaging-26.3-py3-none-any.whl.metadata (3.5 kB)
Collecting pluggy<2,>=1.5 (from pytest==8.3.2->-r requirements.txt (line 4))
  Using cached pluggy-1.6.0-py3-none-any.whl.metadata (4.8 kB)
Collecting colorama (from pytest==8.3.2->-r requirements.txt (line 4))
  Using cached colorama-0.4.6-py2.py3-none-any.whl.metadata (17 kB)
Collecting anyio (from httpx==0.28.1->-r requirements.txt (line 7))
  Using cached anyio-4.15.1-py3-none-any.whl.metadata (4.7 kB)
Collecting certifi (from httpx==0.28.1->-r requirements.txt (line 7))
  Using cached certifi-2026.7.22-py3-none-any.whl.metadata (2.5 kB)
Collecting httpcore==1.* (from httpx==0.28.1->-r requirements.txt (line 7))
  Using cached httpcore-1.0.9-py3-none-any.whl.metadata (21 kB)
Collecting idna (from httpx==0.28.1->-r requirements.txt (line 7))
  Using cached idna-3.20-py3-none-any.whl.metadata (7.2 kB)
Using cached fastapi-0.115.0-py3-none-any.whl (94 kB)
Using cached uvicorn-0.30.6-py3-none-any.whl (62 kB)
Using cached pydantic-2.8.2-py3-none-any.whl (423 kB)
Using cached pytest-8.3.2-py3-none-any.whl (341 kB)
Using cached python_dotenv-1.0.1-py3-none-any.whl (19 kB)
Using cached PyYAML-6.0.2-cp312-cp312-win_amd64.whl (156 kB)
Using cached httpx-0.28.1-py3-none-any.whl (73 kB)
Using cached httpcore-1.0.9-py3-none-any.whl (78 kB)
Using cached pydantic_core-2.20.1-cp312-none-win_amd64.whl (1.9 MB)
Using cached annotated_types-0.8.0-py3-none-any.whl (13 kB)
Using cached click-8.5.0-py3-none-any.whl (125 kB)
Using cached h11-0.16.0-py3-none-any.whl (37 kB)
Using cached pluggy-1.6.0-py3-none-any.whl (20 kB)
Using cached starlette-0.38.6-py3-none-any.whl (71 kB)
Using cached anyio-4.15.1-py3-none-any.whl (132 kB)
Using cached idna-3.20-py3-none-any.whl (69 kB)
Using cached typing_extensions-4.16.0-py3-none-any.whl (45 kB)
Using cached certifi-2026.7.22-py3-none-any.whl (136 kB)
Using cached colorama-0.4.6-py2.py3-none-any.whl (25 kB)
Using cached iniconfig-2.3.1-py3-none-any.whl (7.6 kB)
Using cached packaging-26.3-py3-none-any.whl (129 kB)
Installing collected packages: typing-extensions, PyYAML, python-dotenv, pluggy, packaging, iniconfig, idna, h11, colorama, click, certifi, annotated-types, uvicorn, pytest, pydantic-core, httpcore, anyio, starlette, pydantic, httpx, fastapi
Successfully installed PyYAML-6.0.2 annotated-types-0.8.0 anyio-4.15.1 certifi-2026.7.22 click-8.5.0 colorama-0.4.6 fastapi-0.115.0 h11-0.16.0 httpcore-1.0.9 httpx-0.28.1 idna-3.20 iniconfig-2.3.1 packaging-26.3 pluggy-1.6.0 pydantic-2.8.2 pydantic-core-2.20.1 pytest-8.3.2 python-dotenv-1.0.1 starlette-0.38.6 typing-extensions-4.16.0 uvicorn-0.30.6
== Step 4 of 4: skipped (-SkipTests)
bootstrap OK (tests skipped)
```

## H4. Second run on an existing `.venv` (full output)

Command: `bootstrap.ps1 -SkipTests`, in the folder used for the first run. Exit code 0. The first Step 2 line says `.venv already exists. Reusing it.`

```text
== Step 1 of 4: check Python
Python 3.13.5
== Step 2 of 4: create .venv
.venv already exists. Reusing it.
Python 3.13.5
== Step 3 of 4: install requirements.txt
Requirement already satisfied: fastapi==0.115.0 in c:\users\mange\appdata\local\temp\s0405b\copy\.venv\lib\site-packages (from -r requirements.txt (line 1)) (0.115.0)
Requirement already satisfied: uvicorn==0.30.6 in c:\users\mange\appdata\local\temp\s0405b\copy\.venv\lib\site-packages (from -r requirements.txt (line 2)) (0.30.6)
Requirement already satisfied: pydantic==2.8.2 in c:\users\mange\appdata\local\temp\s0405b\copy\.venv\lib\site-packages (from -r requirements.txt (line 3)) (2.8.2)
Requirement already satisfied: pytest==8.3.2 in c:\users\mange\appdata\local\temp\s0405b\copy\.venv\lib\site-packages (from -r requirements.txt (line 4)) (8.3.2)
Requirement already satisfied: python-dotenv==1.0.1 in c:\users\mange\appdata\local\temp\s0405b\copy\.venv\lib\site-packages (from -r requirements.txt (line 5)) (1.0.1)
Requirement already satisfied: PyYAML==6.0.2 in c:\users\mange\appdata\local\temp\s0405b\copy\.venv\lib\site-packages (from -r requirements.txt (line 6)) (6.0.2)
Requirement already satisfied: httpx==0.28.1 in c:\users\mange\appdata\local\temp\s0405b\copy\.venv\lib\site-packages (from -r requirements.txt (line 7)) (0.28.1)
Requirement already satisfied: starlette<0.39.0,>=0.37.2 in c:\users\mange\appdata\local\temp\s0405b\copy\.venv\lib\site-packages (from fastapi==0.115.0->-r requirements.txt (line 1)) (0.38.6)
Requirement already satisfied: typing-extensions>=4.8.0 in c:\users\mange\appdata\local\temp\s0405b\copy\.venv\lib\site-packages (from fastapi==0.115.0->-r requirements.txt (line 1)) (4.16.0)
Requirement already satisfied: annotated-types>=0.4.0 in c:\users\mange\appdata\local\temp\s0405b\copy\.venv\lib\site-packages (from pydantic==2.8.2->-r requirements.txt (line 3)) (0.8.0)
Requirement already satisfied: pydantic-core==2.20.1 in c:\users\mange\appdata\local\temp\s0405b\copy\.venv\lib\site-packages (from pydantic==2.8.2->-r requirements.txt (line 3)) (2.20.1)
Requirement already satisfied: click>=7.0 in c:\users\mange\appdata\local\temp\s0405b\copy\.venv\lib\site-packages (from uvicorn==0.30.6->-r requirements.txt (line 2)) (8.5.0)
Requirement already satisfied: h11>=0.8 in c:\users\mange\appdata\local\temp\s0405b\copy\.venv\lib\site-packages (from uvicorn==0.30.6->-r requirements.txt (line 2)) (0.16.0)
Requirement already satisfied: iniconfig in c:\users\mange\appdata\local\temp\s0405b\copy\.venv\lib\site-packages (from pytest==8.3.2->-r requirements.txt (line 4)) (2.3.1)
Requirement already satisfied: packaging in c:\users\mange\appdata\local\temp\s0405b\copy\.venv\lib\site-packages (from pytest==8.3.2->-r requirements.txt (line 4)) (26.3)
Requirement already satisfied: pluggy<2,>=1.5 in c:\users\mange\appdata\local\temp\s0405b\copy\.venv\lib\site-packages (from pytest==8.3.2->-r requirements.txt (line 4)) (1.6.0)
Requirement already satisfied: colorama in c:\users\mange\appdata\local\temp\s0405b\copy\.venv\lib\site-packages (from pytest==8.3.2->-r requirements.txt (line 4)) (0.4.6)
Requirement already satisfied: anyio in c:\users\mange\appdata\local\temp\s0405b\copy\.venv\lib\site-packages (from httpx==0.28.1->-r requirements.txt (line 7)) (4.15.1)
Requirement already satisfied: certifi in c:\users\mange\appdata\local\temp\s0405b\copy\.venv\lib\site-packages (from httpx==0.28.1->-r requirements.txt (line 7)) (2026.7.22)
Requirement already satisfied: httpcore==1.* in c:\users\mange\appdata\local\temp\s0405b\copy\.venv\lib\site-packages (from httpx==0.28.1->-r requirements.txt (line 7)) (1.0.9)
Requirement already satisfied: idna in c:\users\mange\appdata\local\temp\s0405b\copy\.venv\lib\site-packages (from httpx==0.28.1->-r requirements.txt (line 7)) (3.20)
== Step 4 of 4: skipped (-SkipTests)
bootstrap OK (tests skipped)
```

## H5. `make setup` on Linux, Python 3.11 (full output)

The container script installs `make`, copies the read-only copy to `/work`, removes `.venv` and `logs`, and runs `make setup` with the default `PYTHON=python3`.

```text
GNU Make 4.4.1
--- make setup (default PYTHON=python3)
PYTHON=python3 bash scripts/bootstrap.sh
== Step 1 of 4: check Python
Python 3.11.17
== Step 2 of 4: create .venv
Python 3.11.17
== Step 3 of 4: install requirements.txt
Collecting fastapi==0.115.0 (from -r requirements.txt (line 1))
  Downloading fastapi-0.115.0-py3-none-any.whl.metadata (27 kB)
Collecting uvicorn==0.30.6 (from -r requirements.txt (line 2))
  Downloading uvicorn-0.30.6-py3-none-any.whl.metadata (6.6 kB)
Collecting pydantic==2.8.2 (from -r requirements.txt (line 3))
  Downloading pydantic-2.8.2-py3-none-any.whl.metadata (125 kB)
     ΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöü 125.2/125.2 kB 2.7 MB/s eta 0:00:00
Collecting pytest==8.3.2 (from -r requirements.txt (line 4))
  Downloading pytest-8.3.2-py3-none-any.whl.metadata (7.5 kB)
Collecting python-dotenv==1.0.1 (from -r requirements.txt (line 5))
  Downloading python_dotenv-1.0.1-py3-none-any.whl.metadata (23 kB)
Collecting PyYAML==6.0.2 (from -r requirements.txt (line 6))
  Downloading PyYAML-6.0.2-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (2.1 kB)
Collecting httpx==0.28.1 (from -r requirements.txt (line 7))
  Downloading httpx-0.28.1-py3-none-any.whl.metadata (7.1 kB)
Collecting starlette<0.39.0,>=0.37.2 (from fastapi==0.115.0->-r requirements.txt (line 1))
  Downloading starlette-0.38.6-py3-none-any.whl.metadata (6.0 kB)
Collecting typing-extensions>=4.8.0 (from fastapi==0.115.0->-r requirements.txt (line 1))
  Downloading typing_extensions-4.16.0-py3-none-any.whl.metadata (3.3 kB)
Collecting click>=7.0 (from uvicorn==0.30.6->-r requirements.txt (line 2))
  Downloading click-8.5.0-py3-none-any.whl.metadata (2.6 kB)
Collecting h11>=0.8 (from uvicorn==0.30.6->-r requirements.txt (line 2))
  Downloading h11-0.16.0-py3-none-any.whl.metadata (8.3 kB)
Collecting annotated-types>=0.4.0 (from pydantic==2.8.2->-r requirements.txt (line 3))
  Downloading annotated_types-0.8.0-py3-none-any.whl.metadata (15 kB)
Collecting pydantic-core==2.20.1 (from pydantic==2.8.2->-r requirements.txt (line 3))
  Downloading pydantic_core-2.20.1-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (6.6 kB)
Collecting iniconfig (from pytest==8.3.2->-r requirements.txt (line 4))
  Downloading iniconfig-2.3.1-py3-none-any.whl.metadata (2.8 kB)
Collecting packaging (from pytest==8.3.2->-r requirements.txt (line 4))
  Downloading packaging-26.3-py3-none-any.whl.metadata (3.5 kB)
Collecting pluggy<2,>=1.5 (from pytest==8.3.2->-r requirements.txt (line 4))
  Downloading pluggy-1.6.0-py3-none-any.whl.metadata (4.8 kB)
Collecting anyio (from httpx==0.28.1->-r requirements.txt (line 7))
  Downloading anyio-4.15.1-py3-none-any.whl.metadata (4.7 kB)
Collecting certifi (from httpx==0.28.1->-r requirements.txt (line 7))
  Downloading certifi-2026.7.22-py3-none-any.whl.metadata (2.5 kB)
Collecting httpcore==1.* (from httpx==0.28.1->-r requirements.txt (line 7))
  Downloading httpcore-1.0.9-py3-none-any.whl.metadata (21 kB)
Collecting idna (from httpx==0.28.1->-r requirements.txt (line 7))
  Downloading idna-3.20-py3-none-any.whl.metadata (7.2 kB)
Downloading fastapi-0.115.0-py3-none-any.whl (94 kB)
   ΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöü 94.6/94.6 kB 5.3 MB/s eta 0:00:00
Downloading uvicorn-0.30.6-py3-none-any.whl (62 kB)
   ΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöü 62.8/62.8 kB 5.3 MB/s eta 0:00:00
Downloading pydantic-2.8.2-py3-none-any.whl (423 kB)
   ΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöü 423.9/423.9 kB 8.4 MB/s eta 0:00:00
Downloading pytest-8.3.2-py3-none-any.whl (341 kB)
   ΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöü 341.8/341.8 kB 8.2 MB/s eta 0:00:00
Downloading python_dotenv-1.0.1-py3-none-any.whl (19 kB)
Downloading PyYAML-6.0.2-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (762 kB)
   ΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöü 763.0/763.0 kB 8.0 MB/s eta 0:00:00
Downloading httpx-0.28.1-py3-none-any.whl (73 kB)
   ΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöü 73.5/73.5 kB 6.5 MB/s eta 0:00:00
Downloading httpcore-1.0.9-py3-none-any.whl (78 kB)
   ΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöü 78.8/78.8 kB 6.2 MB/s eta 0:00:00
Downloading pydantic_core-2.20.1-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (2.1 MB)
   ΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöü 2.1/2.1 MB 7.4 MB/s eta 0:00:00
Downloading annotated_types-0.8.0-py3-none-any.whl (13 kB)
Downloading click-8.5.0-py3-none-any.whl (125 kB)
   ΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöü 125.3/125.3 kB 2.7 MB/s eta 0:00:00
Downloading h11-0.16.0-py3-none-any.whl (37 kB)
Downloading pluggy-1.6.0-py3-none-any.whl (20 kB)
Downloading starlette-0.38.6-py3-none-any.whl (71 kB)
   ΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöü 71.5/71.5 kB 4.3 MB/s eta 0:00:00
Downloading anyio-4.15.1-py3-none-any.whl (132 kB)
   ΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöü 132.1/132.1 kB 7.7 MB/s eta 0:00:00
Downloading idna-3.20-py3-none-any.whl (69 kB)
   ΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöü 69.6/69.6 kB 5.9 MB/s eta 0:00:00
Downloading typing_extensions-4.16.0-py3-none-any.whl (45 kB)
   ΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöü 45.6/45.6 kB 3.1 MB/s eta 0:00:00
Downloading certifi-2026.7.22-py3-none-any.whl (136 kB)
   ΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöü 137.0/137.0 kB 6.3 MB/s eta 0:00:00
Downloading iniconfig-2.3.1-py3-none-any.whl (7.6 kB)
Downloading packaging-26.3-py3-none-any.whl (129 kB)
   ΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöü 130.0/130.0 kB 6.3 MB/s eta 0:00:00
Installing collected packages: typing-extensions, PyYAML, python-dotenv, pluggy, packaging, iniconfig, idna, h11, click, certifi, annotated-types, uvicorn, pytest, pydantic-core, httpcore, anyio, starlette, pydantic, httpx, fastapi
Successfully installed PyYAML-6.0.2 annotated-types-0.8.0 anyio-4.15.1 certifi-2026.7.22 click-8.5.0 fastapi-0.115.0 h11-0.16.0 httpcore-1.0.9 httpx-0.28.1 idna-3.20 iniconfig-2.3.1 packaging-26.3 pluggy-1.6.0 pydantic-2.8.2 pydantic-core-2.20.1 pytest-8.3.2 python-dotenv-1.0.1 starlette-0.38.6 typing-extensions-4.16.0 uvicorn-0.30.6
== Step 4 of 4: run pytest -q
...............                                                          [100%]
=============================== warnings summary ===============================
.venv/lib/python3.11/site-packages/starlette/testclient.py:40
  /work/.venv/lib/python3.11/site-packages/starlette/testclient.py:40: DeprecationWarning: The anyio.abc.BlockingPortal alias is deprecated, use anyio.from_thread.BlockingPortal instead.
    _PortalFactoryType = typing.Callable[[], typing.ContextManager[anyio.abc.BlockingPortal]]

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
15 passed, 1 warning in 1.00s
bootstrap OK
make setup exit code: 0
```

## H6. `bootstrap.sh` on WSL Ubuntu with Python 3.10 (full output)

Command: `bash scripts/bootstrap.sh`. Exit code 2. This is the failure path working as written: the step that failed is named, and the message names the package to install. This stage did not run `sudo`.

```text
== Step 1 of 4: check Python
Python 3.10.12
== Step 2 of 4: create .venv
The virtual environment was not created successfully because ensurepip is not
available.  On Debian/Ubuntu systems, you need to install the python3-venv
package using the following command.

    apt install python3.10-venv

You may need to use sudo with that command.  After installing the python3-venv
package, recreate your virtual environment.

Failing command: /mnt/c/Users/mange/AppData/Local/Temp/s0405b/copy/.venv/bin/python3

bootstrap FAILED: could not create .venv. On Ubuntu or Debian, install the python3-venv package for your Python version.
```

## H7. Docker build and run (full output)

Commands, from the fresh copy:

```text
docker build --progress=plain --no-cache -t telecom-ops-tests .
docker run --rm telecom-ops-tests
```

Build output. Exit code 0.

```text
docker : #0 building with "desktop-linux" instance using docker driver
At C:\Users\mange\AppData\Local\Temp\ps-script-ed646871-5845-4550-8772-c9b043b93066.ps1:102 char:19
+ ... inal\copy"; docker build --progress=plain --no-cache -t telecom-ops-t ...
+                 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (#0 building wit...g docker driver:String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError
 

#1 [internal] load build definition from Dockerfile
#1 transferring dockerfile: 862B done
#1 DONE 0.0s

#2 [internal] load metadata for docker.io/library/python:3.11-slim
#2 DONE 0.0s

#3 [internal] load .dockerignore
#3 transferring context: 158B done
#3 DONE 0.0s

#4 [1/6] FROM docker.io/library/python:3.11-slim
#4 DONE 0.0s

#5 [2/6] WORKDIR /app
#5 CACHED

#6 [internal] load build context
#6 transferring context: 2.27MB 0.3s done
#6 DONE 0.3s

#7 [3/6] COPY requirements.txt .
#7 DONE 0.0s

#8 [4/6] RUN pip install -r requirements.txt
#8 1.867 Collecting fastapi==0.115.0 (from -r requirements.txt (line 1))
#8 1.961   Downloading fastapi-0.115.0-py3-none-any.whl.metadata (27 kB)
#8 2.027 Collecting uvicorn==0.30.6 (from -r requirements.txt (line 2))
#8 2.038   Downloading uvicorn-0.30.6-py3-none-any.whl.metadata (6.6 kB)
#8 2.256 Collecting pydantic==2.8.2 (from -r requirements.txt (line 3))
#8 2.273   Downloading pydantic-2.8.2-py3-none-any.whl.metadata (125 kB)
#8 2.286      
ΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöü 
125.2/125.2 kB 12.8 MB/s eta 0:00:00
#8 2.380 Collecting pytest==8.3.2 (from -r requirements.txt (line 4))
#8 2.395   Downloading pytest-8.3.2-py3-none-any.whl.metadata (7.5 kB)
#8 2.439 Collecting python-dotenv==1.0.1 (from -r requirements.txt (line 5))
#8 2.451   Downloading python_dotenv-1.0.1-py3-none-any.whl.metadata (23 kB)
#8 2.516 Collecting PyYAML==6.0.2 (from -r requirements.txt (line 6))
#8 2.531   Downloading PyYAML-6.0.2-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (2.1 kB)
#8 2.572 Collecting httpx==0.28.1 (from -r requirements.txt (line 7))
#8 2.584   Downloading httpx-0.28.1-py3-none-any.whl.metadata (7.1 kB)
#8 2.699 Collecting starlette<0.39.0,>=0.37.2 (from fastapi==0.115.0->-r requirements.txt (line 1))
#8 2.719   Downloading starlette-0.38.6-py3-none-any.whl.metadata (6.0 kB)
#8 2.889 Collecting typing-extensions>=4.8.0 (from fastapi==0.115.0->-r requirements.txt (line 1))
#8 2.910   Downloading typing_extensions-4.16.0-py3-none-any.whl.metadata (3.3 kB)
#8 2.974 Collecting click>=7.0 (from uvicorn==0.30.6->-r requirements.txt (line 2))
#8 2.985   Downloading click-8.5.0-py3-none-any.whl.metadata (2.6 kB)
#8 3.013 Collecting h11>=0.8 (from uvicorn==0.30.6->-r requirements.txt (line 2))
#8 3.028   Downloading h11-0.16.0-py3-none-any.whl.metadata (8.3 kB)
#8 3.061 Collecting annotated-types>=0.4.0 (from pydantic==2.8.2->-r requirements.txt (line 3))
#8 3.074   Downloading annotated_types-0.8.0-py3-none-any.whl.metadata (15 kB)
#8 4.163 Collecting pydantic-core==2.20.1 (from pydantic==2.8.2->-r requirements.txt (line 3))
#8 4.176   Downloading pydantic_core-2.20.1-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (6.6 
kB)
#8 4.304 Collecting iniconfig (from pytest==8.3.2->-r requirements.txt (line 4))
#8 4.318   Downloading iniconfig-2.3.1-py3-none-any.whl.metadata (2.8 kB)
#8 4.321 Requirement already satisfied: packaging in /usr/local/lib/python3.11/site-packages (from pytest==8.3.2->-r 
requirements.txt (line 4)) (26.3)
#8 4.358 Collecting pluggy<2,>=1.5 (from pytest==8.3.2->-r requirements.txt (line 4))
#8 4.391   Downloading pluggy-1.6.0-py3-none-any.whl.metadata (4.8 kB)
#8 4.467 Collecting anyio (from httpx==0.28.1->-r requirements.txt (line 7))
#8 4.496   Downloading anyio-4.15.1-py3-none-any.whl.metadata (4.7 kB)
#8 4.540 Collecting certifi (from httpx==0.28.1->-r requirements.txt (line 7))
#8 4.554   Downloading certifi-2026.7.22-py3-none-any.whl.metadata (2.5 kB)
#8 4.601 Collecting httpcore==1.* (from httpx==0.28.1->-r requirements.txt (line 7))
#8 4.619   Downloading httpcore-1.0.9-py3-none-any.whl.metadata (21 kB)
#8 4.652 Collecting idna (from httpx==0.28.1->-r requirements.txt (line 7))
#8 4.661   Downloading idna-3.20-py3-none-any.whl.metadata (7.2 kB)
#8 4.753 Downloading fastapi-0.115.0-py3-none-any.whl (94 kB)
#8 4.759    ΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓö
üΓöüΓöüΓöüΓöü 94.6/94.6 kB 22.7 MB/s eta 0:00:00
#8 4.787 Downloading uvicorn-0.30.6-py3-none-any.whl (62 kB)
#8 4.790    ΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓö
üΓöüΓöüΓöüΓöü 62.8/62.8 kB 156.4 MB/s eta 0:00:00
#8 4.815 Downloading pydantic-2.8.2-py3-none-any.whl (423 kB)
#8 4.852    ΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓö
üΓöüΓöüΓöüΓöü 423.9/423.9 kB 13.0 MB/s eta 0:00:00
#8 4.872 Downloading pytest-8.3.2-py3-none-any.whl (341 kB)
#8 4.915    ΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓö
üΓöüΓöüΓöüΓöü 341.8/341.8 kB 8.2 MB/s eta 0:00:00
#8 4.927 Downloading python_dotenv-1.0.1-py3-none-any.whl (19 kB)
#8 4.937 Downloading PyYAML-6.0.2-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (762 kB)
#8 5.028    ΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓö
üΓöüΓöüΓöüΓöü 763.0/763.0 kB 9.1 MB/s eta 0:00:00
#8 5.043 Downloading httpx-0.28.1-py3-none-any.whl (73 kB)
#8 5.052    ΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓö
üΓöüΓöüΓöüΓöü 73.5/73.5 kB 11.4 MB/s eta 0:00:00
#8 5.068 Downloading httpcore-1.0.9-py3-none-any.whl (78 kB)
#8 5.074    ΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓö
üΓöüΓöüΓöüΓöü 78.8/78.8 kB 38.9 MB/s eta 0:00:00
#8 5.107 Downloading pydantic_core-2.20.1-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (2.1 MB)
#8 5.334    ΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓö
üΓöüΓöüΓöüΓöü 2.1/2.1 MB 9.3 MB/s eta 0:00:00
#8 5.348 Downloading annotated_types-0.8.0-py3-none-any.whl (13 kB)
#8 5.368 Downloading click-8.5.0-py3-none-any.whl (125 kB)
#8 5.373    ΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓö
üΓöüΓöüΓöüΓöü 125.3/125.3 kB 88.6 MB/s eta 0:00:00
#8 5.394 Downloading h11-0.16.0-py3-none-any.whl (37 kB)
#8 5.408 Downloading pluggy-1.6.0-py3-none-any.whl (20 kB)
#8 5.430 Downloading starlette-0.38.6-py3-none-any.whl (71 kB)
#8 5.434    ΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓö
üΓöüΓöüΓöüΓöü 71.5/71.5 kB 177.9 MB/s eta 0:00:00
#8 5.451 Downloading anyio-4.15.1-py3-none-any.whl (132 kB)
#8 5.463    ΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓö
üΓöüΓöüΓöüΓöü 132.1/132.1 kB 15.5 MB/s eta 0:00:00
#8 5.479 Downloading idna-3.20-py3-none-any.whl (69 kB)
#8 5.486    ΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓö
üΓöüΓöüΓöüΓöü 69.6/69.6 kB 19.3 MB/s eta 0:00:00
#8 5.511 Downloading typing_extensions-4.16.0-py3-none-any.whl (45 kB)
#8 5.518    ΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓö
üΓöüΓöüΓöüΓöü 45.6/45.6 kB 43.4 MB/s eta 0:00:00
#8 5.543 Downloading certifi-2026.7.22-py3-none-any.whl (136 kB)
#8 5.564    ΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓöüΓö
üΓöüΓöüΓöüΓöü 137.0/137.0 kB 8.9 MB/s eta 0:00:00
#8 5.588 Downloading iniconfig-2.3.1-py3-none-any.whl (7.6 kB)
#8 5.806 Installing collected packages: typing-extensions, PyYAML, python-dotenv, pluggy, iniconfig, idna, h11, click, 
certifi, annotated-types, uvicorn, pytest, pydantic-core, httpcore, anyio, starlette, pydantic, httpx, fastapi
#8 7.403 Successfully installed PyYAML-6.0.2 annotated-types-0.8.0 anyio-4.15.1 certifi-2026.7.22 click-8.5.0 
fastapi-0.115.0 h11-0.16.0 httpcore-1.0.9 httpx-0.28.1 idna-3.20 iniconfig-2.3.1 pluggy-1.6.0 pydantic-2.8.2 
pydantic-core-2.20.1 pytest-8.3.2 python-dotenv-1.0.1 starlette-0.38.6 typing-extensions-4.16.0 uvicorn-0.30.6
#8 7.403 WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the 
system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv
#8 DONE 8.0s

#9 [5/6] COPY . .
#9 DONE 0.1s

#10 [6/6] RUN useradd --create-home app && chown -R app:app /app
#10 DONE 0.6s

#11 exporting to image
#11 exporting layers
#11 exporting layers 0.3s done
#11 writing image sha256:5cf185310062850372847fc5e404e3cdf0a31041063e69941a9b8f5180a14408 done
#11 naming to docker.io/library/telecom-ops-tests done
#11 DONE 0.3s

View build details: docker-desktop://dashboard/build/desktop-linux/desktop-linux/okowm7vcbz5pemk17d6nyaqxf
```

Run output. Exit code 0.

```text
...............                                                          [100%]
=============================== warnings summary ===============================
../usr/local/lib/python3.11/site-packages/starlette/testclient.py:40
  /usr/local/lib/python3.11/site-packages/starlette/testclient.py:40: DeprecationWarning: The anyio.abc.BlockingPortal alias is deprecated, use anyio.from_thread.BlockingPortal instead.
    _PortalFactoryType = typing.Callable[[], typing.ContextManager[anyio.abc.BlockingPortal]]

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
15 passed, 1 warning in 1.13s
```

## H8. Terraform check (full output)

Terraform is not installed on this machine (IG-02). The check ran the official `hashicorp/terraform:1.9` image with a throwaway folder that held a copy of `main.tf`. The apply wrote `generated-env.txt` and a state file inside that folder only. **Verified Fact.** The repo has no `generated-env.txt` and no `terraform.tfstate`. No cloud account was used. The `local` provider writes a file and calls no remote service.

```text
Terraform v1.9.8
--- init
Initializing provider plugins...
- Finding hashicorp/local versions matching "~> 2.5"...
- Installing hashicorp/local v2.9.1...
- Installed hashicorp/local v2.9.1 (signed by HashiCorp)
Terraform has created a lock file .terraform.lock.hcl to record the provider
selections it made above. Include this file in your version control repository
so that Terraform can guarantee to make the same selections by default when
you run "terraform init" in the future.

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.
--- fmt -check
fmt: ok
--- validate
Success! The configuration is valid.

--- apply (local file only, in a throwaway folder)

Terraform used the selected providers to generate the following execution
plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # local_file.workshop_env will be created
  + resource "local_file" "workshop_env" {
      + content              = <<-EOT
            LOG_LEVEL=DEBUG
            API_PORT=8000
        EOT
      + content_base64sha256 = (known after apply)
      + content_base64sha512 = (known after apply)
      + content_md5          = (known after apply)
      + content_sha1         = (known after apply)
      + content_sha256       = (known after apply)
      + content_sha512       = (known after apply)
      + directory_permission = "0755"
      + file_permission      = "0644"
      + filename             = "generated-env.txt"
      + id                   = (known after apply)
    }

Plan: 1 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + settings_file = "generated-env.txt"
local_file.workshop_env: Creating...
local_file.workshop_env: Creation complete after 0s [id=194e575e7075ca0158e148726fe685c81ea57db6]

Apply complete! Resources: 1 added, 0 changed, 0 destroyed.

Outputs:

settings_file = "generated-env.txt"
--- generated-env.txt
LOG_LEVEL=DEBUG
API_PORT=8000
-rw-r--r--    1 root     root            30 Oct 11 18:47 generated-env.txt
--- search the file for shared user, password, token, key
none found
--- bad variable (log_level=TRACE) must fail

Planning failed. Terraform encountered an error while generating this plan.

docker : 
At C:\Users\mange\AppData\Local\Temp\ps-script-283b3830-0a26-4f0f-8dc5-3a47d6a37612.ps1:99 char:1
+ docker run --rm --entrypoint sh -v "${tf}:/tf" -v "$work\tf-run.sh:/r ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (:String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError
 
Error: Invalid value for variable

  on main.tf line 26:
  26: variable "log_level" {
    Γö£ΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇ
    Γöé var.log_level is "TRACE"

log_level must be DEBUG, INFO, WARNING, or ERROR.

This was checked by the validation rule at main.tf:31,3-13.
plan exit code: 1
```

## Gaps from Half A, and what Half B did

| Finding | State after Half B |
|---|---|
| IG-01 `main.tf` writes the shared user | Fixed. H8 shows the written file. |
| IG-02 `main.tf` builds nothing, cannot be checked | Partly fixed. The file now has a provider pin, variables, validation, and an output, and `terraform validate` passes (H8). It still builds only a local text file. Terraform is still not installed on this machine. |
| IG-03 venv steps live in prose | Fixed. H1, H5. |
| IG-04 Makefile and Windows | Partly fixed. `make setup` exists and passed on Linux (H5). `test`, `smoke`, and `etl` still default to `python3`. `make` is still absent on Windows, so Windows uses `bootstrap.ps1`. |
| IG-05 `httpx` missing | Fixed. H1 and H5 passed on a clean install with no hand-installed package. |
| IG-06 `jsonschema` missing, unused packages pinned | Not changed. S04-07 owns it. |
| IG-07 no container | Fixed. H7. |
| IG-08 no environment split | Not changed in code. No code reads `.env`. The Terraform file now has `log_level` and `api_port` variables. |
| IG-09 CI file below the git root | Not changed. S04-07. |
| IG-10 Python pinned only in CI | Partly fixed. The container pins 3.11. Both scripts refuse Python older than 3.10. 3.10 itself is not run. |
| IG-11 no `.gitignore` | Not changed. Added `.dockerignore` only. |
| IG-12, IG-13 Playwright and OPA | Not changed. Out of scope. |
| IG-14 last commit lacks the S04 work | Not changed. A commit is a person's decision. |

## Limits of this evidence

- **Verified Fact.** The runs used folder copies. A `git clone` of the last commit gives a different tree (IG-14).
- **Verified Fact.** The Windows runs used Windows PowerShell with `-NoProfile`. `pwsh` was not run.
- **Unknown.** Behaviour on macOS, on native Ubuntu with a venv package installed, and on Python 3.10.
- **Verified Fact.** `.terraform.lock.hcl` holds hashes for the platforms the container uses. A Windows user who runs `terraform init` may need `terraform providers lock` to add their platform. This was not run.
- **Inference.** `bootstrap.sh` needs no execute bit because the Makefile and the container call it with `bash`. A person who types `./scripts/bootstrap.sh` needs `chmod +x` first.

## Completion gate

Half B PASS when the bootstrap ran on this machine from a fresh folder copy and the tests passed, and the run is recorded. H1 meets that gate. The Docker build ran, so the CONDITIONAL PASS case for a missing Docker does not apply. Stage status: **PASS.**

## Lifecycle

This file cites `docs/00-setup/tool-versions.md` and `docs/04-secrets/cleaned-configuration-model.md` through the setup guide. Stage S04-07 calls `scripts/bootstrap.sh` from CI, fixes IG-09, adds `jsonschema` and `requirements-dev.txt`, and may use the `Dockerfile`. Stage S09 uses the setup guide and this evidence in the readiness checklist.
