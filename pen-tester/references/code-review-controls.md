# Source Code Review Controls Library

## Overview

This library contains **51 source code review controls** organized into **3 domains** and **12 control families**. Each control applies to one or more supported languages: Python, JavaScript/TypeScript, and Rust.

### Control Domains

| Domain | Prefix | Families | Focus |
|--------|--------|----------|-------|
| Secure Code | SEC | SEC-INJ, SEC-MEM, SEC-CRYPTO, SEC-AUTH, SEC-DATA | Vulnerability prevention and secure coding patterns |
| Complexity | CPX | CPX-STRUCT, CPX-METRIC, CPX-MAINTAIN | Code complexity, cognitive load, and structural quality |
| Development Practices | DEV | DEV-DEP, DEV-TEST, DEV-QUAL, DEV-BUILD | Dependencies, testing, quality, and build/deploy hygiene |

### Framework References

Controls are mapped to authoritative sources. Footnote marks appear on findings lines in the interactive report; the legend on the last page provides the full reference.

| Mark | Source | Version | Scope |
|------|--------|---------|-------|
| ¹ | OWASP ASVS | 5.0 (2025) | Application security verification requirements |
| ² | CWE Top 25 | 2025 | Most dangerous software weaknesses (MITRE/CISA) |
| ³ | SEI CERT | C/C++/Java (current) | Secure coding rules — language-specific |
| ⁴ | NIST SSDF | SP 800-218 Rev 1 (2025) | Secure software development practices |
| ⁵ | OWASP Top 10 | 2025 | Web application security risks |
| ⁶ | ISO/IEC 25010 | 2023 | Software quality model — maintainability and reliability |
| ⁷ | McCabe | Cyclomatic Complexity (1976) | Structural complexity measurement |
| ⁸ | Cognitive Complexity | SonarSource (2017) | Human-readable complexity measurement |
| ⁹ | OWASP Secure Coding | Quick Ref Guide (2024) | Secure coding practice checklist |
| ¹⁰ | Rust Safety | Rust Reference / Rustonomicon | Memory safety and unsafe code guidelines |
| ¹¹ | PEP Standards | PEP 8 / PEP 484 / PEP 526 | Python coding standards and type annotations |
| ¹² | NIST SP 800-53 | Rev 5 | Security and privacy controls |
| ¹³ | CMMC 2.0 | Level 2 (2023) | DoD cybersecurity maturity — 110 practices from NIST 800-171 |
| ¹⁴ | DoD Cloud Computing SRG | v1r4 (2024) | Department of Defense cloud security requirements |
| ¹⁵ | FedRAMP | Rev 5 Baselines (2024) | Federal cloud security — NIST 800-53 baselines |
| ¹⁶ | HIPAA Security Rule | 45 CFR §164 | Healthcare data protection requirements |
| ¹⁷ | PCI-DSS | v4.0.1 (2024) | Payment card industry data security standard |
| ¹⁸ | SOC 2 Type II | TSC 2022 | AICPA Trust Services Criteria |
| ¹⁹ | SEC/FINRA | Reg S-P, Cyber Rule (2023) | Securities industry cybersecurity requirements |
| ²⁰ | EU DORA | Reg (EU) 2022/2554 | Digital operational resilience for financial entities |
| ²¹ | EU AI Act | Reg (EU) 2024/1689 | Risk-based regulation for AI systems |

### Language Applicability

| Abbreviation | Languages |
|---|---|
| ALL | Python, JavaScript, TypeScript, Rust |
| PY | Python |
| JS/TS | JavaScript and TypeScript |
| RS | Rust |
| PY,JS/TS | Python, JavaScript, TypeScript |
| PY,RS | Python, Rust |
| JS/TS,RS | JavaScript/TypeScript, Rust |

---

## SEC-INJ — Injection Prevention

### SEC-INJ-001
- **Name**: SQL Injection Prevention
- **Languages**: ALL
- **CIA**: C, I
- **Sources**: ²⁵⁹¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **CWE**: CWE-89
- **Statement**: All database queries use parameterized statements or prepared queries. No string concatenation or interpolation is used to build SQL.
- **Severity**: CRITICAL
- **Test**: Search for string concatenation/interpolation in SQL query construction. Verify ORM usage or parameterized queries.
- **Python**: Check for f-strings, `.format()`, or `%` in `cursor.execute()`. Verify use of parameterized `?` or `%s` placeholders, or ORM (SQLAlchemy, Django ORM).
- **JS/TS**: Check for template literals or concatenation in `query()` calls. Verify use of `$1`/`?` placeholders (pg, mysql2) or ORM (Prisma, TypeORM, Drizzle).
- **Rust**: Check for `format!()` in SQL strings. Verify use of `sqlx::query!()` macro with bind parameters, or Diesel query builder.

### SEC-INJ-002
- **Name**: Command Injection Prevention
- **Languages**: ALL
- **CIA**: C, I, A
- **Sources**: ²⁹¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **CWE**: CWE-78
- **Statement**: System commands are not constructed from user input. Where shell execution is necessary, inputs are validated, escaped, and passed as separate arguments rather than interpolated into command strings.
- **Severity**: CRITICAL
- **Test**: Search for shell execution functions with user-controlled input.
- **Python**: Check `os.system()`, `subprocess.call(shell=True)`, `os.popen()`. Verify `subprocess.run()` with `shell=False` and list args.
- **JS/TS**: Check `child_process.exec()`, `eval()`, `Function()`. Verify `execFile()` or `spawn()` with array args.
- **Rust**: Check `Command::new()` with `.arg()` from unchecked user input. Verify no shell invocation via `sh -c`.

### SEC-INJ-003
- **Name**: Cross-Site Scripting Prevention (Output Encoding)
- **Languages**: JS/TS, PY
- **CIA**: C, I
- **Sources**: ²⁵⁹¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **CWE**: CWE-79
- **Statement**: All user-supplied data rendered into HTML is contextually encoded. Raw HTML insertion (innerHTML, dangerouslySetInnerHTML, |safe, Markup()) is avoided or explicitly sanitized.
- **Severity**: HIGH
- **Test**: Search for raw HTML insertion patterns and verify encoding/sanitization.
- **Python**: Check Jinja2 `|safe`, `Markup()`, Django `mark_safe()`. Verify autoescaping is enabled.
- **JS/TS**: Check `innerHTML`, `outerHTML`, `document.write()`, `dangerouslySetInnerHTML`, `v-html`. Verify use of textContent or DOMPurify.

