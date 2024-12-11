# Setting up your VS Code environment with Magnificent Custom Debuggers

This guide walks you through setting up a local debugging environment that allows you to:

- Run your project in the background using `npm run dev`.
- Attach VS Code’s debugger to Chrome, preserving your existing browser session (so you stay logged in).
- Set breakpoints and inspect variables directly in VS Code.

## Prerequisites

- **Node.js and npm**: Ensure you have Node.js (LTS) installed.
- **Chrome Browser**: You’ll need Google Chrome installed.
- **VS Code**: The latest version with the built-in JavaScript debugger.
- **SvelteKit + Vite Project**: A SvelteKit app using Vite as the dev server.

## Steps Overview

1. **Enable Source Maps in Vite**
2. **Set Up Your `tasks.json`**
3. **Set Up Your `launch.json`**
4. **Start Chrome with Remote Debugging**
5. **Run and Debug in VS Code**
6. **Set Breakpoints and Debug**

---

## 1. Enable Source Maps in Vite

To map breakpoints in VS Code back to your original source files, you need source maps. In your `vite.config.js` (or if your configuration is elsewhere, adjust accordingly), enable `sourcemap`:

```javascript
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [sveltekit()],
  build: {
    sourcemap: true
  }
});
```
Resatart your dev server after making this change:

```
npm run dev
```

## 2. Set Up `tasks.json`

In your project’s .vscode folder, create or update tasks.json to run npm run dev as a background task. This allows VS Code to know when your development server (Vite) is ready:

```
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "dev",
      "type": "npm",
      "script": "dev",
      "isBackground": true,
      "problemMatcher": {
        "owner": "custom",
        "pattern": [
          {
            "regexp": "^(.*)$",
            "message": 1
          }
        ],
        "background": {
          "activeOnStart": true,
          "beginsPattern": "use --host",
          "endsPattern": "terminated"
        }
      }
    }
  ]
}
```

**What This Does:***

Runs `npm run dev`.
- Waits until it sees "use --host" in the output (adjust if your server logs something else) before considering the server ready.
- Keeps running in the background so the website is continuously served at http://localhost:5173.

## Set Up launch.json
In `.vscode/launch.json`, create a configuration to attach to an existing Chrome instance. We’ll rely on you starting Chrome separately, so you can remain logged in:

```
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Attach Debugger to Existing Chrome Instance",
            "type": "pwa-chrome",
            "request": "attach",
            "port": 9222,
            "urlFilter": "http://localhost:5173/*",
            "webRoot": "C:\\Users\\samue\\Downloads\\softigital-deckhub-frontend-f42a4e76ee6d",
            "sourceMaps": true,
            "preLaunchTask": "dev"
          },
      {
        "name": "Debug Flask App",
        "type": "debugpy",
        "request": "launch",
        "program": "C:\\Users\\samue\\Downloads\\softigital-deckhub-frontend-f42a4e76ee6d\\src\\backend\\app.py",
        "console": "integratedTerminal",
        "args": ["run", "--no-debugger", "--no-reload"],
        "env": {
          "FLASK_APP": "app.py",
          "FLASK_ENV": "development"
        },
        "jinja": true,
        "cwd": "C:\\Users\\samue\\Downloads\\softigital-deckhub-frontend-f42a4e76ee6d\\src\\backend"  // Set the correct working directory
      }
    ]
  }
```

What This Does:

- Attaches to a Chrome instance on port 9222.
- Targets the URL http://localhost:5173/*.
- Runs the dev task before attaching so the server is up and running.
- Uses webRoot to map source files correctly and sourceMaps: true to leverage Vite’s source maps.

## Start Chrome with Remote Debugging
To preserve your login session:

1. Close all Chrome instances.
2. Open Chrome with remote debugging enabled:
`C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\ChromeDebugProfile
- Ensure the path to Chrome is correct.
- The --user-data-dir argument creates a fresh profile for debugging. Remove it if you prefer using your existing profile, but close all other Chrome instances first.
3. In the opened Chrome window, navigate to http://localhost:5173 and log in to your application. Keep this window open.

## 5. Run and Debug in VS Code
In VS Code:

1. Open the Run and Debug view (`Ctrl+Shift+D`).
2. Select "Attach to Existing Chrome with Dev Server".
3. Press F5 to start debugging.
4. VS Code will:
- Run the dev task to start the Vite server.
- Attach the debugger to the already running Chrome instance on port 9222.
- Since you opened http://localhost:5173 in Chrome and are logged in, the debugger can now map your breakpoints to the correct running code.

## 6. Set Breakpoints and Debug
- Open your Svelte or js files in VS Code.
- Click in the gutter next to a line number to set a breakpoint.
- Interact with your app in Chrome. When the code at the breakpoint executes, VS Code should pause.
- Inspect variables, the call stack, and step through code in VS Code’s debug panel.

**If Breakpoints Don’t Hit:**
- Confirm source maps are enabled in vite.config.js.
- Double-check webRoot in launch.json is correct.
- Ensure the dev server output matches the beginsPattern in tasks.json.
- Add a debugger; statement in your code and reload the page to test if the debugger pauses.