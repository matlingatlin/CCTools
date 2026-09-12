/**
 * CTRF TypeScript Types
 * Generated from the CTRF JSON Schema specification
 */
/**
 * The root CTRF report object
 *
 * @group Core Types
 */
interface CTRFReport {
    /** Must be 'CTRF' */
    reportFormat: "CTRF";
    /** Semantic version of the CTRF specification */
    specVersion: string;
    /** Unique identifier for this report (UUID v4) */
    reportId?: string;
    /** Identifier shared by all documents belonging to the same logical test run */
    runId?: string;
    /** ISO 8601 timestamp when the report was generated */
    timestamp?: string;
    /** Name of the tool/library that generated this report */
    generatedBy?: string;
    /** The test results */
    results: Results;
    /** Run-level insights computed from historical data */
    insights?: Insights;
    /** Reference to a baseline report for comparison */
    baseline?: Baseline;
    /** Custom metadata */
    extra?: Record<string, unknown>;
}
/**
 * Container for test results
 *
 * @group Core Types
 */
interface Results {
    /** Information about the test tool */
    tool: Tool;
    /** Aggregated test statistics */
    summary: Summary;
    /** Array of individual test results */
    tests: Test[];
    /** Environment information */
    environment?: Environment;
    /** Custom metadata */
    extra?: Record<string, unknown>;
}
/**
 * Test tool information
 *
 * @group Core Types
 */
interface Tool {
    /** Name of the test tool (e.g., 'jest', 'playwright') */
    name: string;
    /** Version of the test tool */
    version?: string;
    /** Custom metadata */
    extra?: Record<string, unknown>;
}
/**
 * Aggregated test statistics
 *
 * @group Core Types
 */
interface Summary {
    /** Total number of tests */
    tests: number;
    /** Number of passed tests */
    passed: number;
    /** Number of failed tests */
    failed: number;
    /** Number of skipped tests */
    skipped: number;
    /** Number of pending tests */
    pending: number;
    /** Number of tests with other status */
    other: number;
    /** Number of flaky tests */
    flaky?: number;
    /** Number of test suites */
    suites?: number;
    /** Start timestamp (Unix epoch milliseconds) */
    start: number;
    /** Stop timestamp (Unix epoch milliseconds) */
    stop: number;
    /** Total duration in milliseconds */
    duration?: number;
    /** Custom metadata */
    extra?: Record<string, unknown>;
}
/**
 * Individual test result
 *
 * @group Core Types
 */
interface Test {
    /** Legacy test identifier (UUID); new producers should prefer testId */
    id?: string;
    /** Stable identifier for the logical test case */
    testId?: string;
    /** Identifier for this specific execution of the test case */
    executionId?: string;
    /** Test name */
    name: string;
    /** Test execution status */
    status: TestStatus;
    /** Test duration in milliseconds */
    duration: number;
    /** Start timestamp (Unix epoch milliseconds) */
    start?: number;
    /** Stop timestamp (Unix epoch milliseconds) */
    stop?: number;
    /** Test suite hierarchy */
    suite?: string[];
    /** Error message (for failed tests) */
    message?: string;
    /** Stack trace (for failed tests) */
    trace?: string;
    /** Code snippet where failure occurred */
    snippet?: string;
    /** AI-generated analysis or suggestion */
    ai?: string;
    /** Line number where test is defined or failed */
    line?: number;
    /** Original status from the test framework */
    rawStatus?: string;
    /** Tags for categorization */
    tags?: string[];
    /** Structured key-value metadata; values may be scalar or multi-valued */
    labels?: Record<string, LabelValue>;
    /** Test type (e.g., 'unit', 'integration', 'e2e') */
    type?: string;
    /** Path to the test file */
    filePath?: string;
    /** Number of retry attempts */
    retries?: number;
    /** Details of each retry attempt */
    retryAttempts?: RetryAttempt[];
    /** Whether the test is flaky */
    flaky?: boolean;
    /** Standard output captured during test */
    stdout?: string[];
    /** Standard error captured during test */
    stderr?: string[];
    /** Thread/worker ID that ran this test */
    threadId?: string;
    /** Browser name (for browser tests) */
    browser?: string;
    /** Device name (for device tests) */
    device?: string;
    /** Base64 encoded screenshot */
    screenshot?: string;
    /** File attachments */
    attachments?: Attachment[];
    /** Test parameters (for parameterized tests) */
    parameters?: Record<string, unknown>;
    /** Test steps */
    steps?: Step[];
    /** Test-level insights */
    insights?: TestInsights;
    /** Custom metadata */
    extra?: Record<string, unknown>;
}
/**
 * Test status enum
 *
 * @group Core Types
 */
