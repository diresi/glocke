import argparse
import subprocess
import RPi.GPIO as G

PIN = 14


def do_your_thing(on_event):
    G.setmode(G.BCM)
    G.setup(PIN, G.IN, pull_up_down=G.PUD_UP)

    main_loop(on_event)


def main_loop(on_event):
    while True:
        once(on_event)


def once(on_event):
    # add some timeout to let interrupts like ^C work
    if G.wait_for_edge(PIN, G.FALLING, timeout=200):
        on_event(PIN)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run something on GPIO event",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--prog", help="program to run", default="/usr/bin/mpg123")
    parser.add_argument("--pin", type=int, default=PIN, help="GPIO pin")
    parser.add_argument("rest", nargs=argparse.REMAINDER)

    args = parser.parse_args()

    def on_event(pin):
        cmd = [args.prog] + args.rest
        subprocess.call(cmd)

    do_your_thing(on_event)
