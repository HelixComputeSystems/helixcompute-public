# Verification and reproduction levels

Evidence Release v1 uses the following controlled vocabulary.

## `RECEIPT_VERIFICATION`

A reviewer can verify hashes, recorded arithmetic, declared gates, and any
published equality digests. The original workload is not rerun.

## `FIXTURE_REPRODUCTION`

A public fixture and implementation can rerun a bounded workload and regenerate
the recorded output. No v1 claim currently carries this level.

## `INDEPENDENT_EXPERIMENT`

An independent implementation can recreate the method and test the claim
without relying on private Core. No v1 claim currently carries this level.

All v1 receipts are `RECEIPT_VERIFICATION`. Describing them as independently
reproducible would overstate what is public.
