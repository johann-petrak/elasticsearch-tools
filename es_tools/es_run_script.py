#!/usr/bin/env python

import argparse
import elasticsearch7 as es
from time import sleep

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run script on index")
    parser.add_argument("-e", type=str, default="localhost",
                        help="Elasticsearch host (localhost)")
    parser.add_argument("-p", type=int, default=9901,
                        help="Elasticsearch port (9901)")
    parser.add_argument("-i", type=str, required=True,
                        help="Index name (required)")
    parser.add_argument("-f", type=str, required=True,
                        help="Script file")
    parser.add_argument("--timeout", type=int, default=3600,
                        help="Timeout in seconds (3600)")
    args = parser.parse_args()

    with open(args.f, "rt", encoding="utf-8") as infp:
        script = infp.read().replace("\n", " ")
    host = f"{args.e}:{args.p}"
    esclient = es.Elasticsearch(host, timeout=args.timeout, request_timeout=args.timeout)
    print("Connected to {args.s}:{args.p}:", esclient.info())
    response = esclient.update_by_query(index=args.i, body=dict(script=dict(source=script)), wait_for_completion=False)
    taskid = response["task"]
    print(f"Started task: {taskid}")
    while True:
        ret = esclient.tasks.get(task_id=taskid)
        if ret["completed"]:
            resp = ret["response"]
            took = resp["took"]
            total = resp["total"]
            updated = resp["updated"]
            created = resp["created"]
            deleted = resp["deleted"]
            print(f"\nTask completed, took {took}: {total} total, {updated} updated, {created} created, {deleted} deleted")
            break
        sleep(10)
        print(".", end="")