type TestStatus = "passed" | "failed" | "skipped" | "pending" | "other";
/** Primitive value supported by a test label */
type LabelPrimitive = string | number | boolean;
/** Scalar or non-empty multi-valued test label value */
type LabelValue = LabelPrimitive | [LabelPrimitive, ...LabelPrimitive[]];
/**
 * Details of a test retry attempt
 *
 * @group Core Types
 */
interface RetryAttempt {
    /** Attempt number (1-indexed) */
    attempt: number;
    /** Identifier for this individual attempt */
    attemptId?: string;
    /** Status of this attempt */
    status: TestStatus;
    /** Duration of this attempt in milliseconds */
    duration?: number;
    /** Error message */
    message?: string;
    /** Stack trace */
    trace?: string;
    /** Line number */
    line?: number;
    /** Code snippet */
    snippet?: string;
    /** Standard output */
    stdout?: string[];
    /** Standard error */
    stderr?: string[];
    /** Start timestamp */
    start?: number;
    /** Stop timestamp */
    stop?: number;
    /** Attachments for this attempt */
    attachments?: Attachment[];
    /** Custom metadata */
    extra?: Record<string, unknown>;
}
/**
 * File attachment
 *
 * @group Core Types
 */
interface Attachment {
    /** Identifier for this attachment reference instance */
    attachmentId?: string;
    /** Attachment name */
    name: string;
    /** MIME content type */
    contentType: string;
    /** Path to the attachment file */
    path: string;
    /** Custom metadata */
    extra?: Record<string, unknown>;
}
/**
 * Test step
 *
 * @group Core Types
 */
interface Step {
    /** Step name */
    name: string;
    /** Step status */
    status: TestStatus;
    /** Custom metadata */
    extra?: Record<string, unknown>;
}
/**
 * Environment information
 *
 * @group Core Types
 */
interface Environment {
    /** Custom report name */
    reportName?: string;
    /** Application name */
    appName?: string;
    /** Application version */
    appVersion?: string;
    /** Build identifier */
    buildId?: string;
    /** Build name */
    buildName?: string;
    /** Build number */
    buildNumber?: number;
    /** Build URL */
    buildUrl?: string;
    /** Repository name */
    repositoryName?: string;
    /** Repository URL */
    repositoryUrl?: string;
    /** Git commit SHA */
    commit?: string;
    /** Git branch name */
    branchName?: string;
    /** Operating system platform */
    osPlatform?: string;
    /** Operating system release */
    osRelease?: string;
    /** Operating system version */
    osVersion?: string;
    /** Test environment name */
    testEnvironment?: string;
    /** Shard or partition that produced this document */
    shardId?: string;
    /** Whether the environment is healthy */
    healthy?: boolean;
    /** Custom metadata */
    extra?: Record<string, unknown>;
}
/**
 * Run-level insights computed from historical data
 *
 * @group Insights
 */
interface Insights {
    /** Pass rate metric */
    passRate?: MetricDelta;
    /** Fail rate metric */
    failRate?: MetricDelta;
    /** Flaky rate metric */
    flakyRate?: MetricDelta;
    /** Average run duration metric */
    averageRunDuration?: MetricDelta;
    /** 95th percentile run duration metric */
    p95RunDuration?: MetricDelta;
    /** Average test duration metric */
    averageTestDuration?: MetricDelta;
    /** Number of historical runs analyzed */
    runsAnalyzed?: number;
    /** Custom metadata */
    extra?: Record<string, unknown>;
}
/**
 * Test-level insights computed from historical data
 *
 * @group Insights
 */
