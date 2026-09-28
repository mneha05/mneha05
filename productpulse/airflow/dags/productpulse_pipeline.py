from __future__ import annotations

import json
from datetime import datetime, timedelta
from pathlib import Path

from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator

DATA = Path('/opt/airflow/data/events.jsonl')

with DAG(
    dag_id='productpulse_daily',
    start_date=datetime(2026, 9, 1),
    schedule='0 6 * * *',
    catchup=False,
    default_args={'retries': 2, 'retry_delay': timedelta(minutes=2)},
    tags=['product-analytics', 'trino', 'dbt'],
) as dag:

    generate = BashOperator(
        task_id='generate_events',
        bash_command='python /opt/airflow/project/generator/generate_events.py --users 5000 --days 14 --out /opt/airflow/data/events.jsonl',
    )

    @task
    def load_to_iceberg() -> int:
        import trino
        rows = [json.loads(x) for x in DATA.read_text().splitlines()]
        conn = trino.dbapi.connect(host='trino', port=8080, user='airflow', catalog='iceberg', schema='productpulse')
        cur = conn.cursor()
        bootstrap = Path('/opt/airflow/project/sql/bootstrap.sql').read_text()
        for statement in (s.strip() for s in bootstrap.split(';')):
            if statement:
                cur.execute(statement)
                cur.fetchall()
        batch = 250
        inserted = 0
        for i in range(0, len(rows), batch):
            chunk = rows[i:i+batch]
            values = []
            for r in chunk:
                vals = [r[k] for k in ('event_id','user_id','event_name','event_ts','event_date','session_id','country','platform','experiment_arm','feature_name')]
                q = []
                for idx, v in enumerate(vals):
                    if v is None:
                        q.append('NULL')
                    else:
                        escaped = str(v).replace("'", "''")
                        if idx == 3:
                            q.append(f"from_iso8601_timestamp('{escaped}')")
                        elif idx == 4:
                            q.append(f"date '{escaped}'")
                        else:
                            q.append(f"'{escaped}'")
                values.append('(' + ','.join(q) + ',current_timestamp)')
            cur.execute('INSERT INTO iceberg.productpulse.raw_events VALUES ' + ','.join(values))
            cur.fetchall()
            inserted += len(chunk)
        return inserted

    dbt = BashOperator(
        task_id='dbt_build',
        bash_command='cd /opt/airflow/project/dbt && dbt build --profiles-dir .',
    )

    generate >> load_to_iceberg() >> dbt
