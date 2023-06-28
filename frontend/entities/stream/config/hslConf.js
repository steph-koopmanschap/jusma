export const HSL_CONFIG = {
    autoStartLoad: true,
    startPosition: -1,
    debug: false,
    capLevelOnFPSDrop: false,
    capLevelToPlayerSize: false,
    defaultAudioCodec: undefined,
    initialLiveManifestSize: 3,
    maxBufferLength: 30,
    maxMaxBufferLength: 600,
    backBufferLength: Infinity,
    maxBufferSize: 60 * 1000 * 1000,
    maxBufferHole: 0.5,
    highBufferWatchdogPeriod: 2,
    nudgeOffset: 0.1,
    nudgeMaxRetry: 3,
    maxFragLookUpTolerance: 0.25,
    liveSyncDurationCount: 3,
    liveMaxLatencyDurationCount: 5,
    liveDurationInfinity: false,
    enableWorker: true,
    enableSoftwareAES: true,
    manifestLoadingTimeOut: 20000,
    manifestLoadingMaxRetry: 3,
    manifestLoadingRetryDelay: 2000,
    manifestLoadingMaxRetryTimeout: 64000,
    startLevel: undefined,
    levelLoadingTimeOut: 10000,
    levelLoadingMaxRetry: 4,
    levelLoadingRetryDelay: 1000,
    levelLoadingMaxRetryTimeout: 64000,
    fragLoadingTimeOut: 20000,
    fragLoadingMaxRetry: 6,
    fragLoadingRetryDelay: 1000,
    fragLoadingMaxRetryTimeout: 64000,
    startFragPrefetch: false,
    testBandwidth: true,
    progressive: false,
    lowLatencyMode: true,
    fpsDroppedMonitoringPeriod: 5000,
    fpsDroppedMonitoringThreshold: 0.2,
    appendErrorMaxRetry: 3
};