interface TestInsights {
    /** Pass rate metric */
    passRate?: MetricDelta;
    /** Fail rate metric */
    failRate?: MetricDelta;
    /** Flaky rate metric */
    flakyRate?: MetricDelta;
    /** Average test duration metric */
    averageTestDuration?: MetricDelta;
    /** 95th percentile test duration metric */
    p95TestDuration?: MetricDelta;
    /** Number of runs this test was executed in */
    executedInRuns?: number;
    /** Custom metadata */
    extra?: Record<string, unknown>;
}
/**
 * Metric with current value, baseline, and change
 *
 * @group Insights
 */
interface MetricDelta {
    /** Current value */
    current?: number;
    /** Baseline value for comparison */
    baseline?: number;
    /** Change from baseline (current - baseline) */
    change?: number;
}
/**
 * Reference to a baseline report
 *
 * @group Core Types
 */
interface Baseline {
    /** Report ID of the baseline report */
    reportId: string;
    /** Timestamp of the baseline report */
    timestamp?: string;
    /** Source description (e.g., 'main-branch', 'previous-run') */
    source?: string;
    /** Build number of the baseline */
    buildNumber?: number;
    /** Build name of the baseline */
    buildName?: string;
    /** Build URL of the baseline */
    buildUrl?: string;
    /** Git commit of the baseline */
    commit?: string;
    /** Custom metadata */
    extra?: Record<string, unknown>;
}
/**
 * Result of schema validation
 *
 * @group Validation Options
 */
interface ValidationResult {
    /** Whether the report is valid */
    valid: boolean;
    /** Array of validation errors */
    errors: ValidationErrorDetail[];
}
/**
 * Details of a validation error
 *
 * @group Validation Options
 */
interface ValidationErrorDetail {
    /** Human-readable error message */
    message: string;
    /** JSON path to the error location */
    path: string;
    /** JSON Schema keyword that failed */
    keyword: string;
}
/**
 * Options for merging reports
 *
 * @group Merge Options
 */
interface MergeOptions {
    /** Remove duplicate tests by executionId, testId, or legacy id */
    deduplicateTests?: boolean;
    /** Recalculate summary from merged tests */
    mergeSummary?: boolean;
    /** Strategy for handling environments */
    preserveEnvironment?: "first" | "last" | "merge";
}
/**
 * Criteria for filtering and finding tests.
 *
 * @group Query & Filter Options
 */
interface FilterCriteria {
    /** Filter by legacy test ID (UUID) */
    id?: string;
    /** Filter by stable logical test case ID */
    testId?: string;
    /** Filter by a specific test execution ID */
    executionId?: string;
    /** Filter by test name */
    name?: string;
    /** Filter by status */
    status?: TestStatus | TestStatus[];
    /** Filter by tags */
    tags?: string | string[];
    /** Filter by suite */
    suite?: string | string[];
    /** Filter by flaky flag */
    flaky?: boolean;
    /** Filter by browser */
    browser?: string;
    /** Filter by device */
    device?: string;
}
/**
 * Options for insights calculation
 *
 * @group Insights Options
 */
interface InsightsOptions {
    /** Baseline report for comparison */
    baseline?: CTRFReport;
    /** Number of historical reports to analyze */
    window?: number;
}
/**
 * Options for ReportBuilder
 *
 * @group Builder Options
 */
interface ReportBuilderOptions {
    /** Automatically generate report ID */
    autoGenerateId?: boolean;
    /** Automatically set timestamp */
    autoTimestamp?: boolean;
}
/**
 * Options for TestBuilder
 *
 * @group Builder Options
 */
interface TestBuilderOptions {
    /** Automatically generate test ID */
    autoGenerateId?: boolean;
}
/**
 * Options for calculating summary
 *
 * @group Core Options
 */
interface SummaryOptions {
    /** Start timestamp */
    start?: number;
    /** Stop timestamp */
    stop?: number;
}
/**
 * Options for parsing JSON
 *
 * @group Core Options
 */
interface ParseOptions {
    /** Validate after parsing */
    validate?: boolean;
}
/**
 * Options for stringifying to JSON
 *
 * @group Core Options
 */
interface StringifyOptions {
    /** Pretty print with indentation */
    pretty?: boolean;
    /** Number of spaces for indentation (default: 2) */
    indent?: number;
}
/**
 * Options for validation
 *
 * @group Validation Options
 */