### SEC-INJ-004
- **Name**: Path Traversal Prevention
- **Languages**: ALL
- **CIA**: C, I
- **Sources**: ²⁹¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **CWE**: CWE-22
- **Statement**: File paths constructed from user input are validated against a whitelist or resolved and checked to remain within an expected base directory. Directory traversal sequences (../) are rejected.
- **Severity**: HIGH
- **Test**: Search for file operations using user-controlled paths.
- **Python**: Check `open()`, `Path()`, `os.path.join()` with user input. Verify `os.path.realpath()` + startswith check.
- **JS/TS**: Check `fs.readFile()`, `path.join()` with user input. Verify `path.resolve()` + startsWith check.
- **Rust**: Check `std::fs::read()`, `Path::new()` with user input. Verify `.canonicalize()` + starts_with check.

### SEC-INJ-005
- **Name**: Deserialization Safety
- **Languages**: ALL
- **CIA**: C, I, A
- **Sources**: ²⁵¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **CWE**: CWE-502
- **Statement**: Untrusted data is never deserialized using unsafe deserializers. Safe alternatives (JSON, protobuf, MessagePack) or strict type validation are used.
- **Severity**: CRITICAL
- **Test**: Search for unsafe deserialization of untrusted input.
- **Python**: Check `pickle.loads()`, `yaml.load()` (without SafeLoader), `marshal.loads()`. Verify `json.loads()` or `yaml.safe_load()`.
- **JS/TS**: Check `eval()`, `Function()` for parsing, `node-serialize`. Verify `JSON.parse()` with schema validation (Zod, Joi).
- **Rust**: Check `serde` with unvalidated input types. Verify deserialization into strongly-typed structs with `#[serde(deny_unknown_fields)]`.

### SEC-INJ-006
- **Name**: Regular Expression Denial of Service (ReDoS) Prevention
- **Languages**: PY, JS/TS
- **CIA**: A
- **Sources**: ²⁹¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **CWE**: CWE-1333
- **Statement**: Regular expressions applied to user input do not use catastrophic backtracking patterns (nested quantifiers, ambiguous alternation). Timeouts or safe regex libraries are used.
- **Severity**: MEDIUM
- **Test**: Identify regex patterns with nested quantifiers applied to external input.
- **Python**: Check for `re.compile()` with `(a+)+`, `(a|a)*` patterns on user input. Verify use of `re2` or timeouts.
- **JS/TS**: Check for regex literals with nested quantifiers on user input. Verify use of `re2` package or `RegExp` with timeout.

---

## SEC-MEM — Memory and Resource Safety

### SEC-MEM-001
- **Name**: Buffer Overflow Prevention
- **Languages**: RS
- **CIA**: C, I, A
- **Sources**: ²³¹⁰¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **CWE**: CWE-120, CWE-787
- **Statement**: Code does not use unchecked indexing or raw pointer arithmetic to write beyond buffer boundaries. Bounds-checked access methods are used.
- **Severity**: CRITICAL
- **Test**: Search for unsafe blocks with raw pointer arithmetic, unchecked slice indexing.
- **Rust**: Check `unsafe` blocks with `*ptr.offset()`, `*ptr.add()`, `slice::from_raw_parts()`. Verify bounds checking with `.get()` or safe iterators.

### SEC-MEM-002
- **Name**: Use-After-Free Prevention
- **Languages**: RS
- **CIA**: C, I, A
- **Sources**: ²¹⁰¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **CWE**: CWE-416
- **Statement**: References are not used after the pointed-to value has been moved, dropped, or deallocated. The borrow checker is not circumvented unsafely.
- **Severity**: CRITICAL
- **Test**: Search for unsafe code that dereferences raw pointers after potential deallocation.
- **Rust**: Check `unsafe` blocks with raw pointer dereferences after `drop()`, `ManuallyDrop`, or `Box::from_raw()`. Verify lifetimes are correctly annotated.

### SEC-MEM-003
- **Name**: Integer Overflow/Underflow Prevention
- **Languages**: ALL
- **CIA**: I, A
- **Sources**: ²³¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **CWE**: CWE-190, CWE-191
- **Statement**: Arithmetic operations that could overflow or underflow are checked, or the language's overflow protection is enabled.
- **Severity**: MEDIUM
- **Test**: Search for arithmetic on user-controlled integers without bounds checking.
- **Python**: Python integers have arbitrary precision; check for issues at system boundaries (ctypes, struct.pack, numpy fixed-width).
- **JS/TS**: Check for arithmetic exceeding `Number.MAX_SAFE_INTEGER`. Verify use of `BigInt` where needed.
- **Rust**: Verify debug overflow checks remain meaningful. Check for `wrapping_*` or explicit `checked_*` methods on security-critical arithmetic. Check `as` casts between integer types.

### SEC-MEM-004
- **Name**: Unsafe Code Minimization
- **Languages**: RS
- **CIA**: C, I, A
- **Sources**: ¹⁰⁴¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **CWE**: CWE-676
- **Statement**: `unsafe` blocks are minimal in scope, documented with safety invariant comments, and isolated behind safe API boundaries. No unnecessary unsafe usage.
- **Severity**: HIGH
- **Test**: Count and audit all `unsafe` blocks.
- **Rust**: Check ratio of unsafe to safe code. Verify each `unsafe` block has a `// SAFETY:` comment documenting the invariant. Check for safe alternatives.

### SEC-MEM-005
- **Name**: Resource Leak Prevention
- **Languages**: ALL
- **CIA**: A
- **Sources**: ³⁶¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **CWE**: CWE-401, CWE-772
- **Statement**: Acquired resources (files, sockets, connections, locks) are always released, using language-appropriate RAII, context managers, or finally blocks.
- **Severity**: MEDIUM
- **Test**: Search for resource acquisition without corresponding cleanup patterns.
- **Python**: Check `open()` without `with` statement. Verify context managers for DB connections, locks, temp files.
- **JS/TS**: Check for unclosed streams, DB connections without `.finally()` or `using` declarations. Verify cleanup in error paths.
- **Rust**: Verify `Drop` implementation for custom resource types. Check for `mem::forget()` on resource-holding types.

