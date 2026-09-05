#!/usr/bin/env bash
# wait_for_emulator.sh
# Verifies adb availability and waits until the Android emulator has fully booted.
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

echo "==> Waiting for emulator device to attach (adb wait-for-device)..."
adb wait-for-device

echo "==> Waiting for Android OS boot completion (timeout: ${TIMEOUT_SECONDS}s)..."
start_time=$(date +%s)

while true; do
    boot_completed=$(adb shell getprop sys.boot_completed 2>/dev/null | tr -d '\r' || true)

    if [ "$boot_completed" = "1" ]; then
        echo "==> Android emulator is fully booted and ready (sys.boot_completed = 1)."
        adb devices
        exit 0
    fi

    current_time=$(date +%s)
    elapsed=$(( current_time - start_time ))

    if [ "$elapsed" -ge "$TIMEOUT_SECONDS" ]; then
        echo "ERROR: Timed out after ${TIMEOUT_SECONDS}s waiting for emulator boot completion." >&2
        adb devices >&2 || true
        exit 1
    fi

    sleep "$POLL_INTERVAL"
done
