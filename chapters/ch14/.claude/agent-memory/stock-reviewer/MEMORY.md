# What stock-reviewer knows about the warehouse feed

- The README lists two known issues: some counts are keyed in as negative numbers, and a couple of deliveries carry product ids that are not in the product list. dbt's two warnings (`assert_no_negative_on_hand` and the `relationships` test on `stg_receipts.product_id`) are these same two issues.
- A negative count is a keying error at the store. It goes back to the store for a recount and is never ordered against.
- A delivery for an unknown product is reported with its receipt id. The product list or the delivery has the wrong id, and only the warehouse team can say which.
