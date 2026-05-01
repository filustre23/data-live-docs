On this page

# Project kernels

Hex projects use kernels to run your code and allocate compute for each session.

## What is a kernel?[​](#what-is-a-kernel "Direct link to What is a kernel?")

In computing, a **kernel** is part of the operating system that sits between hardware and software and manages resources such as CPU and memory.

In Hex, you need a kernel for each active project session. A session can be:

* A [Notebook](/docs/explore-data/notebook-view/develop-your-notebook) session
* A [Published App](/docs/share-insights/apps/publish-and-share-apps) session
* A [Scheduled run](/docs/share-insights/scheduled-runs) session
* An [API](/docs/api-integrations/api/overview) session

## Kernel status and actions[​](#kernel-status-and-actions "Direct link to Kernel status and actions")

In the [Notebook view](/docs/explore-data/notebook-view/develop-your-notebook), use the **Kernel Status** indicator in the lower-right and the **Kernel Actions** menu beside it to monitor and manage the kernel for your Notebook session.

### Kernel status[​](#kernel-status "Direct link to Kernel status")

Notebook kernels start when you open a Notebook session by running the project or restarting the kernel. Status moves from **Starting** (yellow) to **Running** (green) when the kernel is up.

If no cells run for the [idle timeout](#kernel-timeouts) period, the kernel stops automatically. You can stop it yourself with **Stop** in the **Kernel Actions** menu. Status then moves from **Stopping** (yellow) to **Stopped** (red).

warning

Closing your browser tab or leaving the project does not stop your kernel. If you use an advanced compute profile, select **Stop** when you are finished so the kernel does not keep running.

In some cases, your kernel status may display "Pending", meaning that your user has reached the [25 concurrent kernel limit](/docs/explore-data/projects/environment-configuration/project-kernels#concurrent-active-kernel-limit) and the project is waiting for an available kernel. This is most often due to running many projects using the [Hex API](/docs/api-integrations/api/overview).

### Kernel actions[​](#kernel-actions "Direct link to Kernel actions")

* **Restart** restarts the kernel.
* **Restart and run all** restarts the kernel and runs every cell again.
* **Run all without cached results** clears the project cache and runs every cell with the current kernel.
* **Interrupt** cancels in-flight cell execution without stopping the kernel.
* **Stop** stops the kernel, ends compute usage, and clears stored variables.
* **Clear outputs** clears output from all cells, which helps free memory when a cell produced very large output.

warning

Restarting or stopping the kernel clears every Python variable held in memory. If you rely on data that only exists in a variable and cannot be recreated by re-running cells, save it elsewhere before you restart or stop.

## Kernel timeouts[​](#kernel-timeouts "Direct link to Kernel timeouts")

### Idle timeout[​](#idle-timeout "Direct link to Idle timeout")

Kernels for Notebook and App sessions stop automatically after a period with no activity. A kernel counts as idle when no cells are running.

* **Notebook session** kernels default to a 1-hour idle timeout, which you can [change per project](/docs/explore-data/projects/environment-configuration/environment-views#idle-timeout).
* **Published App session** kernels use a 15-minute idle timeout that cannot be changed.
* **Scheduled run and API session** kernels stop when the run finishes and are limited to a 60-minute maximum.

info

[Community tier](https://hex.tech/pricing) workspaces use a 5-minute idle timeout for Published App sessions.

### Execution timeout[​](#execution-timeout "Direct link to Execution timeout")

If a single project run lasts longer than 24 hours, the kernel stops automatically. This means any "run" action must be able to execute all cells within 24 hours, or the kernel will timeout before the run completes.

## Concurrent active kernel limit[​](#concurrent-active-kernel-limit "Direct link to Concurrent active kernel limit")

Each Hex user can have up to 25 concurrent kernels. Workspaces on multi-tenant deployments can have up to 500 concurrent kernels total. If you reach the limit, free capacity by [stopping kernels manually](#stopping-active-kernels). These sessions count toward the limit:

* **Notebook sessions** — Count against the user who started the kernel; they last until stopped manually or by idle timeout.
* **Scheduled run sessions** — Count against the project owner; they end when the scheduled run completes.
* **Publish preview sessions** — Count against whoever triggered publish; they last until the run completes.
* **API run sessions** — Count against the API token creator; they last until the run completes.

## Stopping active kernels[​](#stopping-active-kernels "Direct link to Stopping active kernels")

If your workspace has reached its workspace kernel limit, an Admin can stop kernels in the workspace to bring it back under this limit.

Additionally, if an Editor is reaching their individual kernel limit, they can manage their own kernels.

To view the currently active kernels in a workspace, head to **Settings** > **Compute**. Then, choose to stop individual kernels, or stop all kernels.

#### On this page

* [What is a kernel?](#what-is-a-kernel)
* [Kernel status and actions](#kernel-status-and-actions)
  + [Kernel status](#kernel-status)
  + [Kernel actions](#kernel-actions)
* [Kernel timeouts](#kernel-timeouts)
  + [Idle timeout](#idle-timeout)
  + [Execution timeout](#execution-timeout)
* [Concurrent active kernel limit](#concurrent-active-kernel-limit)
* [Stopping active kernels](#stopping-active-kernels)