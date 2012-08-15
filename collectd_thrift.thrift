struct CollectdData {
    1: i64 timestamp,
    2: string env,
    3: string instance,
    4: string dev,
    5: string vtype, 
    6: i64 value
}

struct CollectdDataV2 {
    1: i64 timestamp,
    2: string env,
    3: string instance,
    4: string dev,
    5: string vtype, 
    6: i64 value,
    7: string cnode,
    8: string tenant
}

service OpenTSDBUpload {
    void upload(1: CollectdData d)
}

service OpenTSDBUploadV2 {
    void upload(1: CollectdDataV2 d)
}
