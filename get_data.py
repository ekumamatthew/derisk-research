import pandas
import math

import classes
import constants
import db

latest_block = 0


def get_events() -> pandas.DataFrame:
    global latest_block
    print("getting events from block", latest_block)
    # Establish the connection.
    connection = db.establish_connection()

    # Load all Zklend events.
    zklend_events = pandas.read_sql(
        sql=f"""
      SELECT
          *
      FROM
          starkscan_events
      WHERE
          from_address='{constants.Protocol.ZKLEND.value}'
      AND
          key_name IN ('Deposit', 'Withdrawal', 'CollateralEnabled', 'CollateralDisabled', 'Borrowing', 'Repayment', 'Liquidation', 'AccumulatorsSync')
      AND
          block_number>{latest_block}
      ORDER BY
          block_number, id ASC;
      """,
        con=connection,
    )
    # Close the connection.
    connection.close()
    zklend_events.set_index("id", inplace=True)
    lb = zklend_events["block_number"].max()
    if not math.isnan(lb):
        latest_block = lb
    return zklend_events