### SEC-MEM-006
- **Name**: Null/None Safety
- **Languages**: ALL
- **CIA**: A, I
- **Sources**: ²⁶¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **CWE**: CWE-476
- **Statement**: Nullable values are checked before dereferencing. Language-specific null safety features are used (Optional types, strict null checks, Option<T>).
- **Severity**: MEDIUM
- **Test**: Search for unchecked nullable access patterns.
- **Python**: Check for attribute access without None guards. Verify `Optional[]` type annotations with explicit None checks.
- **JS/TS**: Verify `strictNullChecks` is enabled in tsconfig. Check for optional chaining (`?.`) usage. Check for `!` non-null assertions.
- **Rust**: Verify `.unwrap()` calls are justified or replaced with `?`, `.unwrap_or()`, or pattern matching on `Option<T>`.

---

## SEC-CRYPTO — Cryptography and Secrets

### SEC-CRYPTO-001
- **Name**: No Hardcoded Secrets
- **Languages**: ALL
- **CIA**: C
- **Sources**: ¹²⁴⁹¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **CWE**: CWE-798
- **Statement**: No API keys, passwords, tokens, private keys, or cryptographic secrets are hardcoded in source files. All secrets are loaded from environment variables or a secrets manager.
- **Severity**: CRITICAL
- **Test**: Search for high-entropy strings, common key patterns (sk_live, AKIA, BEGIN PRIVATE KEY), and assignment to variables named *key*, *secret*, *password*, *token*.
- **Python**: Check for secrets in `.py` files, `settings.py`, `config.py`. Verify use of `os.environ`, `python-dotenv`, or secrets managers.
- **JS/TS**: Check for secrets in `.js/.ts/.json` files, `config.ts`. Verify use of `process.env`, `.env` files (not committed), or vault clients.
- **Rust**: Check for secrets in `.rs` files, `Cargo.toml`. Verify use of `std::env::var()` or secrets crates.

### SEC-CRYPTO-002
- **Name**: Strong Cryptographic Algorithms
- **Languages**: ALL
- **CIA**: C, I
- **Sources**: ¹⁹¹²¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **CWE**: CWE-327
- **Statement**: Only current, approved cryptographic algorithms are used. Deprecated algorithms (MD5, SHA1 for security, DES, 3DES, RC4, ECB mode) are absent from security-sensitive code.
- **Severity**: HIGH
- **Test**: Search for deprecated algorithm usage in cryptographic operations.
- **Python**: Check for `hashlib.md5()`, `hashlib.sha1()` (for security), `DES`, `Blowfish` in `cryptography` or `pycryptodome`. Verify AES-GCM, SHA-256+, Ed25519.
- **JS/TS**: Check for `crypto.createHash('md5')`, `crypto.createCipher()` (deprecated). Verify `crypto.createCipheriv()` with AES-GCM, SHA-256+.
- **Rust**: Check for `md5`, `sha1` crates in security contexts. Verify `ring`, `aes-gcm`, `sha2` crates.

### SEC-CRYPTO-003
- **Name**: Secure Random Number Generation
- **Languages**: ALL
- **CIA**: C
- **Sources**: ¹²⁹¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **CWE**: CWE-330
- **Statement**: Security-sensitive random values (tokens, IDs, nonces, keys) use cryptographically secure random generators, not predictable PRNGs.
- **Severity**: HIGH
- **Test**: Search for non-cryptographic random usage in security contexts.
- **Python**: Check for `random.random()`, `random.randint()` in token/key generation. Verify `secrets.token_hex()`, `os.urandom()`.
- **JS/TS**: Check for `Math.random()` in security contexts. Verify `crypto.randomBytes()`, `crypto.randomUUID()`.
- **Rust**: Check for `rand::thread_rng()` in security contexts. Verify `rand::rngs::OsRng` or `getrandom` crate.

### SEC-CRYPTO-004
- **Name**: Password Storage Security
- **Languages**: ALL
- **CIA**: C
- **Sources**: ¹²⁹¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **CWE**: CWE-916
- **Statement**: Passwords are stored using adaptive hashing algorithms (Argon2id, bcrypt, scrypt) with appropriate cost factors. Plaintext or simple hash storage is prohibited.
- **Severity**: CRITICAL
- **Test**: Search for password hashing patterns and verify algorithm choice.
- **Python**: Check for `hashlib.sha256(password)` without salt. Verify `bcrypt.hashpw()`, `argon2.PasswordHasher()`, or Django `make_password()`.
- **JS/TS**: Check for `crypto.createHash()` on passwords. Verify `bcrypt.hash()`, `argon2.hash()`.
- **Rust**: Check for `sha2::Digest` on passwords. Verify `argon2` or `bcrypt` crate with proper cost.

---

## SEC-AUTH — Authentication and Authorization in Code

### SEC-AUTH-001
- **Name**: Authentication Bypass Prevention
- **Languages**: ALL
- **CIA**: A, C
- **Sources**: ¹⁵⁹¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **CWE**: CWE-287
- **Statement**: Authentication checks cannot be bypassed through alternative code paths, parameter manipulation, or missing middleware. All protected routes/functions have explicit auth guards.
- **Severity**: CRITICAL
- **Test**: Review route definitions and verify every protected endpoint has authentication middleware/decorator.
- **Python**: Check Flask `@login_required`, Django `@permission_required`. Verify no unprotected views serve sensitive data.
- **JS/TS**: Check Express middleware chains, Next.js middleware. Verify no routes skip auth middleware.
- **Rust**: Check Actix `middleware::from_fn()`, Axum extractors. Verify no handlers lack auth guards.

### SEC-AUTH-002
- **Name**: Proper Authorization Checks
- **Languages**: ALL
- **CIA**: C, I
- **Sources**: ¹²⁵¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **CWE**: CWE-862, CWE-863
- **Statement**: Authorization is checked server-side for every operation that accesses or modifies resources. Client-side checks alone are insufficient. Object-level authorization prevents IDOR.
- **Severity**: HIGH
- **Test**: Review data access functions for ownership/role verification.
- **Python**: Check for `object.user_id == request.user.id` patterns. Verify Django `get_object_or_404()` includes user filter.
- **JS/TS**: Check for direct DB queries without user scope. Verify Prisma/TypeORM queries include `where: { userId }`.
- **Rust**: Check for unscoped DB queries. Verify ownership checks in handler logic.

