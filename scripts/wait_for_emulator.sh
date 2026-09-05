#!/usr/bin/env bash
# wait_for_emulator.sh
# Verifies adb availability and waits until the Android emulator has attached and fully booted.
# Strictly an environment/setup utility; never invoked or managed by pytest.

set -euo pipefail

TIMEOUT_SECONDS="${EMULATOR_BOOT_TIMEOUT_SECONDS:-120}"
POLL_INTERVAL=2

echo "==> Checking adb tool availability..."
if ! command -v adb >/dev/null 2>&1; then
    echo "ERROR: 'adb' command not found in PATH." >&2
    echo "Please install Android Platform Tools and ensure 'adb' is in your PATH." >&2
    exit 1
fi

echo "==> Waiting for Android emulator attachment and boot completion (timeout: ${TIMEOUT_SECONDS}s)..."
start_time=$(date +%s)

while true; do
    if adb -e get-state >/dev/null 2>&1; then
        boot_completed=$(adb -e shell getprop sys.boot_completed 2>/dev/null | tr -d '\r' || true)

        if [ "$boot_completed" = "1" ]; then
            echo "==> Android emulator is attached and fully booted (sys.boot_completed = 1)."
            adb devices
            exit 0
        fi
    fi

    current_time=$(date +%s)
    elapsed=$(( current_time - start_time ))

    if [ "$elapsed" -ge "$TIMEOUT_SECONDS" ]; then
        echo "ERROR: Timed out after ${TIMEOUT_SECONDS}s waiting for Android emulator readiness." >&2
        adb devices >&2 || true
        exit 1
    fi

    sleep "$POLL_INTERVAL"
done
