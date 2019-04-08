Any secrets greater than the AWS Parameter store value limit 4096 characters will be broken up into chunks and suffixed `_chunk_<index>`

The chunk indices will be formatted with 3 leading zeros, and beginning the count at `000`
- e.g 
    - `secret_chunk_000`
    - `secret_chunk_001`
    - `secret_chunk_003`
    
    
# Cases Handled
Secret A split into chunks
- `A` -> `A_chunk_000` + `A_chunk_001` ...

Secret A value has shortened and now there is a reduction in chunk size. This is handled with a `CHUNK_TERMINATION_VALUE` environment variable which defaults to `NULL`.
This is due to AWS Parameter Store not allowing empty string values
- `A_chunk_0` + `A_chunk_1` + `A_chunk_2` -> `A_chunk_0` + `A_chunk_1`
    - with `A_chunk_2` value becoming `NULL` for history auditing
- `A_chunk_0` + `A_chunk_1` -> `A_chunk_0`
    - with `A_chunk_1` value becoming `NULL` for history auditing
    - In this case, all future updates will happen to `A_chunk_0` and not revert to the unchunked key name `A`.
    
Secret A was created but now the new value has exceed value size limitation. The new chunked secret is uploaded & the old key is flagged for expiration.
- `A` -> `A_chunk_0` + `A_chunk_1`
- `A` -> expired