interface ValidateOptions {
    /** Specific spec version to validate against */
    specVersion?: string;
}

/**
 * CTRF Constants
 */
/** The CTRF report format identifier */
declare const REPORT_FORMAT: "CTRF";
/** Current spec version */
declare const CURRENT_SPEC_VERSION = "0.0.0";
/** All valid test statuses */
declare const TEST_STATUSES: readonly ["passed", "failed", "skipped", "pending", "other"];
/** Supported specification versions */
declare const SUPPORTED_SPEC_VERSIONS: readonly ["0.0.0"];
/** CTRF namespace UUID for deterministic ID generation */
declare const CTRF_NAMESPACE = "6ba7b810-9dad-11d1-80b4-00c04fd430c8";

/**
 * CTRF Validation
 */

/**
 * Validate a CTRF report against the JSON schema.
 *
 * @group Core Operations
 * @param report - The object to validate
 * @param options - Validation options (e.g., specific spec version)
 * @returns Validation result containing `valid` boolean and `errors` array
 *
 * @example
 * ```typescript
 * const result = validate(report);
 * if (!result.valid) {
 *   console.log(result.errors);
 * }
 *
 * // Validate against specific version
 * const result = validate(report, { specVersion: '1.0.0' });
 * ```
 */
declare function validate(report: unknown, options?: ValidateOptions): ValidationResult;
/**
 *
 * @group Core Operations
 * Check if a report is valid (type guard).
 *
 * @param report - The object to validate
 * @returns true if the report is a valid CTRFReport
 *
 * @example
 * ```typescript
 * if (isValid(report)) {
 *   // TypeScript now knows report is CTRFReport
 *   console.log(report.results.summary.passed);
 * }
 * ```
 */
declare function isValid(report: unknown): report is CTRFReport;
/**
 *
 * @group Core Operations
 * Validate a report and throw if invalid (assertion).
 *
 * @param report - The object to validate
 * @throws ValidationError if the report is invalid
 *
 * @example
 * ```typescript
 * try {
 *   validateStrict(report);
 *   // TypeScript now knows report is CTRFReport
 * } catch (e) {
 *   if (e instanceof ValidationError) {
 *     console.log(e.errors);
 *   }
 * }
 * ```
 */
declare function validateStrict(report: unknown): asserts report is CTRFReport;
/**
 *
 * @group Type Guards
 * Checks if an object has the basic structure of a CTRF report.
 * This is a quick, lightweight check that doesn't validate against the full schema.
 *
 * @param report - The object to check
 * @returns true if the object appears to be a CTRF report
 *
 * @example
 * ```typescript
 * if (isCTRFReport(data)) {
 *   // data has reportFormat: 'CTRF'
 * }
 * ```
 */
declare function isCTRFReport(report: unknown): report is {
    reportFormat: "CTRF";
};
/**
 *
 * @group Type Guards
 * Type guard for Test objects.
 *
 * @param obj - Object to check
 * @returns true if the object is a Test
 */
declare function isTest(obj: unknown): obj is {
    name: string;
    status: string;
    duration: number;
};
/**
 *
 * @group Type Guards
 * Type guard for TestStatus values.
 *
 * @param value - Value to check
 * @returns true if the value is a valid TestStatus
 */
declare function isTestStatus(value: unknown): value is (typeof TEST_STATUSES)[number];
/**
 *
 * @group Type Guards
 * Type guard for RetryAttempt objects.
 *
 * @param obj - Object to check
 * @returns true if the object is a RetryAttempt
 */
declare function isRetryAttempt(obj: unknown): obj is {
    attempt: number;
    status: string;
};
/**
 *
 * @group Type Guards
 * Check if a report has insights.
 *
 * @param report - The report to check
 * @returns true if the report has insights
 */
declare function hasInsights(report: CTRFReport): boolean;

/**
 * CTRF Summary Calculation
 */

/**
 *
 * @group Core Operations
 * Calculate summary statistics from an array of tests.
 *
 * @param tests - Array of test results
 * @param options - Optional timing information
 * @returns Calculated summary object
 *
 * @example
 * ```typescript
 * const summary = calculateSummary(tests);
 *
 * // With timing
 * const summary = calculateSummary(tests, {
 *   start: 1704067200000,
 *   stop: 1704067260000
 * });
 * ```
 */