### SEC-AUTH-003
- **Name**: JWT/Token Security
- **Languages**: ALL
- **CIA**: C, I
- **Sources**: ¹⁹¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **CWE**: CWE-347
- **Statement**: JWTs are validated for signature, algorithm, expiration, issuer, and audience. Algorithm confusion (none, HS256 when RS256 expected) is prevented. Tokens are not stored in localStorage.
- **Severity**: HIGH
- **Test**: Review JWT verification code for complete validation.
- **Python**: Check `jwt.decode()` for `algorithms` parameter. Verify expiration and issuer checks. Check PyJWT options.
- **JS/TS**: Check `jsonwebtoken.verify()` for `algorithms` whitelist. Verify `ignoreExpiration` is not `true`. Check storage location.
- **Rust**: Check `jsonwebtoken::decode()` for `Validation` struct completeness. Verify algorithm restriction.

---

## SEC-DATA — Data Protection

### SEC-DATA-001
- **Name**: Sensitive Data Logging Prevention
- **Languages**: ALL
- **CIA**: C
- **Sources**: ¹⁴⁹¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **CWE**: CWE-532
- **Statement**: Logging statements do not include passwords, tokens, API keys, PII, or other sensitive data. Log redaction is applied to request/response bodies containing sensitive fields.
- **Severity**: HIGH
- **Test**: Search for logging calls that include sensitive variable names or unfiltered request bodies.
- **Python**: Check `logging.info(f"user={user}, password={password}")`. Verify sensitive fields are redacted. Check Django `SENSITIVE_VARIABLES_KEY`.
- **JS/TS**: Check `console.log(req.body)`, `logger.info({ password })`. Verify middleware strips sensitive fields from logs.
- **Rust**: Check `tracing::info!()`, `log::debug!()` for sensitive data. Verify `#[instrument(skip(password))]`.

### SEC-DATA-002
- **Name**: PII Minimization in Code
- **Languages**: ALL
- **CIA**: C
- **Sources**: ¹⁴¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **CWE**: CWE-359
- **Statement**: Code collects, processes, and returns only the minimum PII required for the operation. SELECT * and full-object serialization of user records are avoided.
- **Severity**: MEDIUM
- **Test**: Search for over-broad data queries and serialization patterns.
- **Python**: Check for `SELECT *` in queries, full model serialization. Verify `.values('field1','field2')` or explicit serializer fields.
- **JS/TS**: Check for `SELECT *`, `findMany()` without `select`. Verify Prisma `select: {}` or GraphQL field selection.
- **Rust**: Check for `SELECT *` in sqlx queries. Verify column selection and DTO structs.

### SEC-DATA-003
- **Name**: Input Validation and Sanitization
- **Languages**: ALL
- **CIA**: I, A
- **Sources**: ¹²⁹¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **CWE**: CWE-20
- **Statement**: All external input is validated for type, length, range, and format before processing. Validation occurs server-side regardless of client-side checks. Schemas or type systems enforce constraints.
- **Severity**: HIGH
- **Test**: Review input processing for validation presence and completeness.
- **Python**: Check for raw `request.form` usage without validation. Verify Pydantic models, marshmallow schemas, or Django forms.
- **JS/TS**: Check for `req.body.field` without validation. Verify Zod, Joi, class-validator schemas, or TypeScript type guards.
- **Rust**: Check for `serde` deserialization without constraint validation. Verify `validator` crate or custom `TryFrom` implementations.

### SEC-DATA-004
- **Name**: Error Information Disclosure Prevention
- **Languages**: ALL
- **CIA**: C
- **Sources**: ¹²⁹¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **CWE**: CWE-209
- **Statement**: Error responses do not expose stack traces, internal paths, database schemas, or implementation details to end users. Debug mode is disabled in production configurations.
- **Severity**: MEDIUM
- **Test**: Search for unfiltered error propagation to responses.
- **Python**: Check for `DEBUG = True` in production, bare `except: return str(e)`. Verify custom error handlers.
- **JS/TS**: Check for `res.status(500).json({ error: err.stack })`. Verify NODE_ENV-aware error handlers.
- **Rust**: Check for `.unwrap()` in handlers (panics expose info). Verify custom error types with `Display` that hide internals.

---

## CPX-STRUCT — Structural Complexity

### CPX-STRUCT-001
- **Name**: Function Length Limit
- **Languages**: ALL
- **CIA**: —
- **Sources**: ⁶⁸¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **Statement**: Functions/methods do not exceed 50 lines of logic (excluding blank lines and comments). Functions over 30 lines should be reviewed for decomposition opportunities.
- **Severity**: LOW
- **Test**: Measure function body length. Flag functions exceeding 50 lines, warn at 30.
- **Python**: Count lines in `def` blocks. Check class methods separately.
- **JS/TS**: Count lines in function/arrow function bodies.
- **Rust**: Count lines in `fn` blocks, including `impl` methods.

### CPX-STRUCT-002
- **Name**: Function Parameter Count Limit
- **Languages**: ALL
- **CIA**: —
- **Sources**: ⁶¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **Statement**: Functions accept no more than 5 parameters. Functions with more than 5 parameters should use an options object, builder pattern, or data class.
- **Severity**: LOW
- **Test**: Count function parameters. Flag functions exceeding 5.
- **Python**: Check `def` signatures. Verify use of dataclasses or `**kwargs` with TypedDict.
- **JS/TS**: Check function signatures. Verify use of options objects with interface types.
- **Rust**: Check `fn` signatures. Verify use of builder pattern or config structs.

### CPX-STRUCT-003
- **Name**: Nesting Depth Limit
- **Languages**: ALL
- **CIA**: —
- **Sources**: ⁶⁸¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **Statement**: Control flow nesting does not exceed 4 levels. Deeply nested code should use early returns, guard clauses, or extraction into helper functions.
- **Severity**: MEDIUM
- **Test**: Measure maximum nesting depth of control flow statements.
- **Python**: Count nested `if/for/while/with/try` levels. Verify early returns and guard clauses.
- **JS/TS**: Count nested braces in control flow. Verify early returns and optional chaining.
- **Rust**: Count nested `if/for/while/match/loop` levels. Verify `?` operator and early returns.

