# App Service Builder Python sample

A minimal Python 3.14 HTTP app for learning how to deploy a GitHub repository with
**App Service Builder (Private Preview)**. It uses only the Python standard library:
no framework, third-party packages, container files, or other repository is required.

This is a **dev/test learning sample, not a production HTTP server**. Live
end-to-end preview qualification is pending; local checks do not prove a successful
cloud build or deployment.

## Features

- `/` returns HTTP 200 and `App Service Builder / python-web: Hello`.
- `/health` returns HTTP 200 and `OK`; unknown paths return HTTP 404.
- `SAMPLE_GREETING` changes the deliberately public greeting.
- Root-level `builder.yaml` explicitly selects Python 3.14, the startup command
  `python app.py`, and `/health`. It relies on the single-component defaults for
  the root path (`/`), port 8080, and the required HTTP 200 health response.
- Dependency-free HTTP tests run locally and in GitHub Actions.

## Getting Started

### Prerequisites

- **Python 3.14**, available as `python3` (or `python` on Windows).
- Git, plus curl or a browser for HTTP checks.
- For deployment: Private Preview access, an authorized Azure subscription and
  resource group, and GitHub access to your own fork. Use a location available to
  your preview subscription; this sample does not assume a region.

### Installation

Fork [this repository](https://github.com/Azure-Samples/app-service-builder-python/fork)
to your own GitHub account. Clone **your fork**, replacing `<your-github-account>`:

```sh
git clone https://github.com/<your-github-account>/app-service-builder-python.git
cd app-service-builder-python
python3 --version
```

No package installation is required. `requirements.txt` intentionally contains no
packages, but must remain at the repository root as the build dependency manifest.
Optionally create a virtual environment:

```sh
python3 -m venv .venv
. .venv/bin/activate
```

On Windows PowerShell use Python 3.14 as `python`, create the environment with
`python -m venv .venv`, and activate it with `.venv\Scripts\Activate.ps1`.

### Quickstart

From the repository root:

```sh
python3 app.py
```

The server binds to `0.0.0.0:8080`, so it can also be reached from your local
network. Use it only in a trusted dev/test environment. In another terminal:

```sh
curl -i http://localhost:8080/
curl -i http://localhost:8080/health
curl -i http://localhost:8080/not-found
```

Expect HTTP 200 with `App Service Builder / python-web: Hello`, HTTP 200 with `OK`,
and HTTP 404 with `Not found`, respectively. Stop the server with Ctrl+C.
Do not override `PORT`: this sample always listens on 8080.

## Demo

### Deploy your fork with Portal

Follow the [Portal quickstart](https://builderapps.azure.com/docs/quickstarts/portal/)
using your Private Preview access:

1. Sign in to Portal and select your authorized subscription and resource group.
   Create an app in a location available to your preview.
2. Authorize the GitHub source connection for **your fork**. If your organization
   restricts repository access, have an authorized owner grant access to that
   repository. Do not select the upstream Azure-Samples repository.
3. Select your fork's **`main` branch** and the **repository root** as the app
   source root. Keep `app.py`, `requirements.txt`, and `builder.yaml` together
   at that root; there is no `samples/python-web` subdirectory to select.
4. Start deployment and wait for a successful terminal deployment state.
   Submitting a deployment request does not mean it has finished.
5. Read the app's runtime URL from Portal, then check both `/` and `/health`:

```sh
curl -i "https://<runtime-host>/"
curl -i "https://<runtime-host>/health"
```

Both must return HTTP 200 and the expected greeting/`OK` bodies. If deployment
fails or the health check fails, inspect the deployment status and logs before
proceeding. These are instructions, not evidence of a completed cloud deployment.

### Change the greeting

For a local demo, stop the existing server and restart it:

```sh
SAMPLE_GREETING="Welcome" python3 app.py
```

On Windows PowerShell set `$env:SAMPLE_GREETING = "Welcome"` and run `python app.py`.
The root response becomes `App Service Builder / python-web: Welcome`.
An unset or empty value uses `Hello`. **Never put secrets or personal data in this
setting**: the value is returned publicly over HTTP.

In Portal **Variables**, set `SAMPLE_GREETING` and choose **Save and deploy**.
**Save only** changes desired configuration, not existing runtime processes:
explicitly deploy afterward. Wait for completion and check `/` again.
Activating a retained version uses that version's historical values.
See the [variables guide](https://builderapps.azure.com/docs/guides/variables/).

### Push an app change and explicitly redeploy

After editing your fork locally:

```sh
git add app.py
git commit -m "Update sample greeting"
git push origin main
```

Push the files you actually changed to the branch connected in Portal. Builds read
**committed GitHub source**, not your local working tree. A push alone is not a
promise of automatic deployment: explicitly deploy the connected `main` branch
in Portal, wait for completion, and verify `/` and `/health` again.

### Cleanup

Stop local Python with Ctrl+C and run `deactivate` if you activated a virtual
environment. In Portal, delete **only the sample app** and wait for deletion to
complete. Do not delete the resource group or subscription: they may contain
unrelated resources. App deletion does not delete your GitHub fork or separately
created Azure resources.

## Validation

Run from the repository root with Python 3.14:

```sh
python3 -m py_compile app.py
python3 -m unittest discover -s tests -v
```

On Windows use `python` instead of `python3`. Tests start owned servers on
ephemeral loopback ports, check responses and greetings, and shut down afterward.
They do not deploy to Azure or require credentials.

The build contract remains Python 3.14, `python app.py`, port 8080, and
`/health` returning exactly HTTP 200. The manifest pins the runtime, startup
command, and health path; the root path (`/`), port 8080, and exact HTTP 200 health
status use the single-component defaults. There is no custom build or output path
and no Flask/Django/WSGI detection requirement. Keep the root manifest and the
empty dependency manifest intact when experimenting. Preview build-image/runtime
support still requires end-to-end qualification.

## Resources

- [App Service Builder documentation](https://builderapps.azure.com/docs/)
- [Portal quickstart](https://builderapps.azure.com/docs/quickstarts/portal/)
- [Supported runtimes](https://builderapps.azure.com/docs/reference/runtimes/)
- [Variables guide](https://builderapps.azure.com/docs/guides/variables/)
- [More samples](https://builderapps.azure.com/docs/samples/)

## Contributing and security

See [CONTRIBUTING.md](CONTRIBUTING.md), the
[Microsoft Open Source Code of Conduct](.github/CODE_OF_CONDUCT.md), and the
[MIT license](LICENSE.md). For security vulnerabilities, follow
[Microsoft's security reporting guidance](https://aka.ms/SECURITY.md) rather
than opening a public issue.