declare function calculateSummary(tests: Test[], options?: SummaryOptions): Summary;

/**
 * CTRF Report and Test Builders
 * Fluent API for constructing CTRF reports
 */

/**
 *
 * @group Builders
 * Fluent builder for constructing CTRF reports.
 *
 * @example
 * ```typescript
 * const report = new ReportBuilder()
 *   .specVersion('1.0.0')
 *   .tool({ name: 'jest', version: '29.0.0' })
 *   .environment({ branchName: 'main' })
 *   .addTest(
 *     new TestBuilder()
 *       .name('should add numbers')
 *       .status('passed')
 *       .duration(150)
 *       .build()
 *   )
 *   .build();
 * ```
 */
declare class ReportBuilder {
    private _specVersion;
    private _reportId?;
    private _runId?;
    private _timestamp?;
    private _generatedBy?;
    private _tool?;
    private _environment?;
    private _tests;
    private _insights?;
    private _baseline?;
    private _extra?;
    private _summaryOverrides?;
    constructor(options?: ReportBuilderOptions);
    /**
     * Set the spec version.
     */
    specVersion(version: string): this;
    /**
     * Set or generate the report ID.
     * @param uuid - UUID to use, or undefined to auto-generate
     */
    reportId(uuid?: string): this;
    /**
     * Set the logical test run ID shared across related CTRF documents.
     */
    runId(id: string): this;
    /**
     * Set the timestamp.
     * @param date - Date to use, or undefined for current time
     */
    timestamp(date?: Date | string): this;
    /**
     * Set the generator name.
     */
    generatedBy(name: string): this;
    /**
     * Set the tool information.
     */
    tool(tool: Tool): this;
    /**
     * Set the environment information.
     */
    environment(env: Environment): this;
    /**
     * Add a single test.
     */
    addTest(test: Test): this;
    /**
     * Add multiple tests.
     */
    addTests(tests: Test[]): this;
    /**
     * Set run-level insights.
     */
    insights(insights: Insights): this;
    /**
     * Set the baseline reference.
     */
    baseline(baseline: Baseline): this;
    /**
     * Set extra metadata.
     */
    extra(data: Record<string, unknown>): this;
    /**
     * Override specific summary fields.
     * Useful when you want to set specific timing or counts.
     */
    summaryOverrides(overrides: Partial<Summary>): this;
    /**
     * Build and return the CTRF report.
     * @throws BuilderError if required fields are missing
     */
    build(): CTRFReport;
}
/**
 *
 * @group Builders
 * Fluent builder for constructing Test objects.
 *
 * @example
 * ```typescript
 * const test = new TestBuilder()
 *   .name('should add numbers')
 *   .status('passed')
 *   .duration(150)
 *   .suite(['math', 'addition'])
 *   .build();
 * ```
 */