### CPX-STRUCT-004
- **Name**: File Length Limit
- **Languages**: ALL
- **CIA**: —
- **Sources**: ⁶¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **Statement**: Source files do not exceed 500 lines (excluding comments and blanks). Files approaching this limit should be decomposed into focused modules.
- **Severity**: INFORMATIONAL
- **Test**: Count logical lines per file. Flag files exceeding 500, warn at 300.

### CPX-STRUCT-005
- **Name**: Class/Module Cohesion
- **Languages**: ALL
- **CIA**: —
- **Sources**: ⁶¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **Statement**: Classes and modules have a single, well-defined responsibility. Methods within a class operate on shared state; unrelated functionality is separated into distinct modules.
- **Severity**: LOW
- **Test**: Review class structure for single responsibility. Check for classes with methods that don't share instance state.
- **Python**: Check for classes with unrelated method groups, God classes. Verify module-level function organization.
- **JS/TS**: Check for large classes with mixed concerns. Verify module decomposition.
- **Rust**: Check for `impl` blocks with unrelated methods. Verify trait-based decomposition.

---

## CPX-METRIC — Measurable Complexity

### CPX-METRIC-001
- **Name**: Cyclomatic Complexity Limit
- **Languages**: ALL
- **CIA**: —
- **Sources**: ⁷⁶¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **Statement**: Functions have a cyclomatic complexity of 10 or less. Functions exceeding 15 require mandatory refactoring. Measured as the number of linearly independent paths through the function.
- **Severity**: MEDIUM
- **Test**: Calculate cyclomatic complexity per function. Flag >10, mandatory refactor >15.
- **Python**: Use `radon cc` or `mccabe`. Each `if/elif/for/while/except/and/or/assert` adds 1.
- **JS/TS**: Use `eslint complexity rule` or `plato`. Each branch/loop/ternary adds 1.
- **Rust**: Use `cargo clippy` cognitive complexity lint. Each branch/loop/match arm adds 1.

### CPX-METRIC-002
- **Name**: Cognitive Complexity Limit
- **Languages**: ALL
- **CIA**: —
- **Sources**: ⁸⁶¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **Statement**: Functions have a cognitive complexity of 15 or less. Cognitive complexity penalizes nested control flow more heavily than flat structures, measuring human readability rather than path count.
- **Severity**: MEDIUM
- **Test**: Calculate cognitive complexity per function. Flag >15.
- **Python**: Use `flake8-cognitive-complexity` or `wily`. Nesting increments add cumulative penalties.
- **JS/TS**: Use SonarQube or `eslint-plugin-sonarjs`. Nesting increments are penalized.
- **Rust**: Use `clippy::cognitive_complexity` lint. Default threshold is 25 in clippy.

### CPX-METRIC-003
- **Name**: Halstead Complexity Assessment
- **Languages**: ALL
- **CIA**: —
- **Sources**: ⁶¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **Statement**: Halstead Effort metric is assessed for functions above the cyclomatic threshold. Exceptionally high Halstead Difficulty (>30) combined with high volume indicates code requiring simplification.
- **Severity**: LOW
- **Test**: Calculate Halstead metrics for flagged functions. Report Difficulty and Effort.
- **Python**: Use `radon hal`. Report Volume, Difficulty, Effort per function.
- **JS/TS**: Use `escomplex` or `typhonjs-escomplex`. Report per-function metrics.
- **Rust**: Manual assessment — count operators and operands in flagged functions.

### CPX-METRIC-004
- **Name**: Maintainability Index
- **Languages**: ALL
- **CIA**: —
- **Sources**: ⁶⁷⁸¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **Statement**: Files maintain a Maintainability Index of 20 or above (0–100 scale, where 100 = easily maintainable). Files below 20 require refactoring.
- **Severity**: MEDIUM
- **Test**: Calculate MI per file. Flag files below 20 (poor), warn below 40 (moderate).
- **Python**: Use `radon mi`. MI combines Halstead Volume, cyclomatic complexity, and LOC.
- **JS/TS**: Use `plato` or `escomplex`. Same composite formula.
- **Rust**: Calculate based on cyclomatic complexity and function length metrics.

---

## CPX-MAINTAIN — Maintainability Practices

### CPX-MAINTAIN-001
- **Name**: Type Safety and Annotations
- **Languages**: ALL
- **CIA**: —
- **Sources**: ⁶¹¹¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **Statement**: Functions have type annotations on parameters and return values. TypeScript strict mode is enabled. Type: ignore/any bypasses are documented with justification.
- **Severity**: LOW
- **Test**: Check type annotation coverage and strictness configuration.
- **Python**: Check for `def func(x: int) -> str:` patterns. Verify mypy/pyright configuration. Count `# type: ignore` comments.
- **JS/TS**: Verify `strict: true` in tsconfig.json. Count `any` types and `@ts-ignore` comments. Check for implicit `any`.
- **Rust**: Inherently typed. Check for excessive `as` casts, turbofish `::<>` on generics that could be inferred, and `unsafe` type coercions.

### CPX-MAINTAIN-002
- **Name**: Dead Code Elimination
- **Languages**: ALL
- **CIA**: —
- **Sources**: ⁶⁴¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **Statement**: No unreachable code, unused imports, unused variables, or unused functions exist in the codebase. Dead code increases attack surface and maintenance burden.
- **Severity**: LOW
- **Test**: Run language-specific dead code analysis.
- **Python**: Use `vulture`, `flake8 F401/F841`, or `pyflakes`. Check for `# noqa` suppressions.
- **JS/TS**: Use `eslint no-unused-vars`, `ts-prune`. Check for `// eslint-disable` suppressions.
- **Rust**: Check compiler `#[warn(dead_code)]` output. Verify no blanket `#[allow(dead_code)]` attributes.

