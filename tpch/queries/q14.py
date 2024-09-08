from datetime import datetime

import narwhals as nw
from narwhals.typing import FrameT


@nw.narwhalify
def query(line_item_ds: FrameT, part_ds: FrameT) -> FrameT:
    var1 = datetime(1995, 9, 1)
    var2 = datetime(1995, 10, 1)

    return (
        line_item_ds.join(part_ds, left_on="l_partkey", right_on="p_partkey")
        .filter(nw.col("l_shipdate").is_between(var1, var2, closed="left"))
        .select(
            (
                100.00
                * nw.when(nw.col("p_type").str.contains("PROMO*"))
                .then(nw.col("l_extendedprice") * (1 - nw.col("l_discount")))
                .otherwise(0)
                .sum()
                / (nw.col("l_extendedprice") * (1 - nw.col("l_discount"))).sum()
            )
            .round(2)
            .alias("promo_revenue")
        )
    )