declare class TestBuilder {
    private options;
    private _id?;
    private _testId?;
    private _executionId?;
    private _name?;
    private _status?;
    private _duration?;
    private _start?;
    private _stop?;
    private _suite?;
    private _message?;
    private _trace?;
    private _snippet?;
    private _ai?;
    private _line?;
    private _rawStatus?;
    private _tags?;
    private _labels?;
    private _type?;
    private _filePath?;
    private _retries?;
    private _retryAttempts?;
    private _flaky?;
    private _stdout?;
    private _stderr?;
    private _threadId?;
    private _browser?;
    private _device?;
    private _screenshot?;
    private _attachments?;
    private _parameters?;
    private _steps?;
    private _insights?;
    private _extra?;
    constructor(options?: TestBuilderOptions);
    /**
     * Set or generate the test ID.
     * @param uuid - UUID to use, or undefined to auto-generate based on properties
     */
    id(uuid?: string): this;
    /**
     * Set the stable logical test case ID.
     */
    testId(id: string): this;
    /**
     * Set the identifier for this specific test execution.
     */
    executionId(id: string): this;
    /**
     * Set the test name.
     */
    name(name: string): this;
    /**
     * Set the test status.
     */
    status(status: TestStatus): this;
    /**
     * Set the duration in milliseconds.
     */
    duration(ms: number): this;
    /**
     * Set the start timestamp.
     */
    start(timestamp: number): this;
    /**
     * Set the stop timestamp.
     */
    stop(timestamp: number): this;
    /**
     * Set the suite hierarchy.
     */
    suite(suites: string[]): this;
    /**
     * Set the error message.
     */
    message(msg: string): this;
    /**
     * Set the stack trace.
     */
    trace(trace: string): this;
    /**
     * Set the code snippet.
     */
    snippet(code: string): this;
    /**
     * Set AI-generated analysis.
     */
    ai(analysis: string): this;
    /**
     * Set the line number.
     */
    line(num: number): this;
    /**
     * Set the raw status from the test framework.
     */
    rawStatus(status: string): this;
    /**
     * Set tags.
     */
    tags(tags: string[]): this;
    /**
     * Set structured labels.
     */
    labels(labels: Record<string, LabelValue>): this;
    /**
     * Set test type.
     */
    type(type: string): this;
    /**
     * Set file path.
     */
    filePath(path: string): this;
    /**
     * Set retry count.
     */
    retries(count: number): this;
    /**
     * Add a retry attempt.
     */
    addRetryAttempt(attempt: RetryAttempt): this;
    /**
     * Mark as flaky.
     */
    flaky(isFlaky?: boolean): this;
    /**
     * Set stdout.
     */
    stdout(lines: string[]): this;
    /**
     * Set stderr.
     */
    stderr(lines: string[]): this;
    /**
     * Set thread ID.
     */
    threadId(id: string): this;
    /**
     * Set browser name.
     */
    browser(name: string): this;
    /**
     * Set device name.
     */
    device(name: string): this;
    /**
     * Set screenshot (base64).
     */
    screenshot(base64: string): this;
    /**
     * Add an attachment.
     */
    addAttachment(attachment: Attachment): this;
    /**
     * Set parameters.
     */
    parameters(params: Record<string, unknown>): this;
    /**
     * Add a step.
     */
    addStep(step: Step): this;
    /**
     * Set test-level insights.
     */
    insights(insights: TestInsights): this;
    /**
     * Set extra metadata.
     */
    extra(data: Record<string, unknown>): this;
    /**
     * Build and return the Test object.
     * @throws BuilderError if required fields are missing
     */
    build(): Test;
}

/**
 * CTRF Test ID Generation
 */
/**
 *
 * @group ID Generation
 * Generate a deterministic UUID v5 for a test based on its properties.
 * The same inputs will always produce the same UUID, enabling
 * cross-run analysis and test identification.
 *
 * @param properties - Test properties to generate ID from
 * @param properties.name - Test name (required)
 * @param properties.suite - Suite hierarchy (optional)
 * @param properties.filePath - File path (optional)
 * @returns A deterministic UUID v5 string
 *
 * @example
 * ```typescript
 * const id = generateTestId({
 *   name: 'should add numbers',
 *   suite: ['math', 'addition'],
 *   filePath: 'tests/math.test.ts'
 * });
 * // Always returns the same UUID for these inputs
 * ```
 */
declare function generateTestId(properties: {
    name: string;
    suite?: string[];
    filePath?: string;
}): string;
/**
 *
 * @group ID Generation
 * Generate a random UUID v4 for report identification.
 *
 * @returns A random UUID v4 string
 *
 * @example
 * ```typescript
 * const reportId = generateReportId();
 * // => 'f47ac10b-58cc-4372-a567-0e02b2c3d479'
 * ```
 */
declare function generateReportId(): string;

/**
 * CTRF Parsing and Serialization
 */

/**
 *
 * @group Core Operations
 * Parse a JSON string into a CTRFReport.
 *
 * @param json - JSON string to parse
 * @param options - Parse options (e.g., enable validation)
 * @returns Parsed CTRFReport object
 * @throws ParseError if JSON is invalid
 * @throws ValidationError if validation is enabled and fails
 *
 * @example
 * ```typescript
 * const report = parse(jsonString);
 *
 * // With validation
 * const report = parse(jsonString, { validate: true });
 * ```
 */