### CPX-MAINTAIN-003
- **Name**: Error Handling Completeness
- **Languages**: ALL
- **CIA**: A, I
- **Sources**: ³⁶⁹¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **CWE**: CWE-755
- **Statement**: All error paths are explicitly handled. Bare except/catch blocks, swallowed errors, and unhandled promise rejections are prohibited. Errors are logged or propagated, never silently ignored.
- **Severity**: MEDIUM
- **Test**: Search for empty or overly broad error handlers.
- **Python**: Check for bare `except:`, `except Exception: pass`. Verify specific exception types and logging.
- **JS/TS**: Check for empty `catch(e) {}`, missing `.catch()` on promises, unhandled async rejections. Verify `unhandledRejection` handler.
- **Rust**: Check for `.unwrap()` and `.expect()` in non-test code. Verify `Result<T, E>` propagation with `?` operator.

### CPX-MAINTAIN-004
- **Name**: Documentation and Code Comments
- **Languages**: ALL
- **CIA**: —
- **Sources**: ⁶¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **Statement**: Public APIs have documentation comments. Complex algorithms have explanatory comments. Comments explain "why," not "what." Comment-to-code ratio is between 5% and 30%.
- **Severity**: INFORMATIONAL
- **Test**: Check for docstrings/doc comments on public interfaces. Measure comment ratio.
- **Python**: Check for `"""docstring"""` on public functions/classes/modules. Verify PEP 257 compliance.
- **JS/TS**: Check for JSDoc `/** */` or TSDoc on exported functions. Verify parameter documentation.
- **Rust**: Check for `///` doc comments on `pub` items. Verify `#![warn(missing_docs)]` lint.

---

## DEV-DEP — Dependency Management

### DEV-DEP-001
- **Name**: Known Vulnerability Scanning
- **Languages**: ALL
- **CIA**: C, I, A
- **Sources**: ⁴⁵²¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **CWE**: CWE-1395
- **Statement**: All dependencies are scanned for known vulnerabilities before deployment. A dependency audit tool runs in CI and blocks releases with unpatched CRITICAL/HIGH CVEs.
- **Severity**: HIGH
- **Test**: Check for vulnerability scanning in CI pipeline. Verify scan results are recent.
- **Python**: Check for `pip-audit`, `safety`, or Dependabot. Verify `requirements.txt` or `poetry.lock` is scanned.
- **JS/TS**: Check for `npm audit`, Snyk, or Dependabot. Verify `package-lock.json` or `yarn.lock` is scanned.
- **Rust**: Check for `cargo audit`. Verify `Cargo.lock` is committed and scanned.

### DEV-DEP-002
- **Name**: Dependency Pinning
- **Languages**: ALL
- **CIA**: I
- **Sources**: ⁴¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **Statement**: All dependencies are pinned to specific versions (not ranges) in lock files. Lock files are committed to version control.
- **Severity**: MEDIUM
- **Test**: Verify lock files exist and are committed.
- **Python**: Check for `poetry.lock`, `Pipfile.lock`, or exact versions in `requirements.txt` (no `>=`, `~=`).
- **JS/TS**: Check for `package-lock.json` or `yarn.lock` in repo. Verify no `*` or `latest` in `package.json`.
- **Rust**: Check for `Cargo.lock` committed. Verify no wildcard versions in `Cargo.toml`.

### DEV-DEP-003
- **Name**: Minimal Dependency Footprint
- **Languages**: ALL
- **CIA**: A
- **Sources**: ⁴⁵¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **Statement**: Transitive dependency count is reviewed and minimized. Unnecessary or duplicate dependencies are removed. Direct dependencies are preferred over deeply nested transitive chains.
- **Severity**: LOW
- **Test**: Count direct and transitive dependencies. Flag excessive dependency trees.
- **Python**: Use `pipdeptree`. Check for unused packages with `pip-autoremove`.
- **JS/TS**: Use `npm ls --all`. Check `depcheck` for unused dependencies. Flag packages with >50 transitive deps.
- **Rust**: Use `cargo tree`. Check for duplicate crate versions. Use `cargo machete` for unused deps.

### DEV-DEP-004
- **Name**: Supply Chain Integrity
- **Languages**: ALL
- **CIA**: I
- **Sources**: ⁴⁵¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **CWE**: CWE-829
- **Statement**: Dependencies are sourced from trusted registries. Integrity hashes are verified. Private registries use authentication. Typosquatting checks are applied to dependency names.
- **Severity**: HIGH
- **Test**: Review package sources and verify integrity mechanisms.
- **Python**: Check `--require-hashes` usage with pip. Verify PyPI as only source. Check for private index auth.
- **JS/TS**: Check `integrity` fields in lockfile. Verify npm/yarn registry config. Check for `.npmrc` auth tokens (not committed).
- **Rust**: Check `Cargo.lock` checksums. Verify crates.io as source. Check for `[patch]` overrides.

---

## DEV-TEST — Testing Practices

### DEV-TEST-001
- **Name**: Test Coverage Baseline
- **Languages**: ALL
- **CIA**: —
- **Sources**: ⁴⁶¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **Statement**: Code test coverage is at least 60% by line. Security-critical modules (auth, crypto, input validation) have 80%+ coverage. Coverage is measured and tracked in CI.
- **Severity**: MEDIUM
- **Test**: Check test coverage reports. Verify coverage thresholds in CI config.
- **Python**: Check for `pytest-cov`, `coverage.py`. Verify `.coveragerc` or `pyproject.toml` threshold.
- **JS/TS**: Check for `jest --coverage`, `c8`, `istanbul`. Verify coverage thresholds in jest config.
- **Rust**: Check for `cargo tarpaulin` or `cargo llvm-cov`. Verify CI coverage reporting.

### DEV-TEST-002
- **Name**: Security-Specific Test Cases
- **Languages**: ALL
- **CIA**: C, I
- **Sources**: ⁴⁹¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **Statement**: Test suites include explicit security test cases: authentication bypass attempts, authorization boundary tests, injection payloads, and error handling verification.
- **Severity**: HIGH
- **Test**: Search test files for security-focused test cases. Verify negative testing patterns.
- **Python**: Check for `test_*unauthorized*`, `test_*injection*`, `test_*xss*` patterns. Verify pytest fixtures for auth contexts.
- **JS/TS**: Check for `describe('authorization')`, `it('should reject unauthenticated')`. Verify supertest/fetch with auth headers.
- **Rust**: Check for `#[test]` functions testing auth/authz/injection. Verify integration test modules.

