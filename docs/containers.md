# Container Tooling

This page covers the container runtime setup and daily workflow for this machine.

The setup order lives in [setup.md](setup.md). This page explains what "Bring up container tooling" means in practice.

## Use Colima as the default macOS container runtime

For this setup, `colima` is the normal container runtime on macOS.

The usual reason is straightforward: most project workflows still assume the Docker CLI, `docker compose`, and Docker-compatible socket behavior. `colima` provides that path without depending on Docker Desktop.

The standard tool set for this machine is:

- `colima`
- `docker`
- `docker-compose` (provides the `docker compose` plugin)
- `docker-buildx`
- `podman`

Those tools are installed as part of the Homebrew package step. Container setup here is about bringing the runtime up and verifying that the expected CLI path works.

## Bring up Colima first

Start with `colima` unless you have a specific reason to use `podman` for the task at hand.

Typical bootstrap:

```sh
colima start
docker info
docker run --rm hello-world
```

If the Docker CLI is not already talking to the `colima` context, switch it explicitly:

```sh
docker context use colima
```

That is the default day-to-day path on this machine:

- start `colima`
- use `docker` and `docker compose` normally
- stop thinking about the runtime unless a project needs something unusual

This keeps the common case boring, which is the right goal for container tooling on a development machine.

## Use Docker-compatible project workflows through Colima

When a project says "run Docker" or "start the compose stack", the expected interpretation on this machine is usually "use the Docker CLI against `colima`."

That means commands like:

```sh
docker compose up
docker compose up --build
docker compose ps
docker compose down
```

For most local development projects, that is the happy path to optimize for.

If a repository has container setup docs of its own, follow the project-specific service names and compose files there. The machine-level expectation is only that the Docker-compatible path is available and working.

## Keep Podman as the intentional secondary runtime

`podman` is part of the standard tool set for this machine, but it is not the default runtime on macOS.

Use it when you specifically want the Podman workflow or a rootless-oriented container model instead of the standard Docker-compatible path.

On macOS, treat that as an explicit mode switch, not as something that should silently replace `colima`.

Typical first-time setup:

```sh
podman machine init
podman machine start
podman info
podman run --rm hello-world
```

After the initial setup, the normal startup path is just:

```sh
podman machine start
```

If you only need `colima` right now, `podman` can stay installed but unused until a project or task actually calls for it.

## Do not blur the Colima and Podman paths

The practical rule for this machine is simple:

- use `colima` with `docker` and `docker compose` for the default container workflow
- use `podman` with the native `podman` CLI when you intentionally want the Podman path

Do not assume `docker` and `podman` are interchangeable just because both can run containers.

In particular:

- do not document `podman` as if it were the normal backend for `docker compose` on this machine
- do not add ad hoc shell aliases that make `docker` secretly mean `podman`
- do not switch runtimes mid-task without checking which CLI the project actually expects

Clear separation is less confusing than clever compatibility tricks.

## Verify the runtime after setup

The machine setup is not done when the packages are installed. It is done when the runtime you expect actually starts and runs a container.

For the default `colima` path, verify:

```sh
colima start
docker info
docker compose version
docker run --rm hello-world
```

That confirms:

- the VM-backed runtime starts cleanly
- the Docker CLI can talk to it
- `docker compose` is available
- a basic container can run successfully

If you expect to use `podman` on this machine as well, verify that separately:

```sh
podman machine start
podman info
podman run --rm hello-world
```

That keeps the secondary runtime honest instead of assuming it works because the package is installed.

## Verify with a real project when needed

The final check is always a real project, especially for anything that uses multiple services.

For a Docker-oriented project, the practical test is usually one of these:

```sh
docker compose up
docker compose ps
docker compose down
```

If that project starts cleanly and the expected services come up, the container tooling is in the state this machine expects.

For Podman-specific work, use the project's native `podman` commands and verify that path directly rather than translating the workflow in your head.

## Summary

The active container workflow for this machine is straightforward:

1. Install the container CLI tools through the standard Homebrew package step.
2. Use `colima` as the default macOS runtime.
3. Run Docker-oriented projects through `docker` and `docker compose`.
4. Use `podman` only when you intentionally want the Podman path.
5. Verify each runtime with a real container command, not just package installation.

That keeps the common case simple while still leaving `podman` available for the cases where it is the better fit.