declare function parse(json: string, options?: ParseOptions): CTRFReport;
/**
 *
 * @group Core Operations
 * Serialize a CTRFReport to a JSON string.
 *
 * @param report - The CTRF report to serialize
 * @param options - Stringify options (pretty print, indent)
 * @returns JSON string representation
 *
 * @example
 * ```typescript
 * const json = stringify(report);
 *
 * // Pretty print
 * const json = stringify(report, { pretty: true });
 *
 * // Custom indent
 * const json = stringify(report, { pretty: true, indent: 4 });
 * ```
 */
declare function stringify(report: CTRFReport, options?: StringifyOptions): string;

/**
 * CTRF Report Merging
 */

/**
 *
 * @group Merge
 * Merge multiple CTRF reports into a single report.
 * Useful for combining results from parallel or sharded test runs.
 *
 * @param reports - Array of CTRF reports to merge
 * @param options - Merge options (deduplication, environment handling)
 * @returns A new merged CTRFReport
 * @throws Error if no reports are provided
 *
 * @example
 * ```typescript
 * const merged = merge([report1, report2, report3]);
 *
 * // With deduplication by execution, logical test, or legacy ID
 * const merged = merge(reports, { deduplicateTests: true });
 *
 * // Keep first environment only
 * const merged = merge(reports, { preserveEnvironment: 'first' });
 * ```
 */
declare function merge(reports: CTRFReport[], options?: MergeOptions): CTRFReport;

/**
 * CTRF Filtering and Querying
 */

/**
 *
 * @group Query & Filter
 * Filter tests in a report by criteria.
 *
 * @param report - The CTRF report containing tests to filter
 * @param criteria - Filter criteria (status, tags, suite, flaky, browser, device)
 * @returns Array of tests matching all specified criteria
 *
 * @example
 * ```typescript
 * // Filter by status
 * const failed = filterTests(report, { status: 'failed' });
 *
 * // Filter by multiple criteria
 * const filtered = filterTests(report, {
 *   status: ['failed', 'skipped'],
 *   tags: ['smoke'],
 *   flaky: true
 * });
 * ```
 */
declare function filterTests(report: CTRFReport, criteria: FilterCriteria): Test[];
/**
 *
 * @group Query & Filter
 * Find a single test in a report.
 *
 * @param report - The CTRF report to search
 * @param criteria - Filter criteria including testId, executionId, legacy id, name, status, tags, etc.
 * @returns The first matching test, or undefined if not found
 *
 * @example
 * ```typescript
 * // Find by stable logical test case ID
 * const test = findTest(report, { testId: 'auth/login' });
 *
 * // Find by name
 * const test = findTest(report, { name: 'should login' });
 *
 * // Find by multiple criteria
 * const test = findTest(report, { status: 'failed', flaky: true });
 * ```
 */
declare function findTest(report: CTRFReport, criteria: FilterCriteria): Test | undefined;

/**
 * CTRF Insights Calculation
 *
 * This module replicates the functionality of the existing run-insights.ts
 * while using the reference implementation's type system and API signatures.
 */

/**
 *
 * @group Insights
 * Determines if a test is flaky based on the CTRF specification.
 *
 * A test is considered flaky if:
 * - The `flaky` field is explicitly set to `true`, OR
 * - The test has retries > 0 AND final status is 'passed'
 *
 * @param test - The test to check
 * @returns true if the test is flaky
 *
 * @example
 * ```typescript
 * if (isTestFlaky(test)) {
 *   console.log('Test is flaky:', test.name);
 * }
 * ```
 */
declare function isTestFlaky(test: Test): boolean;
/**
 *
 * @group Insights
 * Add insights to a CTRF report using historical data.
 *
 * Computes run-level and test-level insights according to the CTRF specification,
 * including pass rate, fail rate, flaky rate, and duration metrics.
 *
 * @param report - The current report to enrich with insights
 * @param historicalReports - Array of previous reports for trend analysis
 * @param options - Options including baseline for comparison
 * @returns A new report with insights populated
 *
 * @example
 * ```typescript
 * // Basic usage
 * const reportWithInsights = addInsights(currentReport, previousReports);
 *
 * // With baseline comparison
 * const reportWithInsights = addInsights(currentReport, previousReports, {
 *   baseline: baselineReport
 * });
 * ```
 */