### DEV-TEST-003
- **Name**: No Test-Only Security Bypasses
- **Languages**: ALL
- **CIA**: C, I
- **Sources**: ⁴⁹¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **Statement**: Production code does not contain test-only authentication or authorization bypasses (e.g., `if TEST_MODE: skip_auth()`). Test configurations do not weaken security controls.
- **Severity**: HIGH
- **Test**: Search for conditional security bypasses controlled by environment flags.
- **Python**: Check for `if settings.TESTING: return True` in auth code. Check `@override_settings` patterns.
- **JS/TS**: Check for `if (process.env.NODE_ENV === 'test')` in auth middleware. Verify no `skip` flags.
- **Rust**: Check for `#[cfg(test)]` in non-test modules that bypass security. Verify feature flags don't weaken auth.

---

## DEV-QUAL — Code Quality Practices

### DEV-QUAL-001
- **Name**: Linter and Formatter Enforcement
- **Languages**: ALL
- **CIA**: —
- **Sources**: ⁴⁶¹¹¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **Statement**: A linter and formatter are configured, enforced in CI, and cannot be bypassed without documented justification. Lint rules include security-relevant checks.
- **Severity**: LOW
- **Test**: Verify linter/formatter configuration and CI enforcement.
- **Python**: Check for `ruff`, `flake8`, or `pylint` config. Verify `black` or `ruff format`. Check pre-commit hooks.
- **JS/TS**: Check for `eslint` config with `eslint-plugin-security`. Verify `prettier`. Check husky/lint-staged.
- **Rust**: Check for `clippy` in CI (`cargo clippy -- -D warnings`). Verify `rustfmt` enforcement.

### DEV-QUAL-002
- **Name**: Static Analysis Integration
- **Languages**: ALL
- **CIA**: C, I
- **Sources**: ⁴²¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **Statement**: Static analysis security testing (SAST) runs in CI on every pull request. Findings above a defined severity threshold block merges.
- **Severity**: MEDIUM
- **Test**: Check CI configuration for SAST tool integration.
- **Python**: Check for `bandit`, `semgrep`, or `CodeQL` in CI. Verify threshold configuration.
- **JS/TS**: Check for `semgrep`, `CodeQL`, or `eslint-plugin-security` in CI. Verify error-level rules.
- **Rust**: Check for `cargo clippy`, `cargo audit`, or `semgrep` in CI. Verify `deny(warnings)`.

### DEV-QUAL-003
- **Name**: Code Review Requirements
- **Languages**: ALL
- **CIA**: I
- **Sources**: ⁴¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **Statement**: All changes to protected branches require at least one code review approval. Direct pushes to main/production branches are blocked.
- **Severity**: MEDIUM
- **Test**: Check branch protection rules and review requirements.

### DEV-QUAL-004
- **Name**: Consistent Error Types and Result Patterns
- **Languages**: ALL
- **CIA**: A, I
- **Sources**: ⁶³¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **Statement**: The codebase uses a consistent error handling pattern — custom exception hierarchies, typed error enums, or Result types — rather than mixing string errors, codes, thrown objects, and untyped catches.
- **Severity**: LOW
- **Test**: Review error type definitions and usage patterns.
- **Python**: Check for custom exception classes vs. bare `raise Exception("msg")`. Verify exception hierarchy.
- **JS/TS**: Check for custom Error subclasses vs. `throw "string"`. Verify typed error responses.
- **Rust**: Check for `thiserror` or custom `enum Error`. Verify `Result<T, E>` consistency across modules.

---

## DEV-BUILD — Build and Deployment Hygiene

### DEV-BUILD-001
- **Name**: Secret-Free Repository
- **Languages**: ALL
- **CIA**: C
- **Sources**: ⁴⁹¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **CWE**: CWE-540
- **Statement**: The repository contains no committed secrets, and a pre-commit secret scanner prevents future commits of sensitive data. Git history has been cleaned of any previously committed secrets.
- **Severity**: CRITICAL
- **Test**: Run secret scanning against the repository.
- **Python**: Check for gitleaks, detect-secrets baseline, or trufflehog in CI/pre-commit.
- **JS/TS**: Check for gitleaks or detect-secrets in CI/pre-commit. Verify `.env` is in `.gitignore`.
- **Rust**: Check for gitleaks or similar. Verify no secrets in `build.rs` or `Cargo.toml`.

### DEV-BUILD-002
- **Name**: Production Debug Disabled
- **Languages**: ALL
- **CIA**: C
- **Sources**: ¹⁹¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **CWE**: CWE-489
- **Statement**: Debug mode, verbose logging, and development-only endpoints are disabled in production configuration. Environment-specific configs clearly separate development from production.
- **Severity**: MEDIUM
- **Test**: Search for debug flags in production configuration.
- **Python**: Check `DEBUG = True` in Django/Flask production config. Verify env-based configuration.
- **JS/TS**: Check `NODE_ENV` handling. Verify no `app.use(morgan('dev'))` in production. Check for exposed `/debug` routes.
- **Rust**: Verify `debug_assertions` are not used for security logic. Check for `#[cfg(debug_assertions)]` bypasses.

### DEV-BUILD-003
- **Name**: Reproducible Builds
- **Languages**: ALL
- **CIA**: I
- **Sources**: ⁴¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **Statement**: Builds are reproducible from committed source and lock files. Build scripts do not fetch unversioned resources at build time. Docker images use pinned base images.
- **Severity**: LOW
- **Test**: Review build configuration for reproducibility.
- **Python**: Check for pinned versions in `requirements.txt`, pinned Docker base images. Verify no `pip install latest`.
- **JS/TS**: Check for `npm ci` (not `npm install`) in CI. Verify Docker multi-stage builds with pinned images.
- **Rust**: Verify `Cargo.lock` is committed. Check for `build.rs` scripts fetching external resources.

### DEV-BUILD-004
- **Name**: CI/CD Pipeline Security
- **Languages**: ALL
- **CIA**: C, I
- **Sources**: ⁴¹²¹³¹⁴¹⁵¹⁶¹⁷¹⁸¹⁹²⁰²¹
- **Statement**: CI/CD pipelines use least-privilege credentials, do not expose secrets in logs, and verify artifact integrity. Pipeline configurations are version-controlled and reviewed.
- **Severity**: HIGH
- **Test**: Review CI/CD configuration files for secret handling and permissions.

