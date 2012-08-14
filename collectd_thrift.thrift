struct CollectdData {
    1: i64 timestamp,
    2: string env,
    3: string instance,
    4: string dev,
    5: string vtype, 
    6: i64 value
}

service OpenTSDBUpload {
    void upload(1: CollectdData d)
}