declare function addInsights(report: CTRFReport, historicalReports?: CTRFReport[], options?: InsightsOptions): CTRFReport;

/**
 * CTRF Schema Access
 */
/**
 *
 * @group Schema & Versioning
 * The current version CTRF JSON Schema object.
 *
 * @example
 * ```typescript
 * import { schema } from 'ctrf';
 * console.log(schema.$schema);
 * ```
 */
declare const schema: object;
/**
 *
 * @group Schema & Versioning
 * Get the JSON Schema for a specific CTRF spec version.
 *
 * @param version - The spec version (MAJOR.MINOR.PATCH) to get the schema for
 * @returns The JSON Schema object for that version
 * @throws SchemaVersionError if the version is not supported
 *
 * @example
 * ```typescript
 * const v0_0Schema = getSchema('0.0.0');
 * const v1_0Schema = getSchema('1.0.0');
 * ```
 */
declare function getSchema(version: string): object;
/**
 *
 * @group Schema & Versioning
 * Get the current spec version.
 *
 * @returns The current spec version string
 */
declare function getCurrentSpecVersion(): string;
/**
 *
 * @group Schema & Versioning
 * Get all supported spec versions.
 *
 * @returns Array of supported version strings
 */
declare function getSupportedSpecVersions(): readonly string[];

/**
 * CTRF Error Classes
 */

/**
 *
 * @group Errors
 * Base error class for all CTRF errors.
 * All CTRF-specific errors extend this class.
 */
declare class CTRFError extends Error {
    constructor(message: string);
}
/**
 *
 * @group Errors
 * Error thrown when schema validation fails.
 * Contains detailed error information for each validation issue.
 */
declare class ValidationError extends CTRFError {
    /** Detailed validation errors */
    readonly errors: ValidationErrorDetail[];
    constructor(message: string, errors?: ValidationErrorDetail[]);
}
/**
 *
 * @group Errors
 * Error thrown when JSON parsing fails.
 */
declare class ParseError extends CTRFError {
    /** The original error that caused the parse failure */
    readonly cause?: Error;
    constructor(message: string, cause?: Error);
}
/**
 *
 * @group Errors
 * Error thrown when an unsupported CTRF specification version is encountered.
 */
declare class SchemaVersionError extends CTRFError {
    /** The unsupported version */
    readonly version: string;
    /** Supported versions */
    readonly supportedVersions: string[];
    constructor(version: string, supportedVersions: string[]);
}
/**
 *
 * @group Errors
 * Error thrown when a file read or write operation fails.
 */
declare class FileError extends CTRFError {
    /** The file path that caused the error */
    readonly filePath: string;
    /** The original error */
    readonly cause?: Error;
    constructor(message: string, filePath: string, cause?: Error);
}
/**
 *
 * @group Errors
 * Error thrown when building a report or test fails due to missing required fields.
 */
declare class BuilderError extends CTRFError {
    constructor(message: string);
}

export { type Attachment, type Baseline, BuilderError, CTRFError, type CTRFReport, CTRF_NAMESPACE, CURRENT_SPEC_VERSION, type Environment, FileError, type FilterCriteria, type Insights, type InsightsOptions, type LabelPrimitive, type LabelValue, type MergeOptions, type MetricDelta, ParseError, type ParseOptions, REPORT_FORMAT, ReportBuilder, type ReportBuilderOptions, type Results, type RetryAttempt, SUPPORTED_SPEC_VERSIONS, SchemaVersionError, type Step, type StringifyOptions, type Summary, type SummaryOptions, TEST_STATUSES, type Test, TestBuilder, type TestBuilderOptions, type TestInsights, type TestStatus, type Tool, type ValidateOptions, ValidationError, type ValidationErrorDetail, type ValidationResult, addInsights, calculateSummary, filterTests, findTest, generateReportId, generateTestId, getCurrentSpecVersion, getSchema, getSupportedSpecVersions, hasInsights, isCTRFReport, isRetryAttempt, isTest, isTestFlaky, isTestStatus, isValid, merge, parse, schema, stringify, validate, validateStrict };