---

## Legend

The following source markers appear as superscript footnotes on findings in the interactive report:

| Mark | Full Reference |
|------|---------------|
| ¹ | **OWASP ASVS 5.0** (2025) — Application Security Verification Standard. Comprehensive security requirements covering authentication, session management, access control, validation, cryptography, error handling, data protection, communications, malicious code, business logic, files, API, and configuration. Released at Global AppSec EU Barcelona 2025. |
| ² | **CWE Top 25** (2025) — Common Weakness Enumeration, published by MITRE/CISA. The 25 most dangerous software weaknesses based on analysis of 39,080 CVE entries (June 2024–June 2025). Includes XSS (CWE-79), SQL Injection (CWE-89), Out-of-bounds Write (CWE-787), and Missing Authorization (CWE-862). |
| ³ | **SEI CERT Secure Coding Standards** — Carnegie Mellon SEI rules for C, C++, and Java. Language-specific rules preventing undefined behaviour, memory errors, and security weaknesses. Extended conceptually to Python and Rust where applicable. |
| ⁴ | **NIST SSDF SP 800-218 Rev 1** (December 2025) — Secure Software Development Framework. Practices for preparing the organization, protecting software, producing well-secured software, and responding to vulnerabilities. Includes SP 800-218A for AI-specific development. |
| ⁵ | **OWASP Top 10** (2025) — Top web application security risks. Broken Access Control (#1), Security Misconfiguration (#2), and Software Supply Chain Failures are the leading entries. |
| ⁶ | **ISO/IEC 25010** (2023) — Systems and software quality model. Defines maintainability (modularity, reusability, analysability, modifiability, testability) and reliability characteristics used to assess code quality. |
| ⁷ | **McCabe Cyclomatic Complexity** (Thomas McCabe, 1976) — Measures the number of linearly independent paths through a program's source code. The industry standard threshold is 10 per function; >15 indicates high risk. |
| ⁸ | **Cognitive Complexity** (SonarSource, G. Ann Campbell, 2017) — Measures how difficult code is for humans to read and understand. Unlike cyclomatic complexity, it penalizes nested control flow more heavily and ignores shorthand structures. |
| ⁹ | **OWASP Secure Coding Practices** — Quick Reference Guide (2024). Checklist-based secure coding practices covering input validation, output encoding, authentication, session management, access control, cryptographic practices, error handling, data protection, and communication security. |
| ¹⁰ | **Rust Safety Model** — Rust Reference and Rustonomicon. Rust's ownership, borrowing, and lifetime system provides compile-time memory safety guarantees. `unsafe` blocks opt out of these guarantees and require manual verification of safety invariants. |
| ¹¹ | **PEP Standards** — Python Enhancement Proposals: PEP 8 (style guide), PEP 484 (type hints), PEP 526 (variable annotations), PEP 257 (docstrings). Define idiomatic Python coding practices and type safety conventions. |
| ¹² | **NIST SP 800-53 Rev 5** — Security and Privacy Controls for Information Systems and Organizations. Comprehensive control catalogue covering access control (AC), audit (AU), security assessment (CA), configuration (CM), identification (IA), incident response (IR), system protection (SC), and system integrity (SI). |
| ¹³ | **CMMC 2.0 Level 2** (2023) — Cybersecurity Maturity Model Certification. 110 practices derived from NIST SP 800-171 Rev 2, required for DoD contractors handling CUI. Domains include Access Control (AC), Audit & Accountability (AU), Identification & Authentication (IA), System & Communications Protection (SC), and System & Information Integrity (SI). |
| ¹⁴ | **DoD Cloud Computing SRG** v1r4 (2024) — Security Requirements Guide for cloud service offerings hosting DoD data. Defines Impact Levels (IL2–IL6) and maps security requirements to NIST 800-53 controls. Referenced as SRG-APP-NNNNNN identifiers. |
| ¹⁵ | **FedRAMP** Rev 5 Baselines (2024) — Federal Risk and Authorization Management Program. Standardized approach to security assessment for cloud products used by federal agencies. Uses NIST 800-53 controls at Low, Moderate, and High baselines. |
| ¹⁶ | **HIPAA Security Rule** 45 CFR §164 (as amended 2024) — Health Insurance Portability and Accountability Act. Technical safeguards for protecting electronic Protected Health Information (ePHI). Key sections: §164.312(a) Access Control, §164.312(b) Audit Controls, §164.312(c) Integrity, §164.312(d) Authentication, §164.312(e) Transmission Security. |
| ¹⁷ | **PCI-DSS v4.0.1** (2024) — Payment Card Industry Data Security Standard. 12 requirements covering network security, data protection, vulnerability management, access control, monitoring, and security policy for systems handling payment card data. |
| ¹⁸ | **SOC 2 Type II** TSC 2022 — AICPA Trust Services Criteria. Common Criteria (CC1–CC9) plus supplemental criteria for Security, Availability, Processing Integrity, Confidentiality, and Privacy. Used for third-party assurance reports on service organization controls. |
| ¹⁹ | **SEC/FINRA** Cybersecurity Rules (2023) — Securities and Exchange Commission Regulation S-P (Safeguards Rule §248.30), Regulation S-ID (Identity Theft Prevention §248.201), SEC Cybersecurity Disclosure Rule (§229.106, §249.331), and FINRA Rules 3110 (Supervisory Systems) and 4370 (Business Continuity). |
| ²⁰ | **EU DORA** Regulation (EU) 2022/2554 (effective January 2025) — Digital Operational Resilience Act. ICT risk management framework for financial entities. Key articles: Art. 6 (ICT Risk Management), Art. 9 (Protection and Prevention), Art. 10 (Detection), Art. 17 (Incident Management), Art. 19 (Incident Reporting), Art. 28 (Third-party ICT Risk). |
| ²¹ | **EU AI Act** Regulation (EU) 2024/1689 (phased enforcement 2024-2027) — Risk-based regulation for AI systems. Key articles for high-risk AI: Art. 9 (Risk Management), Art. 10 (Data Governance), Art. 12 (Record-keeping), Art. 13 (Transparency), Art. 15 (Accuracy, Robustness, Cybersecurity). Art. 62 covers serious incident reporting. |